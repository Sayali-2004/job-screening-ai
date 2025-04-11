# job-screening-ai
We developed TalentMate, a multi-agent AI system that automates end-to-end job application screening.

# 🧠 TalentMate: AI-Powered Job Screening System

A multi-agent AI system that automates the entire job screening process — from job description parsing to personalized interview invitations. Built for the Accenture Hackathon 2025 🚀

---

## 📌 Problem Statement

Recruiters face inefficiencies in manually screening hundreds of resumes per role. This leads to:
- Time delays in shortlisting
- Human bias
- Missed top candidates

---

## 💡 Our Solution

**TalentMate** uses a multi-agent system to automate and optimize job screening:

### 🧩 Agents in Action
1. **JD Summarizer Agent**
   - Parses job descriptions (CSV)
   - Extracts key skills, experience, education, and location

2. **CV Extractor Agent**
   - Parses resumes from PDFs
   - Extracts structured profile data using LLM

3. **Matching Agent**
   - Calculates match scores between candidates and job roles
   - Uses weighted similarity logic (skills, experience, etc.)

4. **Shortlisting Agent**
   - Filters top candidates based on score threshold

5. **Interview Invite Agent**
   - Generates personalized interview invitations using AI

---

## 🛠️ Tech Stack

| Area               | Tools Used                           |
|--------------------|--------------------------------------|
| Language Models     | Ollama (LLMs: `mistral`, `llama2`)   |
| PDF Parsing         | PyPDF2                               |
| Data Processing     | Python, Pandas                       |
| Memory & Storage    | SQLite                               |
| Matching Logic      | difflib (text similarity)            |
| Orchestration       | Python scripts via `main.py`         |

---

## ⚙️ How to Run

### ✅ Clone the Repo

```bash
git clone https://github.com/yourusername/talentmate-ai.git
cd talentmate-ai

---

### ✅ Set Up Your Environment
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

---

### ✅ Make Sure Ollama Is Running
```bash
ollama run mistral

---

### ✅ Run the Full Project
```bash
python main.py
streamlit streamlit_app.py



