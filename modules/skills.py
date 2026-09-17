SKILLS = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "NLP",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Streamlit",
    "Git",
    "GitHub",
    "AWS",
    "Docker"
]


def extract_skills(resume_text):
    found_skills = []

    resume_text_lower = resume_text.lower()

    for skill in SKILLS:
        if skill.lower() in resume_text_lower:
            found_skills.append(skill)

    return found_skills