# 🧠 AI-Powered Career Navigation System

An end-to-end **AI-driven career intelligence platform** designed to help users explore real job market data, understand skill requirements, assess readiness, and follow a personalized learning roadmap to become job-ready.

---

## 📌 Table of Contents

- [Project Overview](#project-overview)
- [System Features](#system-features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [How to Run the Application](#how-to-run-the-application)
- [Application Modules](#application-modules)
- [Database Schema](#database-schema)
- [AI & Recommendation Logic](#ai--recommendation-logic)
- [MCQ & Learning Resource Generation](#mcq--learning-resource-generation)
- [UI/UX Design Principles](#uiux-design-principles)
- [Known Limitations](#known-limitations)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## 📘 Project Overview

The **AI-Powered Career Navigation System** bridges the gap between job seekers and real-world job requirements by combining:

- Live job data scraping  
- Skill-based job recommendations  
- AI-powered skill assessments  
- Personalized learning resources and roadmaps  

The platform guides users from **job discovery → skill assessment → improvement → career readiness** in one unified system.

---

## 🚀 System Features

### 🔍 Job Intelligence
- Real-time job scraping from **Merojob**
- Structured job storage using MongoDB
- Full-text search across jobs

### 🤖 AI Job Recommendations
- Skill-based matching logic
- Transparent matched skills and skill gaps
- Personalized job suggestions

### 🧠 Skill Self-Assessment
- AI-generated MCQs per skill
- Automated scoring
- Topic-wise weak area detection

### 📚 Learning Recommendations
- Curated books and online courses
- Generated dynamically based on assessment results

### 📈 Career Roadmaps
- Phase-wise learning guidance
- Role-specific preparation paths

### 🎨 Professional UI/UX
- Sidebar-based navigation
- Dashboard-style layout
- Clean, modern dark theme

---

## 🏗️ System Architecture

┌────────────┐
│ Streamlit │ ← User Interface
└─────┬──────┘
│
┌─────▼────────────┐
│ Application Core │
│ (Recommender, │
│ MCQ Engine) │
└─────┬────────────┘
│
┌─────▼────────────┐
│ MongoDB Database │
│ (Job Storage) │
└─────┬────────────┘
│
┌─────▼────────────┐
│ Web Scraper │
│ (Merojob) │
└─────────────────┘


---

## 🧰 Tech Stack

### Frontend
- Streamlit
- Custom CSS (Dashboard UI, Dark Theme)

### Backend
- Python 3.10+
- Modular service-based architecture

### Database
- MongoDB
- PyMongo

### AI / Logic
- Skill matching & rule-based intelligence
- Prompt-based MCQ and learning resource generation

---

## 📂 Project Structure

major_project/
│
├── app.py # Main Streamlit application
├── src/
│ ├── job_api.py # Job scraping logic
│ ├── recommender.py # Job recommendation engine
│ ├── mcq_engine.py # MCQ & learning resource generator
│
├── requirements.txt
├── README.md
└── .venv/


---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/job-intelligence-platform.git
cd job-intelligence-platform
2️⃣ Create Virtual Environment
python -m venv .venv
.venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Start MongoDB
Ensure MongoDB is running locally:

mongodb://localhost:27017/
▶️ How to Run the Application
streamlit run app.py
The application will automatically open in your default web browser.

🧩 Application Modules
🏠 Dashboard
Overview of system capabilities

Non-scrollable, card-based layout

Entry point for users

🕷️ Scrape & Search Jobs
Scrapes real-time job data from Merojob

Stores unique job postings in MongoDB

Search jobs by title, company, skills, or description

🤖 Job Recommendations
User inputs their skills

System matches skills with job requirements

Displays matched skills and missing skill gaps

📝 Skill Self-Assessment
Skill-specific MCQs

Automatic scoring (out of 100)

Weak topic identification

Learning resources generated after submission

📈 Learning Roadmap
Structured learning phases

Skill prioritization

Role-based guidance

🗄️ Database Schema
Jobs Collection
{
  "title": "Backend Developer",
  "company": "ABC Tech",
  "location": "Kathmandu",
  "description": "Job description text",
  "skills_required": ["Python", "Django", "REST API"],
  "url": "https://example.com/job"
}
🤖 AI & Recommendation Logic
Skill Matching Logic
Normalizes skills to lowercase

Matches user skills against job-required skills

Matched Skills = User Skills ∩ Job Skills
Skill Gap = Job Skills − User Skills
🧠 MCQ & Learning Resource Generation
MCQs generated dynamically per selected skill

Each question includes a topic label

Weak areas detected automatically

Learning resources include:

📚 Books

🎓 Online courses

🎨 UI/UX Design Principles
Sidebar navigation (replaces tabs)

Dashboard-first design

Minimal scrolling

Card-based information layout

Professional dark theme

⚠️ Known Limitations
Single job source (Merojob)

No user authentication

MCQ difficulty is static

Roadmaps are template-based

🔮 Future Enhancements
Multi-source job scraping

User login and profile persistence

Adaptive MCQ difficulty

Resume parsing & ATS scoring

Advanced NLP skill embeddings

Exportable reports (PDF)