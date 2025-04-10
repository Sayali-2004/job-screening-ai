import sqlite3

conn = sqlite3.connect("job_screening.db")
cursor = conn.cursor()

# Add job_id column if it doesn't exist (safe to re-run)
try:
    cursor.execute("ALTER TABLE interview_invites ADD COLUMN job_id INTEGER")
    print("✅ Added job_id column to interview_invites table.")
except sqlite3.OperationalError:
    print("⚠️ job_id column already exists.")

conn.commit()
conn.close()
