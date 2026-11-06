import streamlit as st
from dotenv import load_dotenv

from career_engine import generate_rule_based_plan
from llm_service import generate_ai_plan
from utils import make_download

load_dotenv()

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="AI Student Career Guidance Assistant",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Generative AI-Based Student Career Guidance Assistant")
st.caption("Personalized career paths, skill-gap analysis and learning roadmaps")

# --------------------------------------------------
# SESSION STATE
# IMPORTANT:
# - The form key below is "student_profile_form".
# - The profile data key is "student_profile_data".
# These names must remain different.
# --------------------------------------------------
if "career_plan" not in st.session_state:
    st.session_state["career_plan"] = None

if "student_profile_data" not in st.session_state:
    st.session_state["student_profile_data"] = None

if "generation_mode" not in st.session_state:
    st.session_state["generation_mode"] = ""

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.header("About this project")
    st.write(
        "This assistant uses a curated career knowledge base and, when configured, "
        "Groq-powered generative AI to create a personalized career plan."
    )
    st.info("Your profile is used only to generate guidance in this session.")

# --------------------------------------------------
# SAMPLE PROFILES
# --------------------------------------------------
SAMPLE_PROFILES = {
    "B.Com — Finance": {
        "qualification": "Undergraduate",
        "department": "Commerce",
        "degree": "B.Com",
        "year": "Final year",
        "skills": "Excel, accounting basics, communication",
        "interests": "financial markets, budgeting, analysis",
        "industry": "Banking and Financial Services",
        "goal": "Become a financial analyst",
        "location": "India",
    },
    "Mechanical — Automobiles": {
        "qualification": "Undergraduate",
        "department": "Mechanical Engineering",
        "degree": "B.E./B.Tech",
        "year": "Third year",
        "skills": "CAD basics, engineering drawing, teamwork",
        "interests": "automobiles, electric vehicles, design",
        "industry": "Automotive and Mobility",
        "goal": "Work as an automotive design engineer",
        "location": "India",
    },
    "Computer Science — AI": {
        "qualification": "Undergraduate",
        "department": "Computer Science",
        "degree": "B.E./B.Tech",
        "year": "Final year",
        "skills": "Python, SQL, basic statistics",
        "interests": "artificial intelligence, machine learning, automation",
        "industry": "Information Technology",
        "goal": "Become an AI/ML engineer",
        "location": "India",
    },
    "MBA — Business Analytics": {
        "qualification": "Postgraduate",
        "department": "Management",
        "degree": "MBA",
        "year": "Completed",
        "skills": "Excel, presentation, business communication",
        "interests": "business strategy, data, problem solving",
        "industry": "Consulting and Business Services",
        "goal": "Become a business analyst",
        "location": "India",
    },
}

# --------------------------------------------------
# STUDENT PROFILE FORM
# The form key is intentionally NOT "student_profile_data".
# --------------------------------------------------
with st.form("student_profile_form"):
    st.subheader("1. Student profile")

    sample = st.selectbox(
        "Load a sample profile (optional)",
        ["Custom profile"] + list(SAMPLE_PROFILES.keys()),
    )
    sample_data = SAMPLE_PROFILES.get(sample, {})

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name (optional)", placeholder="Your name")

        qualification_options = [
            "Undergraduate",
            "Postgraduate",
            "Diploma",
            "12th / Higher Secondary",
            "Other",
        ]
        qualification_default = sample_data.get("qualification", "Undergraduate")
        qualification = st.selectbox(
            "Qualification",
            qualification_options,
            index=qualification_options.index(qualification_default),
        )

        department = st.text_input(
            "Department / stream",
            value=sample_data.get("department", ""),
        )
        degree = st.text_input(
            "Degree / course",
            value=sample_data.get("degree", ""),
        )

        year_options = [
            "First year",
            "Second year",
            "Third year",
            "Final year",
            "Completed",
            "Working professional",
        ]
        year_default = sample_data.get("year", "Final year")
        year = st.selectbox(
            "Current study status",
            year_options,
            index=year_options.index(year_default),
        )

    with col2:
        skills = st.text_area(
            "Current skills (comma-separated)",
            value=sample_data.get("skills", ""),
        )
        interests = st.text_area(
            "Interests (comma-separated)",
            value=sample_data.get("interests", ""),
        )

        industry_options = [
            "Not sure yet",
            "Information Technology",
            "Banking and Financial Services",
            "Automotive and Mobility",
            "Healthcare",
            "Education",
            "Manufacturing",
            "Consulting and Business Services",
            "Media and Design",
            "Government / Public Sector",
            "Other",
        ]
        industry_default = sample_data.get("industry", "Not sure yet")
        industry = st.selectbox(
            "Preferred industry",
            industry_options,
            index=industry_options.index(industry_default),
        )

        goal = st.text_input(
            "Career goal",
            value=sample_data.get("goal", ""),
            placeholder="e.g. Become a data analyst",
        )
        location = st.text_input(
            "Preferred job location",
            value=sample_data.get("location", "India"),
        )

    submitted = st.form_submit_button(
        "✨ Generate Career Plan",
        type="primary",
        use_container_width=True,
    )

