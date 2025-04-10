import sqlite3
import ollama

DB_PATH = "job_screening.db"
MODEL = "llama2"  # Or "llama2"

def get_shortlisted_candidates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sc.candidate_id, sc.job_id, cp.name, cp.skills, cp.experience
        FROM shortlisted_candidates sc
        JOIN candidate_profiles cp ON sc.candidate_id = cp.candidate_id
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def generate_email(name, job_id, skills, experience):
    prompt = f"""
You are an HR assistant. Generate a friendly and professional interview invitation email for the candidate named {name}, who is shortlisted for Job ID {job_id}.

Mention their relevant skills: {skills}
Mention their experience: {experience}
Invite them to choose an interview slot.

Keep the tone warm, concise, and clear.
Return only the email body.
"""

    response = ollama.chat(model=MODEL, messages=[
        {"role": "user", "content": prompt}
    ])

    return response["message"]["content"]

def save_email(candidate_id, job_id, email_text):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO interview_invites (candidate_id, job_id, email_text, status)
        VALUES (?, ?, ?, ?)
    """, (candidate_id, job_id, email_text, "Pending"))
    conn.commit()
    conn.close()

def main():
    candidates = get_shortlisted_candidates()
    if not candidates:
        print("⚠️ No shortlisted candidates found.")
        return

    for cand_id, job_id, name, skills, exp in candidates:
        print(f"📨 Generating email for {name} (Candidate ID: {cand_id})...")
        email_text = generate_email(name, job_id, skills, exp)
        save_email(cand_id, job_id, email_text)
        print("✅ Email saved.\n")

if __name__ == "__main__":
    main()
