from typing import List, Dict
from pymongo import MongoClient
from src.helper import extract_skills_from_description
from src.skill_graph import SKILL_GRAPH, CATEGORY_ALIASES

client = MongoClient("mongodb://localhost:27017/")
db = client["job_recommender"]
jobs_col = db["jobs"]

PRIMARY_WEIGHT = 5
DIRECT_MATCH_WEIGHT = 3
CATEGORY_MATCH_WEIGHT = 2
RELATED_MATCH_WEIGHT = 1


def normalize(skill: str) -> str:
    return skill.strip().lower()


def recommend_jobs(user_skills: List[str], top_n: int = 5) -> List[Dict]:
    if not user_skills:
        return []

    user_skills = list(set(map(normalize, user_skills)))
    recommendations = []

    for job in jobs_col.find():
        job_skills = job.get("skills_required", [])

        if not job_skills:
            job_skills = extract_skills_from_description(job.get("description", ""))
            job["skills_required"] = job_skills

        job_skills = list(set(map(normalize, job_skills)))
        title = normalize(job.get("title", ""))

        score = 0
        explanation = {
            "direct": [],
            "category": [],
            "related": [],
            "title_boost": []
        }

        # -------- Direct Matches --------
        for us in user_skills:
            if us in job_skills:
                score += DIRECT_MATCH_WEIGHT
                explanation["direct"].append(us)

        # -------- Category Partial Match --------
        for cat, skills in CATEGORY_ALIASES.items():
            if cat in job_skills:
                for us in user_skills:
                    if us in skills:
                        score += CATEGORY_MATCH_WEIGHT
                        explanation["category"].append(f"{us} → {cat}")

        # -------- Related Skills --------
        for us in user_skills:
            for rs in SKILL_GRAPH.get(us, {}).get("related", []):
                if rs in job_skills:
                    score += RELATED_MATCH_WEIGHT
                    explanation["related"].append(f"{us} → {rs}")

        # -------- Title Priority Boost --------
        for us in user_skills:
            if us in title and us in job_skills:
                score += PRIMARY_WEIGHT
                explanation["title_boost"].append(us)

        if score == 0:
            continue

        max_possible = len(job_skills) * PRIMARY_WEIGHT
        final_score = min(int((score / max_possible) * 100), 100)

        skill_gaps = sorted(set(job_skills) - set(user_skills))

        recommendations.append({
            "job": job,
            "match_score": final_score,
            "explanation": explanation,
            "skill_gaps": skill_gaps
        })

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    return recommendations[:top_n]
