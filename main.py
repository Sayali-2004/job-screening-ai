import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "job_screening.db"

def load_data(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

st.set_page_config(page_title="TalentMate - Job Screening AI", layout="wide")

st.title("🤖 TalentMate - AI-Powered Job Screening Dashboard")

tabs = st.tabs([
    "📄 Job Descriptions", 
    "📁 Candidate Profiles", 
    "🧠 Match Scores", 
    "✅ Shortlisted", 
    "📬 Interview Invites"
])

# 1. Job Descriptions
with tabs[0]:
    st.subheader("📄 Job Descriptions")
    jobs = load_data("SELECT * FROM job_summary")
    st.dataframe(jobs)

# 2. Candidate Profiles
with tabs[1]:
    st.subheader("📁 Candidate Profiles")
    candidates = load_data("SELECT * FROM candidate_profiles")
    st.dataframe(candidates)

# 3. Match Scores
with tabs[2]:
    st.subheader("🧠 Match Scores")
    match_scores = load_data("""
        SELECT ms.*, cp.name AS candidate_name, js.title AS job_title
        FROM match_scores ms
        JOIN candidate_profiles cp ON ms.candidate_id = cp.candidate_id
        JOIN job_summary js ON ms.job_id = js.job_id
        ORDER BY score DESC
    """)
    st.dataframe(match_scores)

# 4. Shortlisted
with tabs[3]:
    st.subheader("✅ Shortlisted Candidates")
    shortlisted = load_data("""
        SELECT sc.*, cp.name AS candidate_name, js.title AS job_title
        FROM shortlisted_candidates sc
        JOIN candidate_profiles cp ON sc.candidate_id = cp.candidate_id
        JOIN job_summary js ON sc.job_id = js.job_id
        ORDER BY score DESC
    """)
    st.dataframe(shortlisted)

# 5. Interview Invites
with tabs[4]:
    st.subheader("📬 Interview Invitations")
    invites = load_data("""
        SELECT ii.*, cp.name AS candidate_name
        FROM interview_invites ii
        JOIN candidate_profiles cp ON ii.candidate_id = cp.candidate_id
    """)
    for _, row in invites.iterrows():
        with st.expander(f"📨 {row['candidate_name']} - Job ID: {row['job_id']}"):
            st.markdown(row['email_text'])
