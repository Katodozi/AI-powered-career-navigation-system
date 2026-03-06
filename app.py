import streamlit as st
import subprocess
from pymongo import MongoClient
from src.job_api import MerojobScraper
from src.recommender import recommend_jobs
from src.mcq_engine import generate_mcqs
from src.mcq_engine import generate_learning_resources
from src.resume_parser import parse_resume

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="🧠 AI-Powered Career Navigation System",
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

# ------------------ ENHANCED GLOBAL CSS ------------------
st.markdown(
"""
<style>

/* ---------- GLOBAL BACKGROUND ---------- */
body {
    background: radial-gradient(circle at 20% 20%, #1e293b, #020617 70%);
    background-attachment: fixed;
    color: #e5e7eb;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* subtle animated glow */
body::before{
content:"";
position:fixed;
top:-200px;
left:-200px;
width:600px;
height:600px;
background:radial-gradient(circle,#3b82f6 0%,transparent 70%);
opacity:.15;
filter:blur(120px);
z-index:-1;
}

/* ---------- SCROLLBAR ---------- */
::-webkit-scrollbar {
width:8px;
}

::-webkit-scrollbar-thumb{
background:#334155;
border-radius:6px;
}

/* ---------- SIDEBAR ---------- */
section[data-testid="stSidebar"]{
background:linear-gradient(180deg,#020617,#0f172a);
border-right:1px solid #1e293b;
}

/* ---------- PAGE HEADINGS ---------- */
.page-title{
font-size:2.4rem;
font-weight:800;
background:linear-gradient(90deg,#60a5fa,#22d3ee);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
margin-bottom:5px;
}

.page-sub{
color:#94a3b8;
margin-bottom:30px;
}

/* ---------- DASHBOARD HEADER ---------- */
.dashboard-header{
text-align:center;
margin-bottom:40px;
}

.dashboard-header h1{
font-size:3rem;
font-weight:900;
background:linear-gradient(90deg,#60a5fa,#22d3ee);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.dashboard-header p{
color:#cbd5e1;
max-width:800px;
margin:auto;
}

/* ---------- CARDS ---------- */
.dash-card{
background:#020617;
border:1px solid #1e293b;
border-radius:16px;
padding:1.5rem;
transition:all .25s ease;
height:100%;
}

.dash-card:hover{
transform:translateY(-6px);
box-shadow:0 10px 30px rgba(0,0,0,.4);
}

.dash-card h3{
color:#60a5fa;
margin-bottom:10px;
}

.dash-card p{
color:#cbd5e1;
font-size:0.95rem;
}

/* ---------- BUTTONS (SOFTER COLORS) ---------- */
.stButton > button{
background:linear-gradient(135deg,#2563eb,#0ea5e9);
border:none;
border-radius:10px;
color:white;
font-weight:600;
padding:.55rem 1.2rem;
transition:.25s;
}

.stButton > button:hover{
background:linear-gradient(135deg,#1d4ed8,#0284c7);
transform:translateY(-1px);
}

/* ---------- TEAM CARDS ---------- */
.team-card{
background:#020617;
border:1px solid #1e293b;
border-radius:16px;
padding:1.2rem;
text-align:center;
transition:all .25s ease;
}

.team-card:hover{
transform:translateY(-5px);
box-shadow:0 10px 30px rgba(59,130,246,0.15);
}

/* ---------- TEAM IMAGE CONTAINER (STREAMLIT FIX) ---------- */
[data-testid="stImage"]{
display:flex;
justify-content:center;
align-items:center;
margin-bottom:10px;
}

/* ---------- TEAM IMAGE ---------- */
[data-testid="stImage"] img{
width:230px !important;
height:200px !important;
object-fit:cover;
border:3px solid #3b82f6;
box-shadow:0 0 15px rgba(59,130,246,0.35);
transition:all .3s ease;
}

/* Hover effect */
[data-testid="stImage"] img:hover{
transform:scale(1.05);
box-shadow:0 0 25px rgba(59,130,246,0.6);
}

/* ---------- TEXT ---------- */
.team-card h4{
margin-bottom:2px;
color:#60a5fa;
font-size:1rem;
}

.team-card p{
font-size:.85rem;
color:#94a3b8;
margin:2px 0;
}

# /* ---------- FEEDBACK BOX ---------- */
# .feedback-box{
# background:#020617;
# border:1px solid #1e293b;
# border-radius:14px;
# padding:20px;
# margin-top:30px;
# }

</style>
""",
unsafe_allow_html=True
)

