import sqlite3
import pandas as pd
import ollama
import json

DB_PATH = "job_screening.db"
CSV_PATH = "job_description.csv"

def load_job_descriptions(csv_path):
    return pd.read_csv(csv_path, encoding="ISO-8859-1")[["Job Title", "Job Description"]]

def extract_from_llm(job_title, job_desc):
    prompt = f"""
You are an AI assistant helping to structure job descriptions for recruitment. Given the following job title and job description, extract these fields in JSON format:
- skills: a list of required technical or soft skills
- experience: short summary like "3+ years in data science"
- education: degree or field required (e.g., "Bachelor's in CS")
- location: if mentioned in the description
Respond ONLY with the JSON.

Job Title: {job_title}
Job Description: {job_desc}
"""

    response = ollama.chat(model='llama3', messages=[
        {"role": "user", "content": prompt}
    ])
    
    try:
        return json.loads(response['message']['content'])
    except Exception as e:
        print(f"❌ Error parsing JSON: {e}")
        print("Response was:", response['message']['content'])
        return None

def save_to_db(job_title, structured_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO job_summary (title, skills, experience, education, location)
        VALUES (?, ?, ?, ?, ?)
    """, (
        job_title,
        ", ".join(structured_data.get("skills", [])),
        structured_data.get("experience", ""),
        structured_data.get("education", ""),
        structured_data.get("location", "")
    ))

    conn.commit()
    conn.close()

def main():
    jobs = load_job_descriptions(CSV_PATH)
    for _, row in jobs.iterrows():
        job_title = row["Job Title"]
        job_desc = row["Job Description"]

        print(f"🔍 Processing: {job_title}")
        structured = extract_from_llm(job_title, job_desc)

        if structured:
            save_to_db(job_title, structured)
            print(f"✅ Saved: {job_title}")
        else:
            print(f"⚠️ Skipped: {job_title}")

if __name__ == "__main__":
    main()
