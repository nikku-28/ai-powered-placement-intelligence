import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
# AI semantic matching model
semantic_model = SentenceTransformer("all-MiniLM-L6-v2")


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI-Powered Placement Intelligence",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# SKILL DATABASE
# ============================================================

skills = [

    # Programming Languages
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C",
    "C++",
    "C#",
    "Go",
    "Kotlin",
    "Rust",
    "R",

    # Frontend
    "HTML",
    "CSS",
    "React",
    "Angular",
    "Vue.js",
    "Next.js",
    "Bootstrap",
    "Tailwind CSS",
    "Redux",

    # Backend / API
    "FastAPI",
    "Django",
    "Flask",
    "Node.js",
    "Express.js",
    "Spring Boot",
    "REST API",
    "GraphQL",
    "Microservices",
    "WebSockets",

    # Databases
    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "Redis",
    "SQLite",
    "Oracle",
    "Database Design",
    "Databases",

    # Cloud
    "AWS",
    "Azure",
    "GCP",
    "EC2",
    "S3",
    "Lambda",
    "Cloud Computing",
    "Cloud Fundamentals",
    "Serverless",

    # DevOps
    "Git",
    "GitHub",
    "GitLab",
    "Docker",
    "Kubernetes",
    "Jenkins",
    "CI/CD",
    "Terraform",

    # AI / ML
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Generative AI",
    "LLM",
    "NLP",
    "Computer Vision",
    "PyTorch",
    "TensorFlow",
    "Scikit-learn",
    "Pandas",
    "NumPy",

    # Software Engineering
    "Data Structures",
    "Algorithms",
    "OOP",
    "Object-Oriented Programming",
    "System Design",
    "Software Architecture",
    "Testing",
    "Unit Testing",
    "Integration Testing",
    "Pytest",
    "Agile",
    "Scrum",
    "Secure Coding",
    "Problem Solving"
]


# ============================================================
# HIGH PRIORITY SKILLS
# ============================================================

high_priority_skills = [
    "Python",
    "SQL",
    "Java",
    "C++",
    "JavaScript",
    "TypeScript",
    "Machine Learning",
    "Artificial Intelligence",
    "Data Structures",
    "Algorithms",
    "OOP",
    "System Design"
]


# ============================================================
# RELATED / PARTIAL SKILLS
# ============================================================

partial_skills = {

    "Python": ["Pandas", "NumPy", "Scikit-learn"],

    "Machine Learning": [
        "Scikit-learn",
        "TensorFlow",
        "PyTorch"
    ],

    "Artificial Intelligence": [
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Computer Vision"
    ],

    "SQL": [
        "MySQL",
        "PostgreSQL",
        "Oracle",
        "SQLite"
    ],

    "Database Design": [
        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB"
    ],

    "Cloud Computing": [
        "AWS",
        "Azure",
        "GCP"
    ],

    "Software Architecture": [
        "System Design",
        "Microservices"
    ],

    "Object-Oriented Programming": [
        "OOP",
        "Java",
        "C++",
        "C#"
    ]
}


# ============================================================
# FUNCTION: EXTRACT PDF TEXT
# ============================================================

def extract_resume_text(pdf_file):

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# ============================================================
# FUNCTION: FIND SKILLS
# ============================================================

def find_skills(text):

    found = []

    text_lower = text.lower()

    for skill in skills:

        if skill.lower() in text_lower:
            found.append(skill)

    return found


# ============================================================
# FUNCTION: CALCULATE WEIGHTED SCORE
# ============================================================

