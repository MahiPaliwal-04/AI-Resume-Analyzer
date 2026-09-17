import re


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_text(text):
    """
    Convert text into a normalized format for comparison.
    """

    if not text:
        return ""

    text = text.lower()

    # Keep letters, numbers, +, #, ., spaces and -
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# STOPWORDS
# ============================================================

STOPWORDS = {
    "the",
    "and",
    "for",
    "are",
    "with",
    "this",
    "that",
    "from",
    "your",
    "you",
    "our",
    "has",
    "have",
    "will",
    "looking",
    "required",
    "include",
    "into",
    "using",
    "use",
    "used",
    "job",
    "role",
    "work",
    "working",
    "candidate",
    "experience",
    "skills",
    "skill",
    "years",
    "year",
    "ability",
    "strong",
    "good",
    "knowledge",
    "team",
    "developer",
    "development",
    "responsibilities",
    "requirements",
    "preferred",
    "must",
    "should",
    "who",
    "what",
    "where",
    "when",
    "how",
    "their",
    "they",
    "them",
    "we",
    "an",
    "a",
    "to",
    "of",
    "in",
    "on",
    "at",
    "is",
    "be",
    "as",
    "or",
    "by",
    "can",
    "do",
    "does",
    "also",
    "such",
    "within",
    "through",
    "than",
    "more",
    "least",
    "etc",
}


# ============================================================
# KEYWORD EXTRACTION
# ============================================================

def extract_meaningful_keywords(text):
    """
    Extract meaningful keywords while removing
    common English stopwords.
    """

    if not text:
        return set()

    words = set(text.split())

    meaningful_words = {
        word
        for word in words
        if len(word) >= 3
        and word not in STOPWORDS
    }

    return meaningful_words


# ============================================================
# KEYWORD MATCHING
# ============================================================

def calculate_keyword_match(resume_text, job_description):
    """
    Calculate meaningful keyword overlap between
    resume and job description.

    Returns:
        score,
        matched_keywords,
        missing_keywords
    """

    resume_text = clean_text(resume_text)
    job_description = clean_text(job_description)

    if not resume_text or not job_description:
        return 0.0, [], []

    resume_words = extract_meaningful_keywords(resume_text)
    jd_words = extract_meaningful_keywords(job_description)

    if not jd_words:
        return 0.0, [], []

    matched_keywords = sorted(
        resume_words.intersection(jd_words)
    )

    missing_keywords = sorted(
        jd_words.difference(resume_words)
    )

    score = (
        len(matched_keywords) /
        len(jd_words)
    ) * 100

    return (
        round(score, 2),
        matched_keywords,
        missing_keywords
    )


# ============================================================
# SKILL MATCHING
# ============================================================

def calculate_skill_match(resume_skills, required_skills):
    """
    Compare detected resume skills with
    required job skills.

    Returns:
        score,
        matched_skills,
        missing_skills
    """

    if not required_skills:
        return 0.0, [], []

    resume_skills = {
        skill.strip().lower()
        for skill in resume_skills
        if skill and skill.strip()
    }

    required_skills = {
        skill.strip().lower()
        for skill in required_skills
        if skill and skill.strip()
    }

    if not required_skills:
        return 0.0, [], []

    matched_skills = sorted(
        resume_skills.intersection(required_skills)
    )

    missing_skills = sorted(
        required_skills.difference(resume_skills)
    )

    score = (
        len(matched_skills) /
        len(required_skills)
    ) * 100

    return (
        round(score, 2),
        matched_skills,
        missing_skills
    )


# ============================================================
# RESUME QUALITY ANALYZER
# ============================================================