# --------------------------------------------------
# GENERATE CAREER PLAN
# --------------------------------------------------
if submitted:
    if (
        not department.strip()
        or not skills.strip()
        or not interests.strip()
        or not goal.strip()
    ):
        st.error(
            "Please complete Department, Current skills, Interests and Career goal."
        )
    else:
        profile = {
            "name": name.strip(),
            "qualification": qualification,
            "department": department.strip(),
            "degree": degree.strip(),
            "year": year,
            "skills": [x.strip() for x in skills.split(",") if x.strip()],
            "interests": [x.strip() for x in interests.split(",") if x.strip()],
            "industry": industry,
            "goal": goal.strip(),
            "location": location.strip() or "Not specified",
        }

        try:
            with st.spinner("Analyzing your profile and preparing your career plan..."):
                plan, mode = generate_ai_plan(profile)

                if plan is None:
                    plan = generate_rule_based_plan(profile)
                    mode = "Knowledge-base mode"

            # Store the result in application data keys, not widget keys.
            st.session_state["career_plan"] = plan
            st.session_state["student_profile_data"] = profile
            st.session_state["generation_mode"] = mode

            st.success("Career plan generated successfully.")

        except Exception as exc:
            st.error(f"Career plan generation failed: {exc}")

# --------------------------------------------------
# DISPLAY CAREER PLAN
# --------------------------------------------------
plan = st.session_state.get("career_plan")
profile = st.session_state.get("student_profile_data")

if plan is not None and profile is not None:
    st.divider()

    student_name = profile.get("name", "")
    heading = "2. Career plan"
    if student_name:
        heading += f": {student_name}"
    st.subheader(heading)

    st.caption(
        f"Generated using: {st.session_state.get('generation_mode', 'Career assistant')}"
    )

    summary = plan.get("profile_summary", "")
    if summary:
        st.info(summary)

    # CAREER PATHS
    st.markdown("### Recommended career paths")
    roles = plan.get("career_paths", [])

    if not roles:
        st.warning("No career paths were returned. Please generate the plan again.")

    for i, role in enumerate(roles[:3], start=1):
        with st.expander(
            f"{i}. {role.get('role', 'Career role')}",
            expanded=(i == 1),
        ):
            st.write(role.get("why_it_fits", ""))

            st.markdown("**Typical responsibilities**")
            for item in role.get("responsibilities", []):
                st.write(f"• {item}")

            st.markdown("**Important skills**")
            st.write(
                ", ".join(role.get("required_skills", [])) or "Not specified"
            )

            st.markdown("**Relevant qualifications**")
            st.write(role.get("qualification", ""))

            st.markdown("**Certifications to consider**")
            for item in role.get("certifications", []):
                st.write(f"• {item}")

    # SKILL GAP
    st.markdown("### Skill-gap analysis")
    gaps = plan.get("skill_gap", {})
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Skills you already have**")
        for item in gaps.get("existing_skills", profile.get("skills", [])):
            st.write(f"✅ {item}")

    with col2:
        st.markdown("**Skills to develop**")
        for item in gaps.get("missing_skills", []):
            st.write(f"🎯 {item}")

    for item in gaps.get("actions", []):
        st.write(f"• {item}")

    # LEARNING ROADMAP
    st.markdown("### Learning roadmap")
    for stage in plan.get("roadmap", []):
        with st.expander(
            stage.get("stage", "Learning stage"),
            expanded=True,
        ):
            st.write(f"**Goal:** {stage.get('goal', '')}")
            st.write(f"**Topics:** {', '.join(stage.get('topics', []))}")

            st.markdown("**Practice activities**")
            for item in stage.get("activities", []):
                st.write(f"• {item}")

            st.markdown("**Project idea**")
            st.write(stage.get("project", ""))

    # LEARNING RESOURCES
    st.markdown("### Learning resources")
    for resource in plan.get("learning_resources", []):
        title = resource.get("name", "Learning resource")
        url = resource.get("url", "")
        purpose = resource.get("purpose", "")

        if url.startswith("https://"):
            st.markdown(f"- [{title}]({url}) — {purpose}")
        else:
            st.write(f"- {title} — {purpose}")

    # JOB SEARCH RESOURCES
    st.markdown("### Job-search resources")
    for item in plan.get("job_search_resources", []):
        url = item.get("url", "")
        if url.startswith("https://"):
            st.markdown(
                f"- [{item.get('name', 'Job portal')}]({url}) — "
                f"{item.get('purpose', '')}"
            )

    st.caption(
        "Job portals are provided as search resources. "
        "This application does not claim that any vacancy is live or available."
    )

    # DOWNLOADS
    st.markdown("### Download your career plan")
    download_data = make_download(profile, plan)

    col1, col2 = st.columns(2)

    with col1:
        st.download_button(
            "⬇️ Download career plan (JSON)",
            data=download_data,
            file_name="my_career_plan.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        st.download_button(
            "⬇️ Download career plan (Markdown)",
            data=make_download(profile, plan, markdown=True),
            file_name="my_career_plan.md",
            mime="text/markdown",
            use_container_width=True,
        )

st.divider()
st.caption(
    "Career guidance is informational, not a guarantee of employment or admission. "
    "Verify current course details, fees, eligibility and certification status "
    "on official provider websites."
)