def calculate_weighted_score(
    jd_skills,
    resume_skills
):

    total_weight = 0
    matched_weight = 0

    exact_matches = []
    partial_matches = []
    missing_skills = []

    for skill in jd_skills:

        # ----------------------------------------------------
        # HIGH PRIORITY SKILL
        # ----------------------------------------------------

        if skill in high_priority_skills:
            weight = 2
        else:
            weight = 1

        total_weight += weight

        # ----------------------------------------------------
        # EXACT MATCH
        # ----------------------------------------------------

        if skill in resume_skills:

            matched_weight += weight

            exact_matches.append(skill)

        # ----------------------------------------------------
        # PARTIAL / RELATED MATCH
        # ----------------------------------------------------

        else:

            related = partial_skills.get(skill, [])

            has_partial_match = False

            for related_skill in related:

                if related_skill in resume_skills:

                    has_partial_match = True
                    break

            if has_partial_match:

                matched_weight += weight * 0.5

                partial_matches.append(skill)

            else:

                missing_skills.append(skill)

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    if total_weight > 0:

        score = (
            matched_weight / total_weight
        ) * 100

    else:

        score = 0

    return (
        score,
        exact_matches,
        partial_matches,
        missing_skills
    )


# ============================================================
# APPLICATION TITLE
# ============================================================

st.title("🎯 AI-Powered Placement Intelligence")

st.write(
    "Analyze your resume against a job description "
    "and identify your skill match, skill gaps and priorities."
)


# ============================================================
# INPUT SECTION
# ============================================================

resume_file = st.file_uploader(
    "📄 Upload your Resume (PDF)",
    type=["pdf"]
)


