import sqlite3

def setup_database():
    conn = sqlite3.connect("job_screening.db")
    cursor = conn.cursor()

    # Job Summary Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_summary (
        job_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        skills TEXT,
        experience TEXT,
        education TEXT,
        location TEXT
    )
    """)

    # Candidate Profiles with expanded fields
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidate_profiles (
        candidate_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        education TEXT,
        experience TEXT,
        skills TEXT,
        certifications TEXT,
        achievements TEXT,
        tech_stack TEXT,
        location TEXT
    )
    """)

    # Match Scores Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS match_scores (
        candidate_id INTEGER,
        job_id INTEGER,
        score REAL,
        reasoning TEXT
    )
    """)
    
    # Shortlisted Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shortlisted_candidates (
        candidate_id INTEGER,
        job_id INTEGER,
        score REAL,
        status TEXT
    )
    """)

    # Interview Invites Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_invites (
        candidate_id INTEGER,
        job_id INTEGER,
        email_text TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Database setup complete!")

if __name__ == "__main__":
    setup_database()
    
