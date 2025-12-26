import os
import json
import glob
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env at project root
load_dotenv()  # Looks for .env in current working directory (project root)

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Prompt file and schema subset (for basic validation)
PROMPT_FILE = "prompts/v1_features.md"

# Simple schema check (we'll do light validation here; full JSON Schema later)
REQUIRED_KEYS = ["modules", "features_by_module"]

def load_prompt():
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        return f.read()

def extract_features(requirements_text):
    prompt_template = load_prompt()
    full_prompt = prompt_template.replace("{requirements_text}", requirements_text.strip())

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # Recommended stable model; change if you prefer another
            # You can also try: "llama3-70b-8192", "llama3-8b-8192", etc.
            messages=[
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            temperature=0.0,        # Deterministic for extraction
            max_tokens=1000,
            top_p=1,
            stream=False            # We'll use non-streaming for simplicity
        )

        raw_output = completion.choices[0].message.content.strip()

        # Clean common markdown wrappers
        if raw_output.startswith("```json"):
            raw_output = raw_output[7:]
        if raw_output.startswith("```"):
            raw_output = raw_output[3:]
        if raw_output.endswith("```"):
            raw_output = raw_output[:-3]
        raw_output = raw_output.strip()

        # Parse JSON
        data = json.loads(raw_output)

        # Basic structure validation
        for key in REQUIRED_KEYS:
            if key not in data:
                raise ValueError(f"Missing required key: {key}")

        if not isinstance(data["modules"], list):
            raise ValueError("modules must be a list")
        if not isinstance(data["features_by_module"], dict):
            raise ValueError("features_by_module must be a dict")

        return data, True, None

    except json.JSONDecodeError as e:
        return raw_output, False, f"JSON parsing error: {str(e)}"
    except Exception as e:
        return raw_output if 'raw_output' in locals() else "", False, f"Error: {str(e)}"

# === Test Harness ===
if __name__ == "__main__":
    samples_dir = "samples"
    output_dir = "outputs/day9"
    os.makedirs(output_dir, exist_ok=True)

    sample_files = glob.glob(os.path.join(samples_dir, "*.txt"))
    if not sample_files:
        print("No samples found in samples/ folder. Add some .txt files first.")
        exit(1)

    results = []
    print(f"Found {len(sample_files)} samples. Starting extraction...\n")

    for sample_file in sample_files:
        filename = os.path.basename(sample_file)
        print(f"Processing {filename}...")

        with open(sample_file, "r", encoding="utf-8") as f:
            requirements_text = f.read()

        extracted_data, success, error = extract_features(requirements_text)

        result = {
            "sample": filename,
            "success": success,
            "error": error,
            "output": extracted_data if success else None,
            "raw_output": extracted_data if not success else None  # Save raw on failure
        }
        results.append(result)

        status = "SUCCESS" if success else "FAILED"
        print(f"  -> {status}")
        if not success:
            print(f"     Reason: {error}\n")

    # Save full results
    results_path = os.path.join(output_dir, "results.json")
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    # Summary
    successful = sum(1 for r in results if r["success"])
    print("\n" + "="*50)
    print(f"TEST HARNESS COMPLETE")
    print(f"Successful: {successful}/{len(results)}")
    print(f"Results saved to: {results_path}")
    print("="*50)

    if successful == len(results):
        print("Day 9 extraction step is reliable! Ready for Day 10.")