import sqlite3

conn = sqlite3.connect("job_screening.db")
cursor = conn.cursor()

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
print("✅ Email invite table created.")
