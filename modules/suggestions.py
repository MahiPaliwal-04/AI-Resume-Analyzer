def generate_suggestions(missing_skills):
    suggestions = []

    if missing_skills:
        for skill in missing_skills:
            suggestions.append(
                f"Consider learning or adding {skill} to your resume "
                "if you have relevant experience."
            )
    else:
        suggestions.append(
            "Your resume covers all recognized skills from the job description."
        )

    return suggestions