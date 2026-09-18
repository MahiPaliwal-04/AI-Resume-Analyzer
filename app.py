import streamlit as st

from modules.parser import extract_text_from_pdf
from modules.skills import extract_skills
from modules.matcher import calculate_match
from modules.suggestions import generate_suggestions
from modules.similarity import calculate_similarity

from modules.job_classifier import (
    get_job_recommendations,
    get_role_skill_gap,
    evaluate_model
)

from modules.ats_scorer import calculate_ats_score


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title("🤖 AI Resume Analyzer")

st.markdown(
    "### Smart Resume Analysis • ATS Scoring • Job Matching • AI Career Insights"
)

st.info(
    "Upload your resume and paste a job description to get "
    "an AI-powered analysis of your resume."
)


# ============================================================
# FEATURE OVERVIEW
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📄 Resume Parsing", "AI")

with col2:
    st.metric("🎯 Job Matching", "TF-IDF")

with col3:
    st.metric("📊 ATS Analysis", "Smart")

with col4:
    st.metric("💼 Career Insights", "AI")


st.divider()


# ============================================================
# MODEL INFORMATION
# ============================================================

with st.expander("🧠 View AI Model Information"):

    st.write(
        "This project combines resume parsing, skill extraction, "
        "TF-IDF similarity, ATS analysis and job-role classification."
    )

    try:

        evaluation = evaluate_model()

        if isinstance(evaluation, dict):

            metric_cols = st.columns(
                min(len(evaluation), 4)
            )

            for index, (key, value) in enumerate(
                evaluation.items()
            ):

                with metric_cols[index % len(metric_cols)]:

                    if isinstance(value, float):

                        st.metric(
                            key.replace("_", " ").title(),
                            f"{value:.2f}"
                        )

                    else:

                        st.metric(
                            key.replace("_", " ").title(),
                            str(value)
                        )

        elif evaluation is not None:

            st.write(evaluation)

        else:

            st.caption(
                "Model evaluation information is currently unavailable."
            )

    except Exception as e:

        st.caption(
            f"Model evaluation information is currently unavailable: {e}"
        )


st.divider()


# ============================================================
# INPUT SECTION
# ============================================================

st.header("📥 Resume & Job Description")

input_col1, input_col2 = st.columns(2)


# ============================================================
# RESUME UPLOAD
# ============================================================

with input_col1:

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload your resume in PDF format",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(
            f"Uploaded: {uploaded_file.name}"
        )


# ============================================================
# JOB DESCRIPTION
# ============================================================

with input_col2:

    st.subheader("💼 Target Job")

    job_description = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Python Developer with experience "
            "in Machine Learning, SQL, Pandas, NumPy, Scikit-learn "
            "and Git."
        )
    )


st.divider()


# ============================================================
# ANALYZE BUTTON
# ============================================================

analyze_button = st.button(
    "🚀 Analyze My Resume",
    type="primary",
    use_container_width=True
)


# ============================================================
# MAIN ANALYSIS
# ============================================================

