import streamlit as st
import sqlite3
import pandas as pd

DB_PATH = "job_screening.db"

def load_data(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

st.set_page_config(page_title="TalentMate AI", layout="wide")

st.title("🤖 TalentMate - AI-Powered Job Screening")

st.sidebar.header("📊 Display Settings")
row_limit = st.sidebar.slider("Rows to show per table", 5, 50, 10)

tabs = st.tabs([
    "📄 Job Descriptions",
    "📁 Candidate Profiles",
    "🧠 Match Scores",
    "✅ Shortlisted Candidates",
    "📬 Interview Invites"
])

# JOB DESCRIPTIONS
with tabs[0]:
    st.subheader("📄 Job Descriptions")
    jobs = load_data("SELECT * FROM job_summary")
    st.dataframe(jobs.head(row_limit))

# CANDIDATES
with tabs[1]:
    st.subheader("📁 Candidate Profiles")
    candidates = load_data("SELECT * FROM candidate_profiles")
    st.dataframe(candidates.head(row_limit))

# MATCH SCORES
with tabs[2]:
    st.subheader("🧠 Match Scores (Top Matches Only)")
    match_scores = load_data("""
        SELECT ms.score, cp.name AS candidate_name, js.title AS job_title, ms.reasoning
        FROM match_scores ms
        JOIN candidate_profiles cp ON ms.candidate_id = cp.candidate_id
        JOIN job_summary js ON ms.job_id = js.job_id
        ORDER BY ms.score DESC
        LIMIT ?
    """, (row_limit,))
    st.dataframe(match_scores)

# SHORTLISTED
with tabs[3]:
    st.subheader("✅ Shortlisted Candidates")
    shortlisted = load_data("""
        SELECT sc.score, cp.name AS candidate_name, js.title AS job_title
        FROM shortlisted_candidates sc
        JOIN candidate_profiles cp ON sc.candidate_id = cp.candidate_id
        JOIN job_summary js ON sc.job_id = js.job_id
        ORDER BY sc.score DESC
        LIMIT ?
    """, (row_limit,))
    st.dataframe(shortlisted)

# INTERVIEW INVITES
with tabs[4]:
    st.subheader("📬 Interview Invitations")
    invites = load_data("""
        SELECT ii.email_text, cp.name AS candidate_name, ii.job_id
        FROM interview_invites ii
        JOIN candidate_profiles cp ON ii.candidate_id = cp.candidate_id
        LIMIT ?
    """, (row_limit,))
    for _, row in invites.iterrows():
        with st.expander(f"📨 {row['candidate_name']} - Job ID: {row['job_id']}"):
            st.markdown(row['email_text'])
            
