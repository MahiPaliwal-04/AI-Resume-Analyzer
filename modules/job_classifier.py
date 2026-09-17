
import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# ===================================
# PROJECT PATHS
# ===================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "job_roles.csv"
)


# ===================================
# LOAD DATASET
# ===================================

def load_job_data():

    if not os.path.exists(DATA_PATH):

        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    if (
        "job_role" not in df.columns
        or "skills" not in df.columns
    ):

        raise ValueError(
            "CSV must contain 'job_role' and 'skills' columns."
        )

    return df


# ===================================
# TRAIN ML MODEL
# ===================================

def train_model():

    df = load_job_data()

    X = df["skills"].fillna("")
    y = df["job_role"]

    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )

    X_vectorized = vectorizer.fit_transform(
        X
    )

    model = LogisticRegression(
        max_iter=2000
    )

    model.fit(
        X_vectorized,
        y
    )

    return model, vectorizer


# ===================================
# PREDICT SINGLE JOB ROLE
# ===================================

def predict_job_role(resume_skills):

    if not resume_skills:

        return None

    model, vectorizer = train_model()

    if isinstance(resume_skills, list):

        resume_text = ", ".join(
            resume_skills
        )

    else:

        resume_text = str(
            resume_skills
        )

    resume_vector = vectorizer.transform(
        [resume_text]
    )

    prediction = model.predict(
        resume_vector
    )[0]

    return prediction


# ===================================
# GET MULTIPLE JOB RECOMMENDATIONS
# ===================================

def get_job_recommendations(
    resume_skills,
    top_n=5
):

    if not resume_skills:

        return []

    model, vectorizer = train_model()

    if isinstance(resume_skills, list):

        resume_text = ", ".join(
            resume_skills
        )

    else:

        resume_text = str(
            resume_skills
        )

    resume_vector = vectorizer.transform(
        [resume_text]
    )

    probabilities = model.predict_proba(
        resume_vector
    )[0]

    classes = model.classes_

    results = sorted(
        zip(
            classes,
            probabilities
        ),
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = []

    for role, probability in results[:top_n]:

        recommendations.append(
            {
                "job_role": role,
                "confidence": round(
                    float(probability) * 100,
                    2
                )
            }
        )

    return recommendations


# ===================================
# GET SKILLS FOR A JOB ROLE
# ===================================

def get_role_skills(job_role):

    df = load_job_data()

    role_data = df[
        df["job_role"].str.strip().str.lower()
        == job_role.strip().lower()
    ]

    if role_data.empty:

        return []

    role_skills = set()

    for skills in role_data["skills"].fillna(""):

        for skill in str(skills).split(","):

            skill = skill.strip()

            if skill:

                role_skills.add(
                    skill
                )

    return sorted(
        role_skills,
        key=str.lower
    )


# ===================================
# GET ROLE SKILL GAP
# ===================================

def get_role_skill_gap(
    resume_skills,
    job_role
):

    if not resume_skills or not job_role:

        return {
            "role": job_role,
            "required_skills": [],
            "matched_skills": [],
            "missing_skills": []
        }

    required_skills = get_role_skills(
        job_role
    )

    # Normalize resume skills
    resume_skill_map = {
        str(skill).strip().lower(): str(skill).strip()
        for skill in resume_skills
        if str(skill).strip()
    }

    matched_skills = []
    missing_skills = []

    for required_skill in required_skills:

        required_normalized = (
            required_skill.strip().lower()
        )

        if required_normalized in resume_skill_map:

            matched_skills.append(
                required_skill
            )

        else:

            missing_skills.append(
                required_skill
            )

    return {
        "role": job_role,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }


# ===================================
# EVALUATE ML MODEL
# ===================================

def evaluate_model():

    df = load_job_data()

    X = df["skills"].fillna("")
    y = df["job_role"]

    # Split RAW text data first
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=42,
        stratify=y
    )

    # Fit TF-IDF ONLY on training data
    vectorizer = TfidfVectorizer(
        lowercase=True,
        ngram_range=(1, 2)
    )

    X_train_vectorized = vectorizer.fit_transform(
        X_train
    )

    X_test_vectorized = vectorizer.transform(
        X_test
    )

    # Train classifier
    model = LogisticRegression(
        max_iter=2000
    )

    model.fit(
        X_train_vectorized,
        y_train
    )

    # Predict test data
    y_pred = model.predict(
        X_test_vectorized
    )

    # Accuracy
    accuracy = accuracy_score(
        y_test,
        y_pred
    )

    # Classification report
    report = classification_report(
        y_test,
        y_pred,
        zero_division=0
    )

    return accuracy, report

