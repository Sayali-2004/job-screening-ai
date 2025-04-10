import sqlite3
import difflib

DB_PATH = "job_screening.db"

def get_all_jobs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_summary")
    jobs = cursor.fetchall()
    conn.close()
    return jobs

def get_all_candidates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidate_profiles")
    candidates = cursor.fetchall()
    conn.close()
    return candidates

def save_match_score(candidate_id, job_id, score, reasoning):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO match_scores (candidate_id, job_id, score, reasoning)
        VALUES (?, ?, ?, ?)
    """, (candidate_id, job_id, score, reasoning))
    conn.commit()
    conn.close()

def compute_match(job, candidate):
    # Unpack relevant fields
    job_id, title, j_skills, j_exp, j_edu, j_loc = job
    cand_id, name, c_edu, c_exp, c_skills, c_cert, c_achieve, c_stack, c_loc = candidate

    def text_similarity(a, b):
        return difflib.SequenceMatcher(None, str(a).lower(), str(b).lower()).ratio()

    skills_score = text_similarity(j_skills, c_skills) * 40
    exp_score    = text_similarity(j_exp, c_exp) * 20
    edu_score    = text_similarity(j_edu, c_edu) * 20
    tech_score   = text_similarity(j_skills, c_stack) * 10
    cert_score   = text_similarity(j_skills, c_cert) * 10

    total_score = skills_score + exp_score + edu_score + tech_score + cert_score

    reasoning = f"Skills: {skills_score:.1f}, Exp: {exp_score:.1f}, Edu: {edu_score:.1f}, Tech: {tech_score:.1f}, Certs: {cert_score:.1f}"

    return round(total_score, 2), reasoning

def main():
    jobs = get_all_jobs()
    candidates = get_all_candidates()

    for job in jobs:
        for candidate in candidates:
            score, reason = compute_match(job, candidate)
            save_match_score(candidate[0], job[0], score, reason)
            print(f"✅ Match: Candidate {candidate[1]} ↔ Job '{job[1]}' → Score: {score}")

if __name__ == "__main__":
    main()
