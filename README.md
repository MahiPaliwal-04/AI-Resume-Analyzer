# 🤖 AI Resume Analyzer

An AI-powered Resume Analysis and Job Matching application built with Python and Streamlit.

The application analyzes a candidate's resume against a target job description and provides ATS scoring, skill matching, TF-IDF text similarity, missing-skill detection, resume quality analysis, job-role recommendations, and personalized improvement suggestions.

---

## 🚀 Live Demo

### 👉 [Open AI Resume Analyzer](https://ai-resume-analyzer-mahi.streamlit.app/)

Try the deployed application directly in your browser.

---

## 💻 GitHub Repository

### 👉 [View Source Code](https://github.com/MahiPaliwal-04/AI-Resume-Analyzer)

---

## ✨ Key Features

- 📄 PDF Resume Parsing
- 🧠 Automated Technical Skill Extraction
- 🎯 Job Description Skill Matching
- 📊 ATS Compatibility Scoring
- 🔎 TF-IDF Text Similarity
- 📌 Missing Skill Detection
- 📝 Resume Quality Analysis
- 💡 Personalized Resume Suggestions
- 👔 Recruiter-Style Recommendations
- 🎯 AI Job Role Recommendations
- 🧩 Role-Based Skill Gap Analysis
- 📈 Resume Optimization Report
- 🏆 Final AI Resume Assessment

---

## 🧠 AI / ML Techniques

### 1. TF-IDF

TF-IDF is used to represent resume and job-description text numerically.

Cosine similarity is then used to measure textual overlap between the two documents.

### 2. Skill-Based Matching

Recognized technical skills are extracted from both the resume and job description.

The system compares the detected skills and calculates the percentage of matching skills.

### 3. ATS Scoring

The ATS analyzer combines multiple signals:

- Keyword Match — 40%
- Skill Match — 35%
- Resume Quality — 25%

### 4. Job Role Classification

The system uses weighted skill and keyword matching to calculate role-match scores for supported job roles.

### 5. Resume Quality Analysis

The analyzer checks factors such as:

- Resume length
- Email information
- Phone number
- Education
- Skills
- Projects
- Experience
- Action-oriented language

---

## 🔄 Analysis Pipeline

```text
Resume PDF
    ↓
Text Extraction
    ↓
Skill Extraction
    ↓
Resume Quality Analysis
    ↓
Job Description Analysis
    ↓
Skill Matching
    ↓
TF-IDF Similarity
    ↓
ATS Scoring
    ↓
Job Role Recommendation
    ↓
Role-Based Skill Gap
    ↓
Resume Optimization
    ↓
Final AI Assessment