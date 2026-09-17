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
# PAGE CONFIG
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
    "Upload your resume and paste a job description to get an AI-powered "
    "analysis of your resume."
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
# MODEL EVALUATION
# ============================================================

with st.expander("🧠 View AI Model Information"):

    st.write(
        "This project combines resume parsing, skill extraction, "
        "TF-IDF similarity, ATS analysis and job-role classification."
    )

    try:
        evaluation = evaluate_model()

        if isinstance(evaluation, dict):

            metric_cols = st.columns(len(evaluation))

            for index, (key, value) in enumerate(evaluation.items()):

                with metric_cols[index]:
                    try:
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
                    except Exception:
                        st.write(f"**{key}:** {value}")

        elif evaluation is not None:
            st.write(evaluation)

    except Exception:
        st.caption(
            "Model evaluation information is currently unavailable."
        )


st.divider()


# ============================================================
# INPUT SECTION
# ============================================================

st.header("📥 Resume & Job Description")

input_col1, input_col2 = st.columns(2)


with input_col1:

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload your resume in PDF format",
        type=["pdf"]
    )


with input_col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder=(
            "Example:\n"
            "We are looking for a Python Developer with experience in "
            "Machine Learning, SQL, Pandas, NumPy and Git..."
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


    # --------------------------------------------------------
    # PROCESSING
    # --------------------------------------------------------

    with st.spinner("🤖 AI is analyzing your resume..."):

        try:

            # =================================================
            # RESUME TEXT EXTRACTION
            # =================================================

            resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text or not resume_text.strip():

                st.error(
                    "❌ Could not extract text from the uploaded PDF."
                )

                st.stop()


            # =================================================
            # SKILL EXTRACTION
            # =================================================

            resume_skills = extract_skills(resume_text)

            job_skills = extract_skills(job_description)


            # =================================================
            # MATCHING
            # =================================================

            try:

                match_result = calculate_match(
                    resume_skills,
                    job_skills
                )

            except Exception:

                match_result = 0


            # =================================================
            # TF-IDF SIMILARITY
            # =================================================

            try:

                similarity_score = calculate_similarity(
                    resume_text,
                    job_description
                )

            except Exception:

                similarity_score = 0


            # =================================================
            # ATS SCORE
            # =================================================

            try:

                ats_result = calculate_ats_score(
                    resume_text,
                    job_description
                )

            except Exception:

                ats_result = 0


            # =================================================
            # CONVERT SCORES SAFELY
            # =================================================

            def normalize_score(value):

                try:

                    if isinstance(value, dict):

                        possible_keys = [
                            "score",
                            "ats_score",
                            "match_score",
                            "similarity",
                            "percentage"
                        ]

                        for key in possible_keys:

                            if key in value:

                                value = value[key]
                                break

                    if isinstance(value, (list, tuple)):

                        if len(value) > 0:
                            value = value[0]

                    value = float(value)

                    if value <= 1:
                        value = value * 100

                    value = max(0, min(100, value))

                    return value

                except Exception:

                    return 0.0


            match_score = normalize_score(match_result)

            similarity_score = normalize_score(similarity_score)

            ats_score = normalize_score(ats_result)


            # =================================================
            # MISSING SKILLS
            # =================================================

            resume_skill_lower = {
                skill.lower()
                for skill in resume_skills
            }

            missing_skills = [
                skill
                for skill in job_skills
                if skill.lower() not in resume_skill_lower
            ]


            # =================================================
            # FINAL AI SCORE
            # =================================================

            final_ai_score = (
                (ats_score * 0.40)
                + (similarity_score * 0.35)
                + (match_score * 0.25)
            )

            final_ai_score = max(
                0,
                min(100, final_ai_score)
            )


            # =================================================
            # STORE IN SESSION
            # =================================================

            st.session_state["resume_text"] = resume_text
            st.session_state["resume_skills"] = resume_skills
            st.session_state["job_skills"] = job_skills
            st.session_state["missing_skills"] = missing_skills
            st.session_state["match_score"] = match_score
            st.session_state["similarity_score"] = similarity_score
            st.session_state["ats_score"] = ats_score
            st.session_state["final_ai_score"] = final_ai_score


            # =================================================
            # SUCCESS
            # =================================================

            st.success(
                "✅ Resume successfully processed and analyzed!"
            )


        except Exception as e:

            st.error(
                f"❌ Analysis failed: {str(e)}"
            )

            st.stop()


    # ========================================================
    # TOP SCORE DASHBOARD
    # ========================================================

    st.divider()

    st.header("📊 Resume Analysis Dashboard")

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
            f"{match_score:.1f}%"
        )


    with score4:

        st.metric(
            "🔎 TF-IDF Similarity",
            f"{similarity_score:.1f}%"
        )


    st.progress(
        int(final_ai_score)
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
            "A few targeted improvements can make your resume stronger."
        )

    elif final_ai_score >= 40:

        st.warning(
            "⚠️ Moderate alignment. "
            "Consider improving keywords, skills and job-specific content."
        )

    else:

        st.error(
            "🚨 Low alignment. "
            "Your resume needs stronger alignment with the target job."
        )


    # ========================================================
    # ATS ANALYSIS
    # ========================================================

    st.divider()

    st.header("📋 ATS Analysis")

    ats_col1, ats_col2 = st.columns(2)


    with ats_col1:

        st.subheader("ATS Score")

        st.metric(
            "ATS Compatibility",
            f"{ats_score:.1f}%"
        )

        st.progress(
            int(ats_score)
        )


    with ats_col2:

        st.subheader("ATS Interpretation")

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

    with st.expander("🔍 View ATS Breakdown"):

        keyword_count = len(job_skills)

        matched_count = (
            keyword_count - len(missing_skills)
        )

        resume_word_count = len(
            resume_text.split()
        )

        st.write(
            f"**Resume Word Count:** {resume_word_count}"
        )

        st.write(
            f"**Recognized Job Skills:** {keyword_count}"
        )

        st.write(
            f"**Matched Skills:** {matched_count}"
        )

        st.write(
            f"**Missing Skills:** {len(missing_skills)}"
        )


    # ========================================================
    # SKILL ANALYSIS
    # ========================================================

    st.divider()

    st.header("🧠 Skill Analysis")

    skill_col1, skill_col2 = st.columns(2)


    with skill_col1:

        st.subheader("✅ Skills Found in Resume")

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

        st.subheader("💼 Skills Required by Job")

        if job_skills:

            for skill in job_skills:

                if skill in resume_skills:

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
    # MISSING SKILLS
    # ========================================================

    st.divider()

    st.header("📌 Skill Gap Analysis")


    if missing_skills:

        st.warning(
            f"You are missing {len(missing_skills)} recognized skill(s) "
            "from the job description."
        )

        missing_col1, missing_col2 = st.columns(2)

        with missing_col1:

            for skill in missing_skills:

                st.write(
                    f"🔸 **{skill}**"
                )

        with missing_col2:

            st.info(
                "Consider adding these skills only if you genuinely "
                "have relevant knowledge or experience."
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

    st.header("📝 Resume Quality Analyzer")

    quality_feedback = []


    resume_lower = resume_text.lower()


    # Contact information
    if "@" in resume_text:

        quality_feedback.append(
            ("success", "✅ Email/contact information detected.")

        )

    else:

        quality_feedback.append(
            ("warning", "⚠️ Email/contact information not clearly detected.")
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

        quality_feedback.append(
            ("success", "✅ Education section detected.")
        )

    else:

        quality_feedback.append(
            ("warning", "⚠️ Education section not clearly detected.")
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

        quality_feedback.append(
            ("success", "✅ Experience section detected.")
        )

    else:

        quality_feedback.append(
            ("warning", "⚠️ Experience section not clearly detected.")
        )


    # Projects
    project_keywords = [
        "project",
        "projects"
    ]

    if any(
        keyword in resume_lower
        for keyword in project_keywords
    ):

        quality_feedback.append(
            ("success", "✅ Project section detected.")
        )

    else:

        quality_feedback.append(
            ("warning", "⚠️ Project section not clearly detected.")
        )


    # Skills
    if resume_skills:

        quality_feedback.append(
            (
                "success",
                f"✅ {len(resume_skills)} recognized technical skills detected."
            )
        )

    else:

        quality_feedback.append(
            (
                "warning",
                "⚠️ No recognized technical skills detected."
            )
        )


    for feedback_type, message in quality_feedback:

        if feedback_type == "success":

            st.success(message)

        else:

            st.warning(message)


    # ========================================================
    # KEYWORD ANALYSIS
    # ========================================================

    st.divider()

    st.header("🔑 Keyword Analysis")

    total_job_skills = len(job_skills)

    matched_skill_count = (
        total_job_skills - len(missing_skills)
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
            len(missing_skills)
        )


    if total_job_skills > 0:

        keyword_percentage = (
            matched_skill_count
            / total_job_skills
            * 100
        )

    else:

        keyword_percentage = 0


    st.write(
        f"**Keyword Coverage: {keyword_percentage:.1f}%**"
    )

    st.progress(
        int(keyword_percentage)
    )


    # ========================================================
    # TF-IDF ANALYSIS
    # ========================================================

    st.divider()

    st.header("🔎 AI Matching Analysis")

    similarity_col1, similarity_col2 = st.columns(2)


    with similarity_col1:

        st.subheader("TF-IDF Similarity")

        st.metric(
            "Semantic/Text Similarity",
            f"{similarity_score:.1f}%"
        )

        st.progress(
            int(similarity_score)
        )


    with similarity_col2:

        st.subheader("Interpretation")

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

            st.error(
                "Low textual alignment."
            )


    # ========================================================
    # PERSONALIZED RESUME SUGGESTIONS
    # ========================================================

    st.divider()

    st.header("💡 Personalized Resume Suggestions")

    try:

        # IMPORTANT:
        # generate_suggestions accepts missing_skills only

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
            f"Suggestions could not be generated: {str(e)}"
        )


    # ========================================================
    # RECRUITER STYLE RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.header("👔 Recruiter-Style Recommendations")

    recruiter_recommendations = []


    if ats_score < 60:

        recruiter_recommendations.append(
            "Improve ATS compatibility by using relevant job-specific keywords."
        )

    elif ats_score < 80:

        recruiter_recommendations.append(
            "Your ATS compatibility is reasonable. Add more targeted keywords where relevant."
        )

    else:

        recruiter_recommendations.append(
            "Your resume demonstrates strong ATS compatibility."
        )


    if len(missing_skills) > 0:

        recruiter_recommendations.append(
            "Review the missing skills and add relevant ones only when supported by your experience."
        )

    else:

        recruiter_recommendations.append(
            "Your resume covers the recognized skills identified in the job description."
        )


    if similarity_score < 60:

        recruiter_recommendations.append(
            "Use terminology and project descriptions that more closely reflect the target job description."
        )

    else:

        recruiter_recommendations.append(
            "Your resume language has good alignment with the job description."
        )


    if "project" not in resume_lower:

        recruiter_recommendations.append(
            "Consider adding a clearly labeled Projects section with measurable outcomes."
        )


    if "experience" not in resume_lower:

        recruiter_recommendations.append(
            "Consider adding a clearly labeled Experience section if applicable."
        )


    for recommendation in recruiter_recommendations:

        st.write(
            f"🔹 {recommendation}"
        )


    # ========================================================
    # RESUME OPTIMIZATION REPORT
    # ========================================================

    st.divider()

    st.header("📈 Resume Optimization Report")

    optimization_score = (
        (ats_score * 0.4)
        + (keyword_percentage * 0.3)
        + (similarity_score * 0.3)
    )

    optimization_score = max(
        0,
        min(100, optimization_score)
    )


    st.metric(
        "Resume Optimization Level",
        f"{optimization_score:.1f}%"
    )

    st.progress(
        int(optimization_score)
    )


    optimization_col1, optimization_col2 = st.columns(2)


    with optimization_col1:

        st.subheader("Strengths")

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


        if strengths:

            for strength in strengths:

                st.success(
                    f"✓ {strength}"
                )

        else:

            st.info(
                "More resume strengths can be developed."
            )


    with optimization_col2:

        st.subheader("Improvement Areas")

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


        if improvements:

            for improvement in improvements:

                st.warning(
                    f"⚠ {improvement}"
                )

        else:

            st.success(
                "No major improvement areas detected."
            )


    # ========================================================
    # AI JOB ROLE RECOMMENDATIONS
    # ========================================================

    st.divider()

    st.header("🎯 AI Job Role Recommendations")

    st.caption(
        "Based on the skills and information detected from your resume."
    )


    selected_job_role = None


    try:

        role_recommendations = get_job_recommendations(
            resume_text
        )


        # ----------------------------------------------------
        # CASE 1: LIST / TUPLE
        # ----------------------------------------------------

        if isinstance(
            role_recommendations,
            (list, tuple)
        ):

            if len(role_recommendations) == 0:

                st.info(
                    "No job-role recommendations available."
                )

            else:

                for index, role_data in enumerate(
                    role_recommendations[:5]
                ):

                    role_name = "Unknown Role"
                    confidence = 0


                    if isinstance(
                        role_data,
                        dict
                    ):

                        role_name = (
                            role_data.get(
                                "job_role",
                                role_data.get(
                                    "role",
                                    "Unknown Role"
                                )
                            )
                        )

                        confidence = (
                            role_data.get(
                                "confidence",
                                role_data.get(
                                    "score",
                                    0
                                )
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

                        confidence = 0


                    if confidence <= 1:

                        confidence = confidence * 100


                    confidence = max(
                        0,
                        min(100, confidence)
                    )


                    # First role is target role
                    if index == 0:

                        selected_job_role = role_name

                        st.subheader(
                            f"🥇 {role_name}"
                        )

                        st.caption(
                            f"Top AI Recommendation • "
                            f"Confidence: {confidence:.2f}%"
                        )

                        st.progress(
                            int(confidence)
                        )

                    else:

                        st.subheader(
                            f"🎯 {role_name}"
                        )

                        st.caption(
                            f"AI Confidence: {confidence:.2f}%"
                        )

                        st.progress(
                            int(confidence)
                        )


                    if index < len(
                        role_recommendations[:5]
                    ) - 1:

                        st.divider()


        # ----------------------------------------------------
        # CASE 2: DICTIONARY
        # ----------------------------------------------------

        elif isinstance(
            role_recommendations,
            dict
        ):

            role_name = (
                role_recommendations.get(
                    "job_role",
                    role_recommendations.get(
                        "role",
                        "Unknown Role"
                    )
                )
            )

            confidence = (
                role_recommendations.get(
                    "confidence",
                    role_recommendations.get(
                        "score",
                        0
                    )
                )
            )


            try:

                confidence = float(
                    confidence
                )

            except Exception:

                confidence = 0


            if confidence <= 1:

                confidence *= 100


            confidence = max(
                0,
                min(100, confidence)
            )


            selected_job_role = role_name


            st.subheader(
                f"🥇 {role_name}"
            )

            st.caption(
                f"AI Recommendation • "
                f"Confidence: {confidence:.2f}%"
            )

            st.progress(
                int(confidence)
            )


        # ----------------------------------------------------
        # CASE 3: STRING
        # ----------------------------------------------------

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
            f"Job role recommendation could not be generated: {str(e)}"
        )


    # ========================================================
    # ROLE BASED SKILL GAP
    # ========================================================

    st.divider()

    st.header("🧩 Role-Based Skill Gap")

    if selected_job_role:

        st.subheader(
            f"🎯 Target Role: {selected_job_role}"
        )


        try:

            # IMPORTANT:
            # get_role_skill_gap requires:
            # resume_text + job_role

            role_skill_gap = get_role_skill_gap(
                resume_text,
                selected_job_role
            )


            if isinstance(
                role_skill_gap,
                dict
            ):

                matched_role_skills = (
                    role_skill_gap.get(
                        "matched_skills",
                        role_skill_gap.get(
                            "matching_skills",
                            []
                        )
                    )
                )


                missing_role_skills = (
                    role_skill_gap.get(
                        "missing_skills",
                        role_skill_gap.get(
                            "skills_to_learn",
                            []
                        )
                    )
                )


                role_col1, role_col2 = st.columns(2)


                with role_col1:

                    st.subheader(
                        "✅ Skills You Have"
                    )


                    if matched_role_skills:

                        if isinstance(
                            matched_role_skills,
                            (list, tuple, set)
                        ):

                            for skill in matched_role_skills:

                                st.success(
                                    f"✓ {skill}"
                                )

                        else:

                            st.success(
                                f"✓ {matched_role_skills}"
                            )

                    else:

                        st.info(
                            "No matching role-specific skills detected."
                        )


                with role_col2:

                    st.subheader(
                        "📚 Skills to Develop"
                    )


                    if missing_role_skills:

                        if isinstance(
                            missing_role_skills,
                            (list, tuple, set)
                        ):

                            for skill in missing_role_skills:

                                st.warning(
                                    f"⚠ {skill}"
                                )

                        else:

                            st.warning(
                                f"⚠ {missing_role_skills}"
                            )

                    else:

                        st.success(
                            "🎉 No major role-specific skill gaps detected."
                        )


            elif isinstance(
                role_skill_gap,
                (list, tuple, set)
            ):

                st.subheader(
                    "📚 Recommended Skills"
                )

                for skill in role_skill_gap:

                    st.warning(
                        f"⚠ {skill}"
                    )


            elif role_skill_gap:

                st.info(
                    str(role_skill_gap)
                )

            else:

                st.info(
                    "No role-specific skill gap information available."
                )


        except Exception as e:

            st.warning(
                f"Skill gap analysis error: {str(e)}"
            )

    else:

        st.info(
            "A target job role could not be determined."
        )


    # ========================================================
    # FINAL AI SUMMARY
    # ========================================================

    st.divider()

    st.header("🏆 Final AI Resume Assessment")


    final_col1, final_col2 = st.columns(
        [1, 2]
    )


    with final_col1:

        st.metric(
            "Final AI Score",
            f"{final_ai_score:.1f}%"
        )

        st.progress(
            int(final_ai_score)
        )


    with final_col2:

        st.subheader(
            "AI Assessment"
        )


        if final_ai_score >= 80:

            st.success(
                "🌟 Your resume shows strong alignment with the target job. "
                "Focus on maintaining clear achievements and relevant keywords."
            )

        elif final_ai_score >= 60:

            st.info(
                "👍 Your resume has a good foundation. "
                "Improving a few missing skills and job-specific keywords "
                "can strengthen the overall match."
            )

        elif final_ai_score >= 40:

            st.warning(
                "⚠️ Your resume has moderate alignment. "
                "Consider tailoring your skills, projects and keywords "
                "to the target role."
            )

        else:

            st.error(
                "🚨 Your resume currently has low alignment with the target job. "
                "Consider significantly tailoring the resume to the role."
            )


    # ========================================================
    # QUICK ACTION PLAN
    # ========================================================

    st.divider()

    st.header(" Recommended Action Plan")


    action_items = []


    if missing_skills:

        action_items.append(
            "Review the missing skills and develop or highlight relevant experience."
        )


    if similarity_score < 60:

        action_items.append(
            "Tailor your resume wording to the job description."
        )


    if ats_score < 70:

        action_items.append(
            "Improve ATS compatibility with relevant keywords and clear sections."
        )


    if "project" not in resume_lower:

        action_items.append(
            "Add a Projects section with technologies and measurable outcomes."
        )


    if "experience" not in resume_lower:

        action_items.append(
            "Add a clearly labeled Experience section if applicable."
        )


    if not action_items:

        action_items.append(
            "Continue refining measurable achievements and keeping your resume targeted."
        )


    for number, action in enumerate(
        action_items,
        start=1
    ):

        st.write(
            f"**{number}.** {action}"
        )


    # ========================================================
    # EXTRACTED RESUME TEXT
    # ========================================================

    st.divider()

    with st.expander("📄 View Extracted Resume Text"):

        st.text_area(
            "Extracted text",
            resume_text,
            height=400
        )


    # ========================================================
    # DETECTED RESUME SKILLS
    # ========================================================

    with st.expander(" View Detected Resume Skills"):

        if resume_skills:

            st.write(
                ", ".join(resume_skills)
            )

        else:

            st.write(
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