if analyze_button:

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if uploaded_file is None:

        st.warning(
            "⚠️ Please upload your resume PDF first."
        )

        st.stop()


    if not job_description.strip():

        st.warning(
            "⚠️ Please paste a job description first."
        )

        st.stop()


    # ========================================================
    # STEP 1 — RESUME TEXT EXTRACTION
    # ========================================================

    with st.spinner(
        "📖 Extracting text from resume..."
    ):

        try:

            resume_text = extract_text_from_pdf(
                uploaded_file
            )

        except Exception as e:

            st.error(
                f"❌ Resume parsing failed: {e}"
            )

            st.stop()


    if not resume_text or not resume_text.strip():

        st.error(
            "❌ Could not extract readable text from the uploaded PDF."
        )

        st.stop()


    # ========================================================
    # STEP 2 — SKILL EXTRACTION
    # ========================================================

    with st.spinner(
        "🛠️ Detecting resume and job skills..."
    ):

        try:

            resume_skills = extract_skills(
                resume_text
            )

        except Exception:

            resume_skills = []


        try:

            job_skills = extract_skills(
                job_description
            )

        except Exception:

            job_skills = []


    if not isinstance(
        resume_skills,
        list
    ):

        resume_skills = list(
            resume_skills
        )


    if not isinstance(
        job_skills,
        list
    ):

        job_skills = list(
            job_skills
        )


    # ========================================================
    # STEP 3 — JOB MATCHING
    # ========================================================

    with st.spinner(
        "🎯 Calculating job match..."
    ):

        try:

            match_result = calculate_match(
                resume_text,
                job_description
            )

        except Exception as e:

            st.error(
                f"❌ Matching calculation failed: {e}"
            )

            st.stop()


    # ========================================================
    # MATCH RESULT
    # ========================================================

    match_percentage = 0.0
    matched_skills = []
    missing_skills = []


    try:

        if isinstance(
            match_result,
            dict
        ):

            match_percentage = match_result.get(
                "match_percentage",
                match_result.get(
                    "score",
                    0
                )
            )

            matched_skills = match_result.get(
                "matched_skills",
                []
            )

            missing_skills = match_result.get(
                "missing_skills",
                []
            )


        elif isinstance(
            match_result,
            (tuple, list)
        ):

            match_percentage = (
                match_result[0]
                if len(match_result) > 0
                else 0
            )

            matched_skills = (
                match_result[1]
                if len(match_result) > 1
                else []
            )

            missing_skills = (
                match_result[2]
                if len(match_result) > 2
                else []
            )

        else:

            match_percentage = match_result

    except Exception:

        match_percentage = 0
        matched_skills = []
        missing_skills = []


    # ========================================================
    # NORMALIZE MATCH SCORE
    # ========================================================

    try:

        match_percentage = float(
            match_percentage
        )

    except Exception:

        match_percentage = 0.0


    if match_percentage <= 1:

        match_percentage *= 100


    match_percentage = max(
        0.0,
        min(
            100.0,
            match_percentage
        )
    )


    # ========================================================
    # AUTHORITATIVE SKILL MATCHING
    # ========================================================

    resume_skill_map = {
        str(skill).strip().lower(): str(skill).strip()
        for skill in resume_skills
        if str(skill).strip()
    }


    job_skill_map = {
        str(skill).strip().lower(): str(skill).strip()
        for skill in job_skills
        if str(skill).strip()
    }


    matched_skills = []
    missing_skills = []


    for skill_key, original_skill in job_skill_map.items():

        if skill_key in resume_skill_map:

            matched_skills.append(
                resume_skill_map[skill_key]
            )

        else:

            missing_skills.append(
                original_skill
            )


    matched_skills = sorted(
        set(matched_skills),
        key=str.lower
    )


    missing_skills = sorted(
        set(missing_skills),
        key=str.lower
    )


    # ========================================================
    # FINAL SKILL MATCH SCORE
    # ========================================================

    if job_skill_map:

        match_percentage = (
            len(matched_skills)
            / len(job_skill_map)
            * 100
        )

    else:

        match_percentage = 0.0


    match_percentage = round(
        match_percentage,
        2
    )


    # ========================================================
    # STEP 4 — TF-IDF SIMILARITY
    # ========================================================

    with st.spinner(
        "🧠 Calculating TF-IDF text similarity..."
    ):

        try:

            similarity_score = calculate_similarity(
                resume_text,
                job_description
            )

        except Exception as e:

            st.warning(
                f"⚠️ TF-IDF similarity calculation failed: {e}"
            )

            similarity_score = 0.0


    try:

        similarity_score = float(
            similarity_score
        )

    except Exception:

        similarity_score = 0.0


    if similarity_score <= 1:

        similarity_score *= 100


    similarity_score = max(
        0.0,
        min(
            100.0,
            similarity_score
        )
    )


    similarity_score = round(
        similarity_score,
        2
    )


    # ========================================================
    # STEP 5 — ATS ANALYSIS
    # ========================================================

    with st.spinner(
        "📊 Calculating ATS score..."
    ):

        try:

            ats_result = calculate_ats_score(
                resume_text,
                job_description,
                resume_skills=resume_skills,
                required_skills=job_skills
            )

        except Exception as e:

            st.error(
                f"❌ ATS analysis failed: {e}"
            )

            st.stop()


    # ========================================================
    # ATS RESULT
    # ========================================================

    if not isinstance(
        ats_result,
        dict
    ):

        st.error(
            "❌ ATS analyzer returned an unexpected result."
        )

        st.stop()


    ats_score = ats_result.get(
        "ats_score",
        0
    )

    ats_keyword_match = ats_result.get(
        "keyword_match",
        0
    )

    ats_skill_match = ats_result.get(
        "skill_match",
        0
    )

    resume_quality = ats_result.get(
        "resume_quality",
        0
    )

    quality_feedback = ats_result.get(
        "quality_feedback",
        []
    )

    ats_matched_keywords = ats_result.get(
        "matched_keywords",
        []
    )

    ats_missing_keywords = ats_result.get(
        "missing_keywords",
        []
    )


    # ========================================================
    # SCORE HELPER
    # ========================================================

    def safe_score(value):

        try:

            value = float(value)

        except Exception:

            return 0.0


        if value <= 1:

            value *= 100


        return max(
            0.0,
            min(
                100.0,
                value
            )
        )


    ats_score = safe_score(
        ats_score
    )

    ats_keyword_match = safe_score(
        ats_keyword_match
    )

    ats_skill_match = safe_score(
        ats_skill_match
    )

    resume_quality = safe_score(
        resume_quality
    )


    # Keep visible skill match consistent
    ats_skill_match = match_percentage


    # ========================================================
    # KEYWORD COVERAGE
    # ========================================================

    total_job_skills = len(
        job_skills
    )

    matched_skill_count = len(
        matched_skills
    )

    missing_skill_count = len(
        missing_skills
    )


    if total_job_skills > 0:

        keyword_percentage = (
            matched_skill_count
            / total_job_skills
            * 100
        )

    else:

        keyword_percentage = 0.0


    keyword_percentage = round(
        keyword_percentage,
        2
    )


    # ========================================================
    # FINAL AI SCORE
    # ========================================================

    final_ai_score = (
        (ats_score * 0.40)
        + (match_percentage * 0.30)
        + (similarity_score * 0.30)
    )


    final_ai_score = max(
        0.0,
        min(
            100.0,
            final_ai_score
        )
    )


    final_ai_score = round(
        final_ai_score,
        2
    )


    # ========================================================
    # RESUME TEXT
    # ========================================================

    resume_lower = resume_text.lower()


    # ========================================================
    # DASHBOARD
    # ========================================================

    st.divider()

    st.header(
        "📊 Resume Analysis Dashboard"
    )


    score1, score2, score3, score4 = st.columns(4)


    with score1:

        st.metric(
            "🤖 Final AI Score",
            f"{final_ai_score:.1f}%"
        )


    with score2:

        st.metric(
            "📋 ATS Score",
            f"{ats_score:.1f}%"
        )


    with score3:

        st.metric(
            "🎯 Job Match",
            f"{match_percentage:.1f}%"
        )


    with score4:

        st.metric(
            "🔎 TF-IDF Similarity",
            f"{similarity_score:.1f}%"
        )


    st.progress(
        min(
            max(
                int(final_ai_score),
                0
            ),
            100
        )
    )


    # ========================================================
    # SCORE INTERPRETATION
    # ========================================================

    if final_ai_score >= 80:

        st.success(
            "🌟 Strong resume-job alignment. "
            "Your resume is well aligned with the provided job description."
        )

    elif final_ai_score >= 60:

        st.info(
            "👍 Good resume-job alignment. "
            "A few targeted improvements can make the resume stronger."
        )

    elif final_ai_score >= 40:

        st.warning(
            "⚠️ Moderate alignment. "
            "Consider improving job-specific content and resume structure."
        )

    else:

        st.error(
            "🚨 Low alignment. "
            "The current resume and job description have limited overall alignment."
        )


    # ========================================================
    # ATS ANALYSIS
    # ========================================================

    st.divider()

    st.header(
        "📋 ATS Analysis"
    )


    ats_col1, ats_col2 = st.columns(2)


    with ats_col1:

        st.subheader(
            "ATS Score"
        )

        st.metric(
            "ATS Compatibility",
            f"{ats_score:.1f}%"
        )

        st.progress(
            min(
                max(
                    int(ats_score),
                    0
                ),
                100
            )
        )


    with ats_col2:

        st.subheader(
            "ATS Interpretation"
        )

        if ats_score >= 80:

            st.success(
                "Excellent ATS compatibility."
            )

        elif ats_score >= 60:

            st.info(
                "Good ATS compatibility with room for improvement."
            )

        elif ats_score >= 40:

            st.warning(
                "Moderate ATS compatibility."
            )

        else:

            st.error(
                "Low ATS compatibility."
            )


    # ========================================================
    # ATS BREAKDOWN
    # ========================================================

    with st.expander(
        "🔍 View ATS Breakdown"
    ):

        breakdown1, breakdown2, breakdown3 = st.columns(3)


        with breakdown1:

            st.metric(
                "Keyword Match",
                f"{ats_keyword_match:.1f}%"
            )

            st.caption(
                "Weight: 40%"
            )


        with breakdown2:

            st.metric(
                "Skill Match",
                f"{ats_skill_match:.1f}%"
            )

            st.caption(
                "Weight: 35%"
            )


        with breakdown3:

            st.metric(
                "Resume Quality",
                f"{resume_quality:.1f}%"
            )

            st.caption(
                "Weight: 25%"
            )


        st.write(
            f"**Resume Word Count:** {len(resume_text.split())}"
        )

        st.write(
            f"**Recognized Job Skills:** {len(job_skills)}"
        )

        st.write(
            f"**Matched Skills:** {len(matched_skills)}"
        )

        st.write(
            f"**Missing Skills:** {len(missing_skills)}"
        )


    # ========================================================
    # SKILL ANALYSIS
    # ========================================================

    st.divider()

    st.header(
        "🧠 Skill Analysis"
    )


    skill_col1, skill_col2 = st.columns(2)


    with skill_col1:

        st.subheader(
            "✅ Skills Found in Resume"
        )

        if resume_skills:

            for skill in resume_skills:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.warning(
                "No recognized skills detected."
            )


    with skill_col2:

        st.subheader(
            "💼 Skills Required by Job"
        )

        if job_skills:

            for skill in job_skills:

                if str(skill).strip().lower() in resume_skill_map:

                    st.success(
                        f"✓ {skill}"
                    )

                else:

                    st.warning(
                        f"⚠ {skill}"
                    )

        else:

            st.info(
                "No recognized skills detected from the job description."
            )


    # ========================================================
    # SKILL GAP
    # ========================================================

    st.divider()

    st.header(
        "📌 Skill Gap Analysis"
    )


    if missing_skills:

        st.warning(
            f"You are missing {len(missing_skills)} "
            "recognized skill(s) from the job description."
        )

        gap_col1, gap_col2 = st.columns(2)


        with gap_col1:

            for skill in missing_skills:

                st.write(
                    f"🔸 **{skill}**"
                )


        with gap_col2:

            st.info(
                "Consider adding these skills only if you "
                "genuinely have relevant knowledge or experience."
            )

    else:

        st.success(
            "🎉 Your resume contains all recognized skills "
            "identified from the job description."
        )


    # ========================================================
    # RESUME QUALITY ANALYZER
    # ========================================================

    st.divider()

    st.header(
        "📝 Resume Quality Analyzer"
    )


    # Contact

    if "@" in resume_text:

        st.success(
            "✅ Email/contact information detected."
        )

    else:

        st.warning(
            "⚠️ Email/contact information not clearly detected."
        )


    # Education

    education_keywords = [
        "education",
        "degree",
        "bachelor",
        "master",
        "b.tech",
        "m.tech",
        "university",
        "college"
    ]


    if any(
        keyword in resume_lower
        for keyword in education_keywords
    ):

        st.success(
            "✅ Education section detected."
        )

    else:

        st.warning(
            "⚠️ Education section not clearly detected."
        )


    # Experience

    experience_keywords = [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internship"
    ]


    if any(
        keyword in resume_lower
        for keyword in experience_keywords
    ):

        st.success(
            "✅ Experience section detected."
        )

    else:

        st.warning(
            "⚠️ Experience section not clearly detected."
        )


    # Projects

    if "project" in resume_lower:

        st.success(
            "✅ Project section detected."
        )

    else:

        st.warning(
            "⚠️ Project section not clearly detected."
        )


    # Skills

    if resume_skills:

        st.success(
            f"✅ {len(resume_skills)} recognized technical skills detected."
        )

    else:

        st.warning(
            "⚠️ No recognized technical skills detected."
        )


    # ========================================================
    # KEYWORD ANALYSIS
    # ========================================================

    st.divider()

    st.header(
        "🔑 Keyword Analysis"
    )


    keyword_col1, keyword_col2, keyword_col3 = st.columns(3)


    with keyword_col1:

        st.metric(
            "Job Keywords",
            total_job_skills
        )


    with keyword_col2:

        st.metric(
            "Matched Keywords",
            matched_skill_count
        )


    with keyword_col3:

        st.metric(
            "Missing Keywords",
            missing_skill_count
        )


    st.write(
        f"**Keyword Coverage: {keyword_percentage:.1f}%**"
    )


    st.progress(
        min(
            max(
                int(keyword_percentage),
                0
            ),
            100
        )
    )


    # ========================================================
    # TF-IDF ANALYSIS
    # ========================================================

    st.divider()

    st.header(
        "🔎 AI Matching Analysis"
    )


    similarity_col1, similarity_col2 = st.columns(2)


    with similarity_col1:

        st.subheader(
            "TF-IDF Text Similarity"
        )

        st.metric(
            "TF-IDF Similarity",
            f"{similarity_score:.1f}%"
        )

        st.caption(
            "Measures lexical overlap between the resume and job description."
        )

        st.progress(
            min(
                max(
                    int(similarity_score),
                    0
                ),
                100
            )
        )


    with similarity_col2:

        st.subheader(
            "Interpretation"
        )

        if similarity_score >= 80:

            st.success(
                "Very strong textual alignment."
            )

        elif similarity_score >= 60:

            st.info(
                "Good textual alignment."
            )

        elif similarity_score >= 40:

            st.warning(
                "Moderate textual alignment."
            )

        else:

            st.warning(
                "Low textual alignment."
            )


    # ========================================================
    # PERSONALIZED SUGGESTIONS
    # ========================================================

    st.divider()

    st.header(
        "💡 Personalized Resume Suggestions"
    )


    try:

        suggestions = generate_suggestions(
            missing_skills
        )


        if suggestions:

            for suggestion in suggestions:

                st.info(
                    f"💡 {suggestion}"
                )

        else:

            st.success(
                "🎉 No additional suggestions were generated."
            )


    except Exception as e:

        st.warning(
            f"Suggestions could not be generated: {e}"
        )


    # ========================================================
    # RECRUITER RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.header(
        "👔 Recruiter-Style Recommendations"
    )


    recruiter_recommendations = []


    if ats_score < 60:

        recruiter_recommendations.append(
            "Improve ATS compatibility by using relevant "
            "job-specific keywords where they accurately "
            "represent your experience."
        )

    elif ats_score < 80:

        recruiter_recommendations.append(
            "ATS compatibility has room for improvement. "
            "Strengthen relevant keywords and resume structure."
        )

    else:

        recruiter_recommendations.append(
            "Your resume shows strong ATS compatibility "
            "for the analyzed job description."
        )


    if missing_skills:

        recruiter_recommendations.append(
            "Review the missing skills and add them only "
            "when supported by your actual experience."
        )

    else:

        recruiter_recommendations.append(
            "Your resume covers all recognized technical "
            "skills identified in the job description."
        )


    if similarity_score < 60:

        recruiter_recommendations.append(
            "Use terminology and project descriptions that "
            "more closely reflect the target job description."
        )

    else:

        recruiter_recommendations.append(
            "Resume language shows reasonable textual alignment "
            "with the target job description."
        )


    if "experience" not in resume_lower:

        recruiter_recommendations.append(
            "Consider adding a clearly labeled Experience section "
            "if applicable."
        )


    for recommendation in recruiter_recommendations:

        st.write(
            f"🔹 {recommendation}"
        )


    # ========================================================
    # RESUME OPTIMIZATION REPORT
    # ========================================================

    st.divider()

    st.header(
        "📈 Resume Optimization Report"
    )


    optimization_score = (
        (ats_score * 0.40)
        + (keyword_percentage * 0.30)
        + (similarity_score * 0.30)
    )


    optimization_score = max(
        0.0,
        min(
            100.0,
            optimization_score
        )
    )


    optimization_score = round(
        optimization_score,
        2
    )


    st.metric(
        "Resume Optimization Level",
        f"{optimization_score:.1f}%"
    )


    st.progress(
        min(
            max(
                int(optimization_score),
                0
            ),
            100
        )
    )


    optimization_col1, optimization_col2 = st.columns(2)


    # Strengths

    with optimization_col1:

        st.subheader(
            "Strengths"
        )


        strengths = []


        if ats_score >= 70:

            strengths.append(
                "Strong ATS compatibility"
            )


        if similarity_score >= 60:

            strengths.append(
                "Good job-description alignment"
            )


        if keyword_percentage >= 60:

            strengths.append(
                "Good keyword coverage"
            )


        if resume_skills:

            strengths.append(
                f"{len(resume_skills)} technical skills detected"
            )


        if not strengths:

            strengths.append(
                "Resume analysis completed; additional optimization opportunities identified."
            )


        for strength in strengths:

            st.success(
                f"✓ {strength}"
            )


    # Improvement Areas

    with optimization_col2:

        st.subheader(
            "Improvement Areas"
        )


        improvements = []


        if ats_score < 70:

            improvements.append(
                "Improve ATS compatibility"
            )


        if similarity_score < 60:

            improvements.append(
                "Increase job-description alignment"
            )


        if keyword_percentage < 60:

            improvements.append(
                "Improve relevant keyword coverage"
            )


        if missing_skills:

            improvements.append(
                "Address relevant skill gaps"
            )


        if not improvements:

            st.success(
                "No major improvement areas detected."
            )

        else:

            for improvement in improvements:

                st.warning(
                    f"⚠ {improvement}"
                )


    # ========================================================
    # AI JOB ROLE RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.header(
        "🎯 AI Job Role Recommendations"
    )


    st.caption(
        "Based on the skills and information detected from your resume."
    )


    selected_job_role = None


    try:

        role_recommendations = get_job_recommendations(
            resume_text
        )


        if isinstance(
            role_recommendations,
            (list, tuple)
        ):

            if role_recommendations:

                for index, role_data in enumerate(
                    role_recommendations[:5]
                ):

                    role_name = "Unknown Role"
                    confidence = 0.0


                    if isinstance(
                        role_data,
                        dict
                    ):

                        role_name = role_data.get(
                            "job_role",
                            role_data.get(
                                "role",
                                "Unknown Role"
                            )
                        )

                        confidence = role_data.get(
                            "confidence",
                            role_data.get(
                                "score",
                                0
                            )
                        )

                    else:

                        role_name = str(
                            role_data
                        )


                    try:

                        confidence = float(
                            confidence
                        )

                    except Exception:

                        confidence = 0.0


                    if confidence <= 1:

                        confidence *= 100


                    confidence = max(
                        0.0,
                        min(
                            100.0,
                            confidence
                        )
                    )


                    if index == 0:

                        selected_job_role = role_name

                        st.subheader(
                            f"🥇 {role_name}"
                        )

                        st.caption(
                            f"Top AI Recommendation • "
                            f"Role Match Score: {confidence:.2f}%"
                        )

                        st.progress(
                            int(confidence)
                        )

                    else:

                        st.subheader(
                            f"🎯 {role_name}"
                        )

                        st.caption(
                            f"Role Match Score: {confidence:.2f}%"
                        )

                        st.progress(
                            int(confidence)
                        )


                    if index < len(
                        role_recommendations[:5]
                    ) - 1:

                        st.divider()


            else:

                st.info(
                    "No job-role recommendations available."
                )


        elif isinstance(
            role_recommendations,
            dict
        ):

            selected_job_role = role_recommendations.get(
                "job_role",
                role_recommendations.get(
                    "role",
                    "Unknown Role"
                )
            )


            confidence = role_recommendations.get(
                "confidence",
                role_recommendations.get(
                    "score",
                    0
                )
            )


            try:

                confidence = float(
                    confidence
                )

            except Exception:

                confidence = 0.0


            if confidence <= 1:

                confidence *= 100


            confidence = max(
                0.0,
                min(
                    100.0,
                    confidence
                )
            )


            st.subheader(
                f"🥇 {selected_job_role}"
            )

            st.caption(
                f"AI Recommendation • "
                f"Role Match Score: {confidence:.2f}%"
            )

            st.progress(
                int(confidence)
            )


        elif role_recommendations:

            selected_job_role = str(
                role_recommendations
            )

            st.subheader(
                f"🥇 {selected_job_role}"
            )


        else:

            st.info(
                "No job-role recommendations available."
            )


    except Exception as e:

        st.warning(
            f"Job role recommendation could not be generated: {e}"
        )


    # ========================================================
    # ROLE-BASED SKILL GAP
    # ========================================================

    st.divider()

    st.header(
        "🧩 Role-Based Skill Gap"
    )


    if selected_job_role:

        st.subheader(
            f"🎯 Target Role: {selected_job_role}"
        )


        try:

            role_skill_gap = get_role_skill_gap(
                resume_text,
                selected_job_role
            )


            if isinstance(
                role_skill_gap,
                dict
            ):

                matched_role_skills = role_skill_gap.get(
                    "matched_skills",
                    role_skill_gap.get(
                        "matching_skills",
                        []
                    )
                )


                missing_role_skills = role_skill_gap.get(
                    "missing_skills",
                    role_skill_gap.get(
                        "skills_to_learn",
                        []
                    )
                )


                if not isinstance(
                    matched_role_skills,
                    (list, tuple, set)
                ):

                    matched_role_skills = (
                        [matched_role_skills]
                        if matched_role_skills
                        else []
                    )


                if not isinstance(
                    missing_role_skills,
                    (list, tuple, set)
                ):

                    missing_role_skills = (
                        [missing_role_skills]
                        if missing_role_skills
                        else []
                    )


                # ------------------------------------------------
                # Normalize using actual resume skills
                # ------------------------------------------------

                detected_resume_lower = {
                    str(skill).strip().lower()
                    for skill in resume_skills
                }


                filtered_matched = []

                for skill in matched_role_skills:

                    skill_text = str(
                        skill
                    ).strip()


                    if skill_text.lower() in detected_resume_lower:

                        filtered_matched.append(
                            skill_text
                        )


                # ------------------------------------------------
                # Remove already-known skills from missing list
                # ------------------------------------------------

                filtered_missing = []

                for skill in missing_role_skills:

                    skill_text = str(
                        skill
                    ).strip()


                    if skill_text.lower() not in detected_resume_lower:

                        filtered_missing.append(
                            skill_text
                        )


                # ------------------------------------------------
                # Display
                # ------------------------------------------------

                role_col1, role_col2 = st.columns(2)


                with role_col1:

                    st.subheader(
                        "✅ Skills You Have"
                    )


                    if filtered_matched:

                        for skill in sorted(
                            set(filtered_matched),
                            key=str.lower
                        ):

                            st.success(
                                f"✓ {skill}"
                            )

                    else:

                        st.info(
                            "No matching role-specific skills detected."
                        )


                with role_col2:

                    st.subheader(
                        "📚 Skills to Develop"
                    )


                    if filtered_missing:

                        for skill in sorted(
                            set(filtered_missing),
                            key=str.lower
                        ):

                            st.warning(
                                f"⚠ {skill}"
                            )

                    else:

                        st.success(
                            "🎉 No major role-specific skill gaps detected."
                        )


            else:

                st.info(
                    "Role-specific skill gap information is unavailable."
                )


        except Exception as e:

            st.warning(
                f"Skill gap analysis error: {e}"
            )


    else:

        st.info(
            "A target job role could not be determined."
        )


    # ========================================================
    # FINAL AI ASSESSMENT
    # ========================================================

    st.divider()

    st.header(
        "🏆 Final AI Resume Assessment"
    )


    final_col1, final_col2 = st.columns(
        [1, 2]
    )


    with final_col1:

        st.metric(
            "Final AI Score",
            f"{final_ai_score:.1f}%"
        )

        st.progress(
            min(
                max(
                    int(final_ai_score),
                    0
                ),
                100
            )
        )


    with final_col2:

        st.subheader(
            "AI Assessment"
        )


        if final_ai_score >= 80:

            st.success(
                "🌟 Strong alignment with the target job. "
                "The resume demonstrates good coverage across "
                "ATS, skills and textual similarity."
            )

        elif final_ai_score >= 60:

            st.info(
                "👍 Good foundation. Targeted improvements to "
                "job-specific content can strengthen alignment."
            )

        elif final_ai_score >= 40:

            st.warning(
                "⚠️ Moderate alignment. Review job-specific "
                "keywords, skills and resume wording."
            )

        else:

            st.error(
                "🚨 Low overall alignment based on the analyzed "
                "ATS, skill-match and TF-IDF signals."
            )


    # ========================================================
    # QUICK ACTION PLAN
    # ========================================================

    st.divider()

    st.header(
        "⚡ Recommended Action Plan"
    )


    action_items = []


    if missing_skills:

        action_items.append(
            "Review the missing skills and highlight them only "
            "if you genuinely have relevant knowledge or experience."
        )


    if similarity_score < 60:

        action_items.append(
            "Tailor resume wording and project descriptions "
            "to the terminology used in the target job description."
        )


    if ats_score < 70:

        action_items.append(
            "Improve ATS compatibility using relevant keywords "
            "and clearly labeled resume sections."
        )


    if "project" not in resume_lower:

        action_items.append(
            "Add a clearly labeled Projects section with technologies "
            "and measurable outcomes."
        )


    if "experience" not in resume_lower:

        action_items.append(
            "Add a clearly labeled Experience section if applicable."
        )


    if not action_items:

        action_items.append(
            "Continue tailoring measurable achievements and "
            "keeping the resume targeted to each job description."
        )


    for number, action in enumerate(
        action_items,
        start=1
    ):

        st.write(
            f"**{number}.** {action}"
        )


    # ========================================================
    # EXTRACTED TEXT
    # ========================================================

    st.divider()


    with st.expander(
        "📄 View Extracted Resume Text"
    ):

        st.text_area(
            "Extracted Resume Content",
            resume_text,
            height=400
        )


    # ========================================================
    # DETECTED SKILLS
    # ========================================================

    with st.expander(
        "🔍 View Detected Resume Skills"
    ):

        if resume_skills:

            st.write(
                ", ".join(
                    str(skill)
                    for skill in resume_skills
                )
            )

        else:

            st.info(
                "No recognized skills detected."
            )


    # ========================================================
    # FINAL STATUS
    # ========================================================

    st.divider()

    st.success(
        "✅ Analysis completed successfully!"
    )


    st.caption(
        "AI Resume Analyzer • Resume Parsing • Skill Extraction • "
        "TF-IDF Matching • ATS Scoring • Job Classification"
    )