def calculate_resume_quality(resume_text):
    """
    Basic resume quality analysis.

    Checks:
    - Resume length
    - Email
    - Phone number
    - Important sections
    - Action verbs

    Returns:
        quality_score,
        feedback
    """

    if not resume_text:
        return 0.0, [
            "Resume text could not be analyzed."
        ]

    text = clean_text(resume_text)

    score = 0
    feedback = []

    # --------------------------------------------------------
    # 1. RESUME LENGTH
    # --------------------------------------------------------

    word_count = len(text.split())

    if word_count >= 400:
        score += 20

    elif word_count >= 250:
        score += 15

    elif word_count >= 150:
        score += 10

    else:
        feedback.append(
            "Resume appears too short."
        )

    # --------------------------------------------------------
    # 2. EMAIL
    # --------------------------------------------------------

    email_pattern = (
        r"\b[A-Za-z0-9._%+-]+"
        r"@[A-Za-z0-9.-]+\."
        r"[A-Za-z]{2,}\b"
    )

    if re.search(email_pattern, resume_text):
        score += 15

    else:
        feedback.append(
            "Email address not detected."
        )

    # --------------------------------------------------------
    # 3. PHONE NUMBER
    # --------------------------------------------------------

    phone_patterns = [
        r"\b(?:\+91[-.\s]?)?[6-9]\d{9}\b",
        r"\b(?:\+?\d{1,3}[-.\s]?)?\d{10}\b",
    ]

    phone_found = any(
        re.search(pattern, resume_text)
        for pattern in phone_patterns
    )

    if phone_found:
        score += 15

    else:
        feedback.append(
            "Phone number not detected."
        )

    # --------------------------------------------------------
    # 4. IMPORTANT RESUME SECTIONS
    # --------------------------------------------------------

    sections = {
        "experience": [
            "experience",
            "work experience",
            "employment",
            "professional experience",
        ],

        "education": [
            "education",
            "academic",
            "qualification",
        ],

        "skills": [
            "skills",
            "technical skills",
            "technologies",
            "technical expertise",
        ],

        "projects": [
            "projects",
            "academic projects",
            "personal projects",
            "project experience",
        ],
    }

    section_score = 0

    for section, keywords in sections.items():

        if any(
            keyword in text
            for keyword in keywords
        ):
            section_score += 7.5

        else:
            feedback.append(
                f"{section.title()} section "
                f"not clearly detected."
            )

    score += section_score

    # --------------------------------------------------------
    # 5. ACTION VERBS
    # --------------------------------------------------------

    action_verbs = [
        "developed",
        "built",
        "created",
        "implemented",
        "designed",
        "optimized",
        "analyzed",
        "automated",
        "engineered",
        "deployed",
        "managed",
        "improved",
        "integrated",
        "trained",
        "evaluated",
        "tested",
        "configured",
        "maintained",
        "led",
        "delivered",
    ]

    found_action_verbs = []

    for verb in action_verbs:

        if re.search(
            r"\b" + re.escape(verb) + r"\b",
            text
        ):
            found_action_verbs.append(verb)

    if len(found_action_verbs) >= 4:
        score += 15

    elif len(found_action_verbs) >= 2:
        score += 10

    elif len(found_action_verbs) >= 1:
        score += 5

    else:
        feedback.append(
            "Add more action-oriented words such as "
            "developed, implemented, optimized, "
            "deployed, etc."
        )

    return (
        round(min(score, 100), 2),
        feedback
    )


# ============================================================
# ATS SCORE
# ============================================================

def calculate_ats_score(
    resume_text,
    job_description,
    resume_skills=None,
    required_skills=None
):
    """
    Calculate the overall ATS score.

    Weighted scoring:

    Keyword Match   = 40%
    Skill Match     = 35%
    Resume Quality  = 25%

    Returns a dictionary containing
    complete ATS analysis.
    """

    if resume_skills is None:
        resume_skills = []

    if required_skills is None:
        required_skills = []

    # --------------------------------------------------------
    # KEYWORD SCORE
    # --------------------------------------------------------

    (
        keyword_score,
        matched_keywords,
        missing_keywords
    ) = calculate_keyword_match(
        resume_text,
        job_description
    )

    # --------------------------------------------------------
    # SKILL SCORE
    # --------------------------------------------------------

    (
        skill_score,
        matched_skills,
        missing_skills
    ) = calculate_skill_match(
        resume_skills,
        required_skills
    )

    # --------------------------------------------------------
    # RESUME QUALITY SCORE
    # --------------------------------------------------------

    (
        quality_score,
        quality_feedback
    ) = calculate_resume_quality(
        resume_text
    )

    # --------------------------------------------------------
    # FINAL ATS SCORE
    # --------------------------------------------------------

    final_score = (
        keyword_score * 0.40
        + skill_score * 0.35
        + quality_score * 0.25
    )

    return {
        "ats_score": round(
            final_score,
            2
        ),

        "keyword_match": round(
            keyword_score,
            2
        ),

        "skill_match": round(
            skill_score,
            2
        ),

        "resume_quality": round(
            quality_score,
            2
        ),

        "matched_keywords": matched_keywords,

        "missing_keywords": missing_keywords,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "quality_feedback": quality_feedback,
    }