import os
import json
import uuid
import jsonschema
from jsonschema import validate, ValidationError
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Paths
SCHEMA_PATH = os.path.join("schema", "output_schema.json")
PROMPTS = {
    "features": "prompts/v1_features.md",
    "stories":  "prompts/v1_stories.md",
    "api_db":   "prompts/v1_api_db.md"
}
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load full schema
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    FULL_SCHEMA = json.load(f)

# Load prompts
prompt_templates = {}
for key, path in PROMPTS.items():
    with open(path, "r", encoding="utf-8") as f:
        prompt_templates[key] = f.read()

def clean_json_output(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("```json"): raw = raw[7:]
    if raw.startswith("```"): raw = raw[3:]
    if raw.endswith("```"): raw = raw[:-3]
    return raw.strip()

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

# Step 1
def extract_features(requirements_text: str, retries=2):
    template = prompt_templates["features"]
    prompt = template.replace("{requirements_text}", requirements_text.strip())

    for attempt in range(retries + 1):
        raw = llm_generate(prompt)
        cleaned = clean_json_output(raw)
        try:
            data = json.loads(cleaned)
            if all(k in data for k in ["modules", "features_by_module"]):
                return data, True
        except json.JSONDecodeError:
            pass
        if attempt < retries:
            prompt = f"INVALID JSON OUTPUT. You MUST return only valid JSON.\nPrevious attempt:\n{cleaned}\n\nOriginal task again:\n{template.replace('{requirements_text}', requirements_text.strip())}"
    return cleaned, False

# Step 2
def generate_stories(features_data: dict, retries=2):
    template = prompt_templates["stories"]
    input_json = json.dumps(features_data, indent=2)
    prompt = template.replace("{features_json}", input_json)

    for attempt in range(retries + 1):
        raw = llm_generate(prompt, max_tokens=1500)
        cleaned = clean_json_output(raw)
        try:
            data = json.loads(cleaned)
            if "user_stories" in data and isinstance(data["user_stories"], list) and len(data["user_stories"]) > 0:
                return data["user_stories"], True
        except json.JSONDecodeError:
            pass
        if attempt < retries:
            prompt = f"Previous output was not valid JSON or missing 'user_stories' array.\nPrevious:\n{cleaned}\n\nRetry:\n{template.replace('{features_json}', input_json)}"
    return cleaned, False

# Step 3
def generate_api_db(full_data_so_far: dict, retries=2):
    template = prompt_templates["api_db"]
    input_json = json.dumps(full_data_so_far, indent=2)
    prompt = template.replace("{input_json}", input_json)
    required_keys = ["api_endpoints", "db_schema", "open_questions"]

    for attempt in range(retries + 1):
        raw = llm_generate(prompt, max_tokens=3000)
        cleaned = clean_json_output(raw)
        try:
            data = json.loads(cleaned)
            if all(k in data for k in required_keys):
                return data, True
        except json.JSONDecodeError:
            pass
        if attempt < retries:
            feedback = f"Output invalid or missing keys {required_keys}. RETURN ONLY THE FULL JSON WITH ALL REQUIRED FIELDS."
            prompt = f"{feedback}\n\nPrevious output:\n{cleaned}\n\nFull task again:\n{template.replace('{input_json}', input_json)}"
    return cleaned, False

# Final validation
def final_validate(data: dict):
    try:
        validate(instance=data, schema=FULL_SCHEMA)
        return True, None
    except ValidationError as e:
        return False, str(e.message)

# Main pipeline
def run_pipeline(requirements_text: str, trace_id: str = None):
    if trace_id is None:
        trace_id = f"trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"

    print(f"\nPipeline started → {trace_id}\n")

    # Step 1
    print("1. Extracting modules & features...")
    features, ok = extract_features(requirements_text)
    if not ok:
        print("Features extraction failed.")
        return None, trace_id
    result = features

    # Step 2
    print("2. Generating user stories...")
    stories, ok = generate_stories(features)
    if not ok:
        print("User stories failed.")
        return None, trace_id
    result["user_stories"] = stories

    # Step 3
    print("3. Generating API endpoints + DB schema + open questions...")
    addition, ok = generate_api_db(result)
    if not ok:
        print("API/DB step failed after retries.")
        return None, trace_id

    result.update(addition)

    # Final validation
    valid, err = final_validate(result)
    if not valid:
        print(f"Final schema validation FAILED:\n{err}")
    else:
        print("FULL SPEC GENERATED & VALIDATED SUCCESSFULLY!")

    # Save
    path = os.path.join(OUTPUT_DIR, f"{trace_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Saved → {path}\n")
    return result, trace_id

# === Run on sample ===
if __name__ == "__main__":
    sample_file = "samples/sample1.txt"   # change to test others
    with open(sample_file, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"Running pipeline on: {os.path.basename(sample_file)}\n")
    spec, tid = run_pipeline(text)

    if spec:
        print("DONE! Full valid spec generated.")