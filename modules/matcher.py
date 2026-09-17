from modules.skills import extract_skills


def calculate_match(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    if not job_skills:
        return 0, [], [], resume_skills, job_skills

    matched_skills = []

    for skill in job_skills:
        if skill in resume_skills:
            matched_skills.append(skill)

    missing_skills = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)

    match_percentage = (len(matched_skills) / len(job_skills)) * 100

    return (
        match_percentage,
        matched_skills,
        missing_skills,
        resume_skills,
        job_skills
    )