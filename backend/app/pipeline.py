# backend/app/pipeline.py
import os
import json
import uuid
from jsonschema import validate, ValidationError
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# === PATHS ===
BASE_DIR = os.path.dirname(__file__)  # backend/app/

SCHEMA_PATH = os.path.join(BASE_DIR, "schemas", "output_schema.json")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
PROMPTS = {
    "features": os.path.join(PROMPTS_DIR, "v1_features.md"),
    "stories":  os.path.join(PROMPTS_DIR, "v1_stories.md"),
    "api_db":   os.path.join(PROMPTS_DIR, "v1_api_db.md")
}

# Output directory: backend/app/logs/<base_trace_id>/vX.json
OUTPUT_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# === Load schema and prompts ===
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    FULL_SCHEMA = json.load(f)

prompt_templates = {}
for key, path in PROMPTS.items():
    with open(path, "r", encoding="utf-8") as f:
        prompt_templates[key] = f.read()

# === Helper: clean JSON output ===
def clean_json_output(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```json"):
        raw = raw[7:]
    if raw.startswith("```"):
        raw = raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    return raw.strip()

# === LLM call ===
def llm_generate(prompt: str, temperature=0.0, max_tokens=2500):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=1,
        stream=False
    )
    return completion.choices[0].message.content.strip()

# === Versioning helper ===
def get_versioned_paths(base_trace_id: str):
    trace_dir = os.path.join(OUTPUT_DIR, base_trace_id)
    os.makedirs(trace_dir, exist_ok=True)

    existing = [f for f in os.listdir(trace_dir) if f.startswith("v") and f.endswith(".json")]
    versions = []
    for f in existing:
        try:
            v_num = int(f[1:f.index(".json")])
            versions.append(v_num)
        except:
            pass
    next_version = max(versions, default=0) + 1

    version_file = os.path.join(trace_dir, f"v{next_version}.json")
    latest_file = os.path.join(trace_dir, "latest.json")
    history_file = os.path.join(trace_dir, "history.json")

    return trace_dir, version_file, latest_file, history_file, next_version

# === Step 1: Extract features (unchanged) ===
def extract_features(requirements_text: str, retries=2):
    template = prompt_templates["features"]
    prompt = template.replace("{requirements_text}", requirements_text.strip())

    for attempt in range(retries + 1):
        raw = llm_generate(prompt)
        cleaned = clean_json_output(raw)
        try:
            data = json.loads(cleaned)
            if "modules" in data and "features_by_module" in data:
                return data, True
        except json.JSONDecodeError:
            pass
        if attempt < retries:
            prompt = f"INVALID JSON. Return only valid JSON.\nPrevious:\n{cleaned}\n\nTry again:\n{template.replace('{requirements_text}', requirements_text.strip())}"
    return cleaned, False

# === Step 2: Generate user stories (now receives original requirements) ===
def generate_stories(features_data: dict, original_requirements: str, retries=2):
    template = prompt_templates["stories"]
    input_json = json.dumps(features_data, indent=2)
    prompt = template.replace("{features_json}", input_json) \
                     .replace("{original_requirements}", original_requirements.strip())

    for attempt in range(retries + 1):
        raw = llm_generate(prompt, max_tokens=1500)
        cleaned = clean_json_output(raw)
        try:
            data = json.loads(cleaned)
            if "user_stories" in data and isinstance(data["user_stories"], list):
                return data["user_stories"], True
        except json.JSONDecodeError:
            pass
        if attempt < retries:
            retry_prompt = template.replace("{features_json}", input_json) \
                                   .replace("{original_requirements}", original_requirements.strip())
            prompt = f"Invalid output. Return ONLY JSON with 'user_stories' array.\nPrevious:\n{cleaned}\n\nRetry:\n{retry_prompt}"
    return cleaned, False

# === Step 3: Generate API + DB + open questions (now receives original requirements) ===
def generate_api_db(full_data_so_far: dict, original_requirements: str, retries=2):
    template = prompt_templates["api_db"]
    input_json = json.dumps(full_data_so_far, indent=2)
    prompt = template.replace("{input_json}", input_json) \
                     .replace("{original_requirements}", original_requirements.strip())

    for attempt in range(retries + 1):
        raw = llm_generate(prompt, max_tokens=3000)
        cleaned = clean_json_output(raw)
        try:
            data = json.loads(cleaned)
            required = ["api_endpoints", "db_schema", "open_questions"]
            if all(k in data for k in required):
                return data, True
        except json.JSONDecodeError:
            pass
        if attempt < retries:
            retry_prompt = template.replace("{input_json}", input_json) \
                                   .replace("{original_requirements}", original_requirements.strip())
            prompt = f"Missing keys or invalid JSON. Return FULL JSON only.\nPrevious:\n{cleaned}\n\nRetry:\n{retry_prompt}"
    return cleaned, False

