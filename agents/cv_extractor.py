import os
import sqlite3
import ollama
import json
import re
import PyPDF2

DB_PATH = "job_screening.db"
RESUME_FOLDER = "data/resumes"
MODEL = "llama2"  # or "llama2" depending on your setup

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

def clean_llm_output_to_json(raw_output):
    try:
        json_str = re.search(r"\{[\s\S]*\}", raw_output).group(0)
        return json.loads(json_str)
    except Exception as e:
        print("❌ Regex/JSON parsing failed:", e)
        return None

def extract_candidate_data_with_llm(resume_text):
    prompt = f"""
You are a resume parser AI. Extract the following fields from the resume in valid JSON format:

- name
- education
- work_experience
- skills (as a list)
- certifications
- achievements
- tech_stack (as a list)
- location (if available)

Respond ONLY with clean JSON. Do NOT include explanations, markdown, or text outside the JSON.

Resume Text:
{resume_text}
"""
    response = ollama.chat(model=MODEL, messages=[
        {"role": "user", "content": prompt}
    ])
    
    raw_output = response['message']['content']
    print("🧾 LLM Raw Response:\n", raw_output)
    return clean_llm_output_to_json(raw_output)

def to_string(value):
    if isinstance(value, list):
        # Flatten list of dicts or convert to readable string
        flattened = []
        for item in value:
            if isinstance(item, dict):
                flattened.append(", ".join([str(v) for v in item.values()]))
            else:
                flattened.append(str(item))
        return ", ".join(flattened)
    elif isinstance(value, dict):
        return json.dumps(value)
    else:
        return str(value) if value is not None else ""


def save_to_db(candidate):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO candidate_profiles (
            name, education, experience, skills,
            certifications, achievements, tech_stack, location
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        to_string(candidate.get("name")),
        to_string(candidate.get("education")),
        to_string(candidate.get("work_experience")),
        to_string(candidate.get("skills")),
        to_string(candidate.get("certifications")),
        to_string(candidate.get("achievements")),
        to_string(candidate.get("tech_stack")),
        to_string(candidate.get("location"))
    ))

    conn.commit()
    conn.close()

def main():
    files = [f for f in os.listdir(RESUME_FOLDER) if f.endswith(".pdf")]
    for filename in files:
        file_path = os.path.join(RESUME_FOLDER, filename)
        print(f"\n📄 Processing: {filename}")

        resume_text = extract_text_from_pdf(file_path)
        structured_data = extract_candidate_data_with_llm(resume_text)

        if structured_data:
            save_to_db(structured_data)
            print(f"✅ Saved to DB: {structured_data.get('name', 'Unknown')}")
        else:
            print(f"⚠️ Skipped: {filename} (JSON issue)")

if __name__ == "__main__":
    main()
