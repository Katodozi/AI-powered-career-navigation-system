import streamlit as st
import subprocess
from pymongo import MongoClient
from src.job_api import MerojobScraper
from src.recommender import recommend_jobs
from src.mcq_engine import generate_mcqs
from src.mcq_engine import generate_learning_resources

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI-Powered Career Navigation System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------ DB CONNECTION ------------------

@st.cache_resource
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["job_recommender"]
    return db["jobs"]

jobs_col = get_db()

# ------------------ CUSTOM CSS ------------------
st.markdown(
    """
    <style>
    /* ---------- Global ---------- */
    body {
        background-color: #0b1220;
        color: #e5e7eb;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #020617, #020617);
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #e5e7eb;
    }

    /* ---------- Dashboard Header ---------- */
    .dashboard-header {
        padding: 2.5rem 1rem 2rem 1rem;
        text-align: center;
        border-bottom: 1px solid #1e293b;
        margin-bottom: 2rem;
    }

    .dashboard-header h1 {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #3b82f6, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .dashboard-header p {
        font-size: 1.15rem;
        color: #cbd5f5;
        max-width: 900px;
        margin: 0 auto;
        line-height: 1.7;
    }

    /* ---------- Dashboard Cards ---------- */
    .dash-card {
        background: #020617;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 1.2rem;
        height: 100%;
    }


    .dash-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(59, 130, 246, 0.15);
    }

    .dash-card h3 {
        font-size: 1.2rem;
        font-weight: 700;
        color: #3b82f6;
        margin-bottom: 0.5rem;
    }

    .dash-card p {
        font-size: 0.95rem;
        color: #cbd5e1;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------ SIDEBAR NAVIGATION ------------------
st.sidebar.markdown("## 🧠 Career Navigator")
st.sidebar.caption("AI-powered career intelligence platform")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "🕷️ Scrape & Search Jobs",
        "🤖 Job Recommendations",
        "📝 Self Assessment",
        "📈 Learning Roadmap",
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    """
    **What this system does**
    - 🔍 Scrapes real job data  
    - 🤖 Matches skills intelligently  
    - 🧠 Assesses knowledge with MCQs  
    - 📈 Builds personalized roadmaps  
    """
)

# ------------------ DASHBOARD ------------------
if page == "🏠 Dashboard":
    st.markdown(
        """
        <div class="dashboard-header">
            <h1>AI-Powered Career Navigation System</h1>
            <p>
                A complete AI-driven career intelligence platform designed to help you
                discover relevant jobs, understand skill gaps, assess your readiness,
                and follow a structured roadmap to become job-ready.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        <style>
        html, body {
            height: 100%;
            overflow: hidden;
        }

        section.main {
            height: 100vh;
            overflow: hidden;
        }

        section.main > div {
            height: 100%;
            overflow: hidden;
        }

        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            height: 100%;
            overflow: hidden;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="dash-card">
                <h3>🕷️ Job Scraping</h3>
                <p>
                    Automatically scrape the latest jobs from Merojob and store them in a
                    structured database for analysis and search.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        

    with col2:
        st.markdown(
            """
            <div class="dash-card">
                <h3>🤖 Smart Recommendations</h3>
                <p>
                    Get transparent, skill-based job recommendations using semantic
                    matching and career intelligence logic.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            """
            <div class="dash-card">
                <h3>🧠 Skill Assessment</h3>
                <p>
                    Test yourself with AI-generated MCQs and instantly identify weak
                    areas with curated learning resources.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    col4, col5 = st.columns(2)

    with col4:
        st.markdown(
            """
            <div class="dash-card">
                <h3>📈 Learning Roadmaps</h3>
                <p>
                    Receive personalized, phase-wise learning roadmaps tailored to
                    specific job roles and skill gaps.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:
        st.markdown(
            """
            <div class="dash-card">
                <h3>🎯 Career Readiness</h3>
                <p>
                    Move from beginner to job-ready with clear guidance, assessments,
                    and actionable career insights.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================================================
# TAB 2: SCRAPE + SEARCH JOBS
# ==================================================
elif page == "🕷️ Scrape & Search Jobs":
    st.header("📂 Job Explorer")
    st.caption("Scrape latest jobs and explore your job database")

    # ------------------ SCRAPE SECTION ------------------
    st.subheader("🕷️ Scrape Jobs from Merojob")

    col1, col2 = st.columns([3, 1])

    with col1:
        keyword = st.text_input(
            "Job keyword",
            placeholder="e.g. Python Developer, Backend, QA"
        )

    with col2:
        max_jobs = st.slider("Max jobs", 5, 50, 20)

    if st.button("🚀 Start Scraping", use_container_width=True):
        if not keyword:
            st.warning("Please enter a keyword.")
        else:
            with st.spinner("Scraping jobs from Merojob..."):
                scraper = MerojobScraper(max_jobs=max_jobs)
                jobs = scraper.scrape(keyword)

                inserted = 0
                for job in jobs:
                    if not jobs_col.find_one({"url": job.get("url")}):
                        jobs_col.insert_one(job)
                        inserted += 1

            st.success(f"✅ {inserted} new jobs saved to database.")

    st.markdown("---")

    # ------------------ SEARCH SECTION ------------------
    st.subheader("🔍 Search Jobs in Database")

    col1, col2 = st.columns([3, 1])

    with col1:
        search_query = st.text_input(
            "Search",
            placeholder="Title, skills, company, description"
        )

    with col2:
        limit = st.selectbox("Results", [10, 20, 50, 100], index=1)

    query = {}
    if search_query:
        query = {
            "$or": [
                {"title": {"$regex": search_query, "$options": "i"}},
                {"company": {"$regex": search_query, "$options": "i"}},
                {"description": {"$regex": search_query, "$options": "i"}},
                {"skills_required": {"$regex": search_query, "$options": "i"}},
            ]
        }

    jobs = list(jobs_col.find(query).sort("_id", -1).limit(limit))

    st.markdown(f"### 📄 {len(jobs)} jobs found")

    if not jobs:
        st.info("No jobs found. Try another keyword.")
    else:
        for job in jobs:
            with st.container():
                st.markdown('<div class="job-card">', unsafe_allow_html=True)

                st.subheader(job.get("title", "No Title"))
                st.markdown(
                    f"<div class='job-meta'>🏢 {job.get('company', 'N/A')} "
                    f"| 📍 {job.get('location', 'N/A')}</div>",
                    unsafe_allow_html=True
                )

                if job.get("skills_required"):
                    st.markdown("🛠 **Skills**")
                    for s in job["skills_required"]:
                        st.markdown(
                            f"<span class='skill-chip'>{s}</span>",
                            unsafe_allow_html=True
                        )

                with st.expander("📄 Job Description"):
                    st.write(job.get("description", "No description available"))

                if job.get("url"):
                    st.markdown(f"🔗 [View Job Posting]({job['url']})")

                st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# TAB 3: JOB RECOMMENDATIONS
# ==================================================
elif page == "🤖 Job Recommendations":
    st.header("🤖 Job Recommendations")
    st.caption("Transparent skill-based matching using knowledge graph")

    user_skills_input = st.multiselect(
        "Your Skills",
        sorted({s for j in jobs_col.find() for s in j.get("skills_required", [])})
    )

    if st.button("🎯 Get Recommendations", use_container_width=True):
        user_skills = [s.lower() for s in user_skills_input]
        st.session_state["user_skills"] = user_skills

        if not user_skills:
            st.warning("Please select at least one skill.")
        else:
            results = recommend_jobs(user_skills)

            if not results:
                st.info("No suitable jobs found.")
            else:
                # 🔐 Store results for Roadmap tab
                st.session_state["recommended_jobs"] = results

                for idx, rec in enumerate(results, 1):
                    job = rec["job"]
                    exp = rec["explanation"]
                    gaps = rec["skill_gaps"]

                    with st.container():
                        st.subheader(f"{idx}. {job.get('title')}")
                        st.caption(f"🏢 {job.get('company')} | 📍 {job.get('location')}")

                        st.progress(rec["match_score"] / 100)
                        st.caption(f"🎯 Match Score: {rec['match_score']}%")

                        if exp["direct"]:
                            st.success("✅ Direct Matches: " + ", ".join(exp["direct"]))

                        if exp["category"]:
                            st.info("🧩 Category Matches: " + ", ".join(exp["category"]))

                        if exp["related"]:
                            st.info("🔗 Related Skills: " + ", ".join(exp["related"]))

                        if exp["title_boost"]:
                            st.warning("⭐ Title Priority Boost: " + ", ".join(exp["title_boost"]))

                        if gaps:
                            st.markdown("### 📌 Skill Gaps")
                            st.write(", ".join(s.title() for s in gaps))
                        else:
                            st.success("🎉 No major skill gaps identified!")

                        with st.expander("📄 Job Description"):
                            st.write(job.get("description"))

                        if job.get("url"):
                            st.markdown(f"🔗 [View Job Posting]({job['url']})")


# ==================================================
# TAB 4: SELF ASSESSMENT
# ==================================================
elif page == "📝 Self Assessment":
    st.header("📝 Skill Self Assessment")
    st.caption("Test your skills with AI-generated MCQs")

    # 🔐 Get recommended jobs from session
    recommended_jobs = st.session_state.get("recommended_jobs", [])

    if not recommended_jobs:
        st.info("Go to Job Recommendations tab and generate recommendations first.")
    else:
        # 🔹 Collect unique skills from recommended jobs
        recommended_skills = sorted({
            skill.lower()
            for rec in recommended_jobs
            for skill in rec["job"].get("skills_required", [])
        })

        if not recommended_skills:
            st.warning("No skills found for recommended jobs.")
        else:
            st.subheader("Select a skill to assess")

            selected_skill = st.radio(
                "Skills from Recommended Jobs",
                recommended_skills,
                horizontal=True
            )

            if st.button("🧠 Generate MCQs"):
                with st.spinner("Generating questions..."):
                    mcq_data = generate_mcqs(selected_skill)
                    st.session_state["mcqs"] = mcq_data
                    st.session_state["answers"] = {}

        # ------------------ SHOW MCQS ------------------
        if "mcqs" in st.session_state:
            questions = st.session_state["mcqs"]["questions"]

            if questions:
                st.markdown("---")
                st.subheader(f"📚 MCQs on {selected_skill.title()}")

                for i, q in enumerate(questions):
                    st.markdown(f"**Q{i+1}. {q['question']}**")

                    choice = st.radio(
                        f"Select answer for Q{i+1}",
                        options=list(q["options"].keys()),
                        format_func=lambda x: f"{x}. {q['options'][x]}",
                        key=f"q_{i}"
                    )

                    st.session_state["answers"][i] = choice

                # ------------------ SUBMIT ------------------
                if st.button("✅ Submit Assessment"):
                    score = 0
                    weak_topics = {}

                    for i, q in enumerate(questions):
                        if st.session_state["answers"].get(i) == q["answer"]:
                            score += 20
                        else:
                            topic = q.get("topic", "General")
                            weak_topics[topic] = weak_topics.get(topic, 0) + 1

                    st.markdown("---")
                    st.subheader("📊 Result")
                    st.metric("Score", f"{score} / 100")

                    # ✅ ONLY congratulate on perfect score
                    if score == 100:
                        st.success("🎉 Perfect score! You have excellent mastery of this skill.")
                    else:
                        st.warning("📉 Skill needs improvement")

                        if weak_topics:
                            st.markdown("### ⚠️ Weak Areas Identified!!")
                            for topic, count in weak_topics.items():
                                st.write(
                                    f"- **{topic}** (missed {count} question(s))"
                                )

                        st.markdown("### 📖 Recommended Learning Resources")

                        # ✅ Spinner added ONLY here
                        with st.spinner("Finding the best books and courses for you..."):
                            resources = generate_learning_resources(selected_skill)

                        if resources["books"]:
                            st.markdown("#### 📚 Books")
                            for b in resources["books"]:
                                st.write(
                                    f"• **{b['title']}** — {b['reason']}"
                                )

                        if resources["courses"]:
                            st.markdown("#### 🎓 Online Courses")
                            for c in resources["courses"]:
                                st.write(
                                    f"• **{c['title']}** ({c['platform']}) — {c['reason']}"
                                )

                        if not resources["books"] and not resources["courses"]:
                            st.info("No recommendations could be generated at this time.")
            else:
                st.warning("No questions were generated for this skill.")

# ==================================================
# TAB 5: LEARNING ROADMAP
# ==================================================
elif page == "📈 Learning Roadmap":
    st.header("🧭 Learning Roadmaps")
    st.caption("Personalized step-by-step preparation plans for recommended roles")

    if "recommended_jobs" not in st.session_state:
        st.info("Get job recommendations first to generate roadmaps.")
    else:
        jobs = st.session_state["recommended_jobs"]

        job_titles = {
            f"{rec['job'].get('title')} — {rec['job'].get('company')}": rec
            for rec in jobs
        }

        selected_job_label = st.radio(
            "Select a job to generate roadmap",
            list(job_titles.keys())
        )

        selected_rec = job_titles[selected_job_label]
        job = selected_rec["job"]
        gaps = selected_rec["skill_gaps"]

        if st.button("🛣 Generate Roadmap", use_container_width=True):
            with st.spinner("Generating personalized roadmap..."):
                prompt = f"""
You are a senior career mentor.

Job Title: {job.get('title')}
Job Description:
{job.get('description')}

User Skill Gaps:
{", ".join(gaps) if gaps else "No major gaps"}

Create a clear learning roadmap:
- Phase-wise steps
- What to learn in each phase
- Tools, technologies, concepts
- Beginner → job-ready progression
Keep it concise and actionable.
"""

                result = subprocess.run(
                    ["ollama", "run", "gpt-oss:120b-cloud"],
                    input=prompt,
                    text=True,
                    capture_output=True,
                    encoding="utf-8",
                    errors="ignore"
                )

                roadmap = (
                    result.stdout
                    or result.stderr
                    or "No roadmap could be generated."
                )

                st.session_state["roadmap_output"] = roadmap.strip()

        if "roadmap_output" in st.session_state:
            st.markdown("---")
            st.subheader("📍 Generated Roadmap")
            st.write(st.session_state["roadmap_output"])
