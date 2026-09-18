# 🤖 AI Resume Analyzer

An AI-powered Resume Analysis and Job Matching application built with Python and Streamlit.

The system analyzes a candidate's resume against a given job description and provides ATS scoring, skill matching, TF-IDF similarity, missing skill detection, resume quality analysis, job-role recommendations, and personalized resume improvement suggestions.

---

## 🚀 Live Demo

### 👉 [OPEN AI RESUME ANALYZER](https://ai-resume-analyzer-mahi.streamlit.app/)

Try the fully deployed application directly in your browser.

---

## 💻 GitHub Repository

👉 [View Source Code](https://github.com/MahiPaliwal-04/AI-Resume-Analyzer)

---

## 📸 Project Screenshots

### 🏠 Dashboard

![Dashboard](screenshots/dashboard.png)

### 📊 Resume & Job Matching Analysis

![Matching Analysis](screenshots/matching-analysis.png)

### 💼 AI Job Role Recommendations

![Job Recommendations](screenshots/job-recommendations.png)

### 📋 Resume Optimization Report

![Optimization Report](screenshots/optimization-report.png)

---

## ✨ Key Features

- 📄 PDF Resume Upload and Text Extraction
- 🧠 Resume Skill Detection
- 🎯 Job Description Matching
- 📊 TF-IDF Based Text Similarity
- 🤖 ATS Score Calculation
- 📋 ATS Score Breakdown
- 🔍 Missing Skill Detection
- 📈 Resume Quality Analysis
- 🔑 Keyword Analysis
- 💼 AI Job Role Recommendations
- 🧩 Role-Based Skill Gap Analysis
- 💡 Personalized Resume Improvement Suggestions
- 📑 Resume Optimization Report
- ⚡ Quick Action Plan
- 📊 Final AI Resume Assessment
- 🌐 Interactive Streamlit Web Interface

---

## 🧠 AI & Machine Learning Techniques

### TF-IDF

Term Frequency-Inverse Document Frequency is used to convert resume and job-description text into numerical feature vectors.

### Cosine Similarity

Cosine similarity is used to measure the similarity between the resume and job description.

### Skill Matching

The system extracts recognized technical skills from the resume and job description to identify matched and missing skills.

### ATS Analysis

An ATS-style scoring system evaluates important resume factors such as:

- Resume–Job Description similarity
- Skill matching
- Keywords
- Resume structure
- Relevant sections

### Job Role Recommendation

The application analyzes resume content and provides relevant job-role recommendations based on detected skills and resume information.

---

## 🔄 Analysis Pipeline

```text
Resume PDF
    ↓
Text Extraction
    ↓
Resume Parsing
    ↓
Skill Detection
    ↓
Job Description Input
    ↓
TF-IDF Vectorization
    ↓
Cosine Similarity
    ↓
Skill Matching
    ↓
ATS Scoring
    ↓
Missing Skill Detection
    ↓
Resume Quality Analysis
    ↓
Job Role Recommendations
    ↓
Skill Gap Analysis
    ↓
Personalized Suggestions
    ↓
Final Resume Assessment