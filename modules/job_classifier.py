# ============================================================
# AI JOB CLASSIFIER
# ============================================================

from modules.skills import extract_skills


# ============================================================
# ROLE SKILL DATABASE
# ============================================================

ROLE_SKILLS = {

    "Software Engineer": [
        "Python",
        "Java",
        "C++",
        "SQL",
        "Git",
        "OOP",
        "Data Structures",
        "Algorithms",
        "Linux"
    ],

    "Backend Developer": [
        "Python",
        "Java",
        "SQL",
        "Git",
        "Docker",
        "AWS",
        "Linux"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Excel",
        "Power BI"
    ],

    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "Python",
        "SQL",
        "Git"
    ],

    "Python Developer": [
        "Python",
        "SQL",
        "Git",
        "Pandas",
        "NumPy",
        "Scikit-learn"
    ]
}


# ============================================================
# ROLE KEYWORDS
# ============================================================

ROLE_KEYWORDS = {

    "Software Engineer": [
        "software",
        "software engineer",
        "developer",
        "programming",
        "application",
        "development",
        "algorithms",
        "data structures"
    ],

    "Backend Developer": [
        "backend",
        "back end",
        "api",
        "server",
        "database",
        "rest",
        "backend developer"
    ],

    "Data Analyst": [
        "data analyst",
        "data analysis",
        "analytics",
        "reporting",
        "dashboard",
        "data",
        "excel",
        "business intelligence"
    ],

    "Web Developer": [
        "web developer",
        "website",
        "frontend",
        "front end",
        "web",
        "html",
        "css",
        "javascript"
    ],

    "Python Developer": [
        "python developer",
        "python",
        "scripting",
        "automation",
        "django",
        "flask"
    ]
}


# ============================================================
# HELPER — NORMALIZE TEXT
# ============================================================

def normalize_text(text):
    """
    Convert any input into normalized lowercase text.
    """

    if text is None:
        return ""

    return str(text).strip().lower()


# ============================================================
# HELPER — NORMALIZE SKILL LIST
# ============================================================

def normalize_skill_list(skills):
    """
    Convert skills into a case-insensitive dictionary.
    """

    if not skills:
        return {}

    result = {}

    for skill in skills:

        skill_text = str(skill).strip()

        if skill_text:

            result[
                skill_text.lower()
            ] = skill_text

    return result


# ============================================================
# JOB ROLE RECOMMENDATIONS
# ============================================================

def get_job_recommendations(resume_text):
    """
    Recommend job roles based on resume skills and keywords.

    Returns a list of dictionaries containing:
        job_role
        score
        confidence
    """

    resume_text_normalized = normalize_text(
        resume_text
    )

    # --------------------------------------------------------
    # Extract resume skills
    # --------------------------------------------------------

    try:

        resume_skills = extract_skills(
            resume_text
        )

    except Exception:

        resume_skills = []


    resume_skill_map = normalize_skill_list(
        resume_skills
    )


    recommendations = []


    # --------------------------------------------------------
    # Calculate role scores
    # --------------------------------------------------------

    for role, required_skills in ROLE_SKILLS.items():

        role_skill_map = normalize_skill_list(
            required_skills
        )

        matched_skill_count = 0


        for skill_key in role_skill_map:

            if skill_key in resume_skill_map:

                matched_skill_count += 1


        # Skill-based score
        if role_skill_map:

            skill_score = (
                matched_skill_count
                / len(role_skill_map)
            ) * 100

        else:

            skill_score = 0.0


        # ----------------------------------------------------
        # Keyword-based score
        # ----------------------------------------------------

        keywords = ROLE_KEYWORDS.get(
            role,
            []
        )

        matched_keywords = 0


        for keyword in keywords:

            if normalize_text(keyword) in resume_text_normalized:

                matched_keywords += 1


        if keywords:

            keyword_score = (
                matched_keywords
                / len(keywords)
            ) * 100

        else:

            keyword_score = 0.0


        # ----------------------------------------------------
        # Combined role score
        # ----------------------------------------------------

        role_score = (
            skill_score * 0.70
            + keyword_score * 0.30
        )


        role_score = max(
            0.0,
            min(
                100.0,
                role_score
            )
        )


        recommendations.append(
            {
                "job_role": role,
                "score": round(
                    role_score,
                    2
                ),
                "confidence": round(
                    role_score,
                    2
                ),
                "matched_skills": [
                    resume_skill_map[key]
                    for key in role_skill_map
                    if key in resume_skill_map
                ],
                "required_skills": list(
                    role_skill_map.values()
                )
            }
        )


    # --------------------------------------------------------
    # Sort by score
    # --------------------------------------------------------

    recommendations.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    return recommendations


# ============================================================
# ROLE-BASED SKILL GAP
# ============================================================

def get_role_skill_gap(resume_text, job_role):
    """
    Compare resume skills against the selected job role.

    Returns:
        {
            "matched_skills": [...],
            "missing_skills": [...]
        }
    """

    # --------------------------------------------------------
    # Validate role
    # --------------------------------------------------------

    if not job_role:

        return {
            "matched_skills": [],
            "missing_skills": []
        }


    selected_role = str(
        job_role
    ).strip()


    # --------------------------------------------------------
    # Find role requirements
    # --------------------------------------------------------

    required_skills = ROLE_SKILLS.get(
        selected_role,
        []
    )


    if not required_skills:

        return {
            "matched_skills": [],
            "missing_skills": []
        }


    # --------------------------------------------------------
    # Extract resume skills
    # --------------------------------------------------------

    try:

        resume_skills = extract_skills(
            resume_text
        )

    except Exception:

        resume_skills = []


    # --------------------------------------------------------
    # Normalize resume skills
    # --------------------------------------------------------

    resume_skill_map = normalize_skill_list(
        resume_skills
    )


    # --------------------------------------------------------
    # Normalize role skills
    # --------------------------------------------------------

    role_skill_map = normalize_skill_list(
        required_skills
    )


    matched_skills = []

    missing_skills = []


    # --------------------------------------------------------
    # Compare skills
    # --------------------------------------------------------

    for skill_key, original_skill in role_skill_map.items():

        if skill_key in resume_skill_map:

            matched_skills.append(
                resume_skill_map[skill_key]
            )

        else:

            missing_skills.append(
                original_skill
            )


    # --------------------------------------------------------
    # Remove duplicates
    # --------------------------------------------------------

    matched_skills = sorted(
        set(matched_skills),
        key=str.lower
    )


    missing_skills = sorted(
        set(missing_skills),
        key=str.lower
    )


    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }


# ============================================================
# MODEL EVALUATION
# ============================================================

def evaluate_model():
    """
    Return information about the rule-based job
    recommendation system.

    These are system metrics, not trained ML accuracy.
    """

    return {
        "model_type": "Skill + Keyword Based Job Classifier",
        "roles_supported": len(
            ROLE_SKILLS
        ),
        "skill_database_size": len(
            set(
                skill
                for skills in ROLE_SKILLS.values()
                for skill in skills
            )
        ),
        "classification_method": (
            "Weighted skill and keyword matching"
        )
    }