# ------------------ SIDEBAR ------------------
st.sidebar.markdown(
"""
<h2 style="text-align:center;">🧠 Career Navigator</h2>
<p style="text-align:center;color:#94a3b8;">
AI Career Intelligence Platform
</p>
""",
unsafe_allow_html=True
)

page = st.sidebar.selectbox(
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
<b>🚀 Platform Features</b>

🔍 Real job scraping  
🤖 AI skill matching  
🧠 Knowledge assessments  
📈 Learning roadmaps
""",
unsafe_allow_html=True
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit • Ollama • MongoDB")

# ------------------ DASHBOARD ------------------
if page == "🏠 Dashboard":

    st.markdown(
    """
    <div class="dashboard-header">
        <h1>AI-Powered Career Navigation System</h1>
        <p>
        Discover relevant jobs, identify skill gaps, assess readiness,
        and follow structured learning paths toward your target career.
        </p>
    </div>
    """,
    unsafe_allow_html=True
    )

    # ---------- STATS ----------
    total_jobs = jobs_col.count_documents({})

    c1,c2,c3 = st.columns(3)

    c1.metric("📄 Jobs Collected",total_jobs)
    c2.metric("🧠 AI Modules","4")
    c3.metric("⚡ Recommendation Engine","Active")

    st.markdown("---")

    # ---------- FEATURE CARDS ----------
    col1,col2,col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="dash-card">
        <h3>🕷️ Job Scraping</h3>
        <p>
        Automatically scrape real job postings from Merojob
        and store them inside MongoDB for analysis.
        </p>
        </div>
        """,unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="dash-card">
        <h3>🤖 Smart Recommendations</h3>
        <p>
        AI-powered job matching based on skill similarity
        and semantic understanding.
        </p>
        </div>
        """,unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="dash-card">
        <h3>🧠 Skill Assessment</h3>
        <p>
        AI generated MCQs help evaluate your knowledge
        and identify weak areas.
        </p>
        </div>
        """,unsafe_allow_html=True)

    col4,col5 = st.columns(2)

    with col4:
        st.markdown("""
        <div class="dash-card">
        <h3>📈 Learning Roadmaps</h3>
        <p>
        Generate personalized learning paths
        based on skill gaps.
        </p>
        </div>
        """,unsafe_allow_html=True)

    with col5:
        st.markdown("""
        <div class="dash-card">
        <h3>🎯 Career Readiness</h3>
        <p>
        Track progress from beginner to job-ready
        using assessments and learning paths.
        </p>
        </div>
        """,unsafe_allow_html=True)

    st.markdown("---")

    # # ---------- FEEDBACK ----------
    # st.markdown('<div class="page-title">💬 Feedback</div>',unsafe_allow_html=True)
    # st.markdown('<div class="page-sub">Help us improve the platform</div>',unsafe_allow_html=True)

    # with st.container():
    #     name = st.text_input("Your Name")
    #     feedback = st.text_area("Your Feedback")

    #     if st.button("Submit Feedback"):
    #         st.success("Thank you for your feedback!")

    # st.markdown("---")

    # ---------- CONTACT ----------
    st.markdown('<div class="page-title">📩 Contact</div>',unsafe_allow_html=True)
    st.write("For queries or suggestions contact us at:")
    st.write("**careernavigator@gmail.com**")

    st.markdown("---")

    # ---------- TEAM ----------
    st.markdown('<div class="page-title">👨‍💻 Project Team</div>',unsafe_allow_html=True)

    t1,t2,t3,t4 = st.columns(4)

    with t1:
        st.image("resume_and_images\oneandonly.jpg")
        st.markdown("""
        <div class="team-card">
        <h4>Anuj Bhattarai</h4>
        <p>Full stack Developer</p>
        <p>ML & NLP Specialist</p>
        </div>
        """,unsafe_allow_html=True)

    with t2:
        st.image("resume_and_images\sagar.jpg")
        st.markdown("""
        <div class="team-card">
        <h4>Sagar Adhikari</h4>
        <p>Frontend developer</p>
        <p>System Design</p>
        </div>
        """,unsafe_allow_html=True)

    with t3:
        st.markdown("""
        <div class="team-card">
        <img src="https://i.pravatar.cc/100?img=3">
        <h4>Bidhwota Giri</h4>
        <p>QA</p>
        <p>UI/UX Designer</p>
        </div>
        """,unsafe_allow_html=True)

    with t4:
        st.markdown("""
        <div class="team-card">
        <img src="https://i.pravatar.cc/100?img=4">
        <h4>Apekshya Neupane</h4>
        <p>Frontend developer</p>
        <p>Job Market Research</p>
        </div>
        """,unsafe_allow_html=True)


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
    st.subheader("🔍 Search Jobs")

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

    st.markdown(f"### 📄 jobs found")

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

    # 🔹 Input Method Selection
    input_mode = st.radio(
        "Choose Input Method",
        ["Select Skills Manually", "Upload Resume (PDF)"]
    )

    user_skills = []

    # ==================================================
    # OPTION 1: MANUAL SKILL SELECTION (UNCHANGED LOGIC)
    # ==================================================
    if input_mode == "Select Skills Manually":
        user_skills_input = st.multiselect(
            "Your Skills",
            sorted({s for j in jobs_col.find() for s in j.get("skills_required", [])})
        )

        user_skills = [s.lower() for s in user_skills_input]

    # ==================================================
    # OPTION 2: RESUME UPLOAD
    # ==================================================
    else:
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF only)",
            type=["pdf"]
        )

        if uploaded_file is not None:
            with st.spinner("Parsing resume..."):
                resume_data = parse_resume(uploaded_file)

            # # ==============================
            # # 🔍 DEBUG SECTION
            # # ==============================
            # st.markdown("### 🔎 Debug Information")

            # from src.resume_parser import extract_text_from_pdf, llm_call

            # # Reset file pointer before re-reading
            # uploaded_file.seek(0)

            # raw_text = extract_text_from_pdf(uploaded_file)

            # st.write("**Extracted Text Length:**", len(raw_text))
            # st.text_area(
            #     "Extracted Text Preview (first 1000 chars)",
            #     raw_text[:1000],
            #     height=200
            # )

            # # Show raw LLM response
            # prompt_preview = raw_text[:3000]

            # debug_prompt = f"""
            # Extract skills as JSON only.
            # Resume:
            # {prompt_preview}
            # """

            # raw_llm_output = llm_call(debug_prompt)

            # st.text_area(
            #     "Raw LLM Output",
            #     raw_llm_output,
            #     height=200
            # )

            # # Show parsed output
            # st.write("Parsed Resume Data:", resume_data)

            # ==============================
            # NORMAL FLOW
            # ==============================

            extracted_skills = resume_data.get("skills", [])

            if not extracted_skills:
                st.warning("No skills detected in resume.")
            else:
                st.success("Resume parsed successfully!")

                st.write("### 🛠 Extracted Skills")
                st.write(", ".join(s.title() for s in extracted_skills))

                user_skills = extracted_skills
    # ==================================================
    # RECOMMENDATION ENGINE (UNCHANGED)
    # ==================================================
    if st.button("🎯 Get Recommendations", use_container_width=True):

        st.session_state["user_skills"] = user_skills

        if not user_skills:
            st.warning("Please provide skills (manual selection or resume upload).")
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

            selected_skill = st.selectbox(
                "Skills from Recommended Jobs",
                recommended_skills
                #horizontal=True
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
