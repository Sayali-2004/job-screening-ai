import sqlite3

DB_PATH = "job_screening.db"
SHORTLIST_THRESHOLD = 30.0  # You can adjust this

def get_high_matches():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT candidate_id, job_id, score FROM match_scores
        WHERE score >= ?
    """, (SHORTLIST_THRESHOLD,))
    results = cursor.fetchall()
    conn.close()
    return results

def save_shortlisted(candidate_id, job_id, score):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO shortlisted_candidates (candidate_id, job_id, score, status)
        VALUES (?, ?, ?, ?)
    """, (candidate_id, job_id, score, "Shortlisted"))
    conn.commit()
    conn.close()

def main():
    matches = get_high_matches()
    if not matches:
        print("⚠️ No candidates matched the threshold.")
        return

    for match in matches:
        candidate_id, job_id, score = match
        save_shortlisted(candidate_id, job_id, score)
        print(f"✅ Shortlisted Candidate {candidate_id} for Job {job_id} → Score: {score}")

if __name__ == "__main__":
    main()
