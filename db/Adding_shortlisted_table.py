import sqlite3

conn = sqlite3.connect("job_screening.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS shortlisted_candidates (
    candidate_id INTEGER,
    job_id INTEGER,
    score REAL,
    status TEXT
)
""")

conn.commit()
conn.close()
print("✅ Table created")