job_description = st.text_area(
    "💼 Paste the Job Description here:",
    height=250
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🚀 Analyze Resume & Job Description",
    use_container_width=True
):

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    if resume_file is None:

        st.warning(
            "⚠️ Please upload your resume first."
        )

    elif not job_description.strip():

        st.warning(
            "⚠️ Please paste a Job Description first."
        )

    else:

        # ----------------------------------------------------
        # EXTRACT RESUME TEXT
        # ----------------------------------------------------

        resume_text = extract_resume_text(
            resume_file
        )


        # ----------------------------------------------------
        # FIND SKILLS
        # ----------------------------------------------------

        resume_skills = find_skills(
            resume_text
        )

        jd_skills = find_skills(
            job_description
        )


        # ----------------------------------------------------
        # CALCULATE SCORE
        # ----------------------------------------------------

        (
            match_score,
            matched_skills,
            partial_matches,
            missing_skills
        ) = calculate_weighted_score(
            jd_skills,
            resume_skills
        )


        # ====================================================
        # RESULTS
        # ====================================================

        st.divider()

        st.subheader(
            "📊 Resume Analysis"
        )


        # ----------------------------------------------------
        # MATCH SCORE
        # ----------------------------------------------------

        st.metric(
            "Resume–JD Match Score",
            f"{match_score:.0f}%"
        )


        # ----------------------------------------------------
        # SCORE INTERPRETATION
        # ----------------------------------------------------

        if match_score >= 80:

            st.success(
                "🎉 Excellent match! "
                "Your resume strongly aligns with this job."
            )

        elif match_score >= 60:

            st.info(
                "👍 Good match! "
                "Your resume covers many important requirements."
            )

        elif match_score >= 40:

            st.warning(
                "⚠️ Moderate match. "
                "Several important skills could be improved."
            )

        else:

            st.error(
                "🚨 Low match. "
                "Several important JD requirements are missing."
            )


        # ----------------------------------------------------
        # PROGRESS BAR
        # ----------------------------------------------------

        st.progress(
            min(match_score / 100, 1.0)
        )


        # ====================================================
        # SKILL BREAKDOWN
        # ====================================================

        st.subheader(
            "📈 Skill Breakdown"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "JD Skills",
                len(jd_skills)
            )


        with col2:

            st.metric(
                "Matched",
                len(matched_skills)
            )


        with col3:

            st.metric(
                "Missing",
                len(missing_skills)
            )


        # ====================================================
        # RESUME SKILLS
        # ====================================================

        st.subheader(
            "✅ Skills Found in Your Resume"
        )


        if resume_skills:

            for skill in resume_skills:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.info(
                "No predefined skills were found "
                "in the resume."
            )


        # ====================================================
        # JD SKILLS
        # ====================================================

        st.subheader(
            "🎯 Skills Required by Job Description"
        )


        if jd_skills:

            for skill in jd_skills:

                st.write(
                    f"• {skill}"
                )

        else:

            st.info(
                "No predefined skills were found "
                "in the Job Description."
            )


        # ====================================================
        # EXACT MATCHES
        # ====================================================

        st.subheader(
            "🟢 Exact Skill Matches"
        )


        if matched_skills:

            for skill in matched_skills:

                st.success(
                    f"✓ {skill}"
                )

        else:

            st.warning(
                "No exact skill matches found."
            )


        # ====================================================
        # PARTIAL MATCHES
        # ====================================================

        st.subheader(
            "🟡 Related / Partial Matches"
        )


        if partial_matches:

            for skill in partial_matches:

                st.warning(
                    f"≈ {skill}"
                )

        else:

            st.info(
                "No partial skill matches found."
            )


        # ====================================================
        # MISSING SKILLS
        # ====================================================

        st.subheader(
            "🔴 Missing Skills"
        )


        if missing_skills:

            for skill in missing_skills:

                st.error(
                    f"✗ {skill}"
                )

        else:

            st.success(
                "🎉 Excellent! "
                "No required skills are missing."
            )


        # ====================================================
        # SKILL GAP PRIORITY
        # ====================================================

        st.divider()

        st.subheader(
            "🎯 Skill Gap Priority"
        )


        high_priority_missing = []

        medium_priority_missing = []


        for skill in missing_skills:

            if skill in high_priority_skills:

                high_priority_missing.append(
                    skill
                )

            else:

                medium_priority_missing.append(
                    skill
                )


        # ----------------------------------------------------
        # HIGH PRIORITY
        # ----------------------------------------------------

        st.write(
            "🔴 **High Priority — Focus First**"
        )


        if high_priority_missing:

            for skill in high_priority_missing:

                st.error(
                    f"🔥 {skill}"
                )

        else:

            st.success(
                "No high-priority skill gaps."
            )


        # ----------------------------------------------------
        # MEDIUM PRIORITY
        # ----------------------------------------------------

        st.write(
            "🟡 **Medium Priority — Good to Learn**"
        )


        if medium_priority_missing:

            for skill in medium_priority_missing:

                st.warning(
                    f"⚡ {skill}"
                )

        else:

            st.success(
                "No medium-priority skill gaps."
            )


        # ====================================================
        # FINAL RECOMMENDATION
        # ====================================================

        st.divider()

        st.subheader(
            "💡 Recommendation"
        )


        if match_score >= 80:

            st.success(
                "Your resume is highly aligned with "
                "the job description. Focus on interview "
                "preparation and strengthening your existing skills."
            )

        elif match_score >= 60:

            st.info(
                "Your resume has a reasonable match. "
                "Focus on the missing high-priority skills "
                "before applying."
            )

        elif match_score >= 40:

            st.warning(
                "Your resume has a moderate match. "
                "Improve the high-priority skill gaps "
                "and consider tailoring your resume."
            )

        else:

            st.error(
                "Your current resume has a low match "
                "with this JD. Focus on building the "
                "high-priority missing skills and "
                "tailoring your resume."
            )
            # ---------------------------------
# RESUME IMPROVEMENT SUGGESTIONS
# ---------------------------------

st.divider()

st.subheader("💡 Resume Improvement Suggestions")

if missing_skills:

    st.write("Based on the JD, consider addressing these skill gaps:")

    for skill in missing_skills[:10]:
        st.info(
            f"Consider adding or demonstrating **{skill}** "
            "in your resume if you genuinely have relevant experience."
        )

else:

    st.success(
        "Your resume contains the required skills identified from this JD."
    )