# === Refinement (unchanged for now — can be improved later) ===
def refine_spec(current_spec: dict, refinement_text: str, retries=2):
    refine_path = os.path.join(PROMPTS_DIR, "v1_refine.md")
    if "refine" not in prompt_templates:
        with open(refine_path, "r", encoding="utf-8") as f:
            prompt_templates["refine"] = f.read()

    template = prompt_templates["refine"]
    current_json = json.dumps(current_spec, indent=2)
    prompt = template.replace("{current_spec}", current_json).replace("{refinement_text}", refinement_text.strip())

    for attempt in range(retries + 1):
        raw = llm_generate(prompt, max_tokens=3500)
        cleaned = clean_json_output(raw)
        try:
            data = json.loads(cleaned)
            required = ["modules", "features_by_module", "user_stories", "api_endpoints", "db_schema", "open_questions"]
            if all(k in data for k in required):
                return data, True
        except json.JSONDecodeError:
            pass
        if attempt < retries:
            prompt = f"Invalid or incomplete JSON. Return FULL refined spec.\nPrevious:\n{cleaned}\n\nRetry:\n{template.replace('{current_spec}', current_json).replace('{refinement_text}', refinement_text.strip())}"
    return cleaned, False

# === Final validation ===
def final_validate(data: dict):
    try:
        validate(instance=data, schema=FULL_SCHEMA)
        return True, None
    except ValidationError as e:
        return False, str(e.message)

# === Main pipeline (updated to pass original requirements throughout) ===
def run_pipeline(requirements_text: str, base_trace_id: str = None):
    if base_trace_id is None:
        base_trace_id = f"trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

    trace_dir, version_file, latest_file, history_file, version = get_versioned_paths(base_trace_id)

    print(f"\nPipeline started → {base_trace_id} (v{version})\n")

    # Step 1: Extract features
    features, ok = extract_features(requirements_text)
    if not ok:
        print("Feature extraction failed.")
        return None, base_trace_id
    result = features.copy()

    # Step 2: Generate user stories (pass original text)
    stories, ok = generate_stories(features, requirements_text)
    if not ok:
        print("User stories generation failed.")
        return None, base_trace_id
    result["user_stories"] = stories

    # Step 3: Generate API, DB, open questions (pass original text)
    addition, ok = generate_api_db(result, requirements_text)
    if not ok:
        print("API/DB generation failed.")
        return None, base_trace_id
    result.update(addition)

    # Final schema validation
    valid, err = final_validate(result)
    if not valid:
        print(f"Final validation failed: {err}")

    # Save versioned spec
    spec_data = {
        "version": version,
        "generated_at": datetime.now().isoformat(),
        "trace_id": base_trace_id,
        "type": "initial_generation",
        "spec": result
    }
    with open(version_file, "w", encoding="utf-8") as f:
        json.dump(spec_data, f, indent=2, ensure_ascii=False)

    # Update latest
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump({"current_version": version, "trace_id": base_trace_id, **result}, f, indent=2)

    # Update history
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)
    history.append({
        "version": version,
        "file": f"v{version}.json",
        "generated_at": datetime.now().isoformat(),
        "type": "initial_generation",
        "requirements_summary": requirements_text[:150] + "..." if len(requirements_text) > 150 else requirements_text
    })
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

    print(f"v{version} saved → {version_file}")
    return result, base_trace_id

# === Refinement pipeline (unchanged) ===
def run_refinement(current_spec: dict, refinement_text: str, base_trace_id: str):
    trace_dir, version_file, latest_file, history_file, version = get_versioned_paths(base_trace_id)

    print(f"\nRefinement started → {base_trace_id} (v{version})\n")

    refined, ok = refine_spec(current_spec, refinement_text)
    if not ok:
        print("Refinement failed after retries.")
        return None, base_trace_id

    valid, err = final_validate(refined)
    if not valid:
        print(f"Refined spec validation failed: {err}")

    # Save new version
    spec_data = {
        "version": version,
        "generated_at": datetime.now().isoformat(),
        "parent_version": version - 1,
        "trace_id": base_trace_id,
        "type": "refinement",
        "refinement_instruction": refinement_text,
        "spec": refined
    }
    with open(version_file, "w", encoding="utf-8") as f:
        json.dump(spec_data, f, indent=2, ensure_ascii=False)

    # Update latest
    with open(latest_file, "w", encoding="utf-8") as f:
        json.dump({"current_version": version, "trace_id": base_trace_id, **refined}, f, indent=2)

    # Update history
    history = []
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            history = json.load(f)
    history.append({
        "version": version,
        "file": f"v{version}.json",
        "generated_at": datetime.now().isoformat(),
        "type": "refinement",
        "instruction_summary": refinement_text[:100] + "..." if len(refinement_text) > 100 else refinement_text
    })
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)

    print(f"v{version} saved → {version_file}")
    return refined, base_trace_id

# === Local testing ===
if __name__ == "__main__":
    sample_file = "../../samples/sample1.txt"
    if os.path.exists(sample_file):
        with open(sample_file, "r", encoding="utf-8") as f:
            text = f.read()
        run_pipeline(text)
    else:
        print("Sample file not found.")
