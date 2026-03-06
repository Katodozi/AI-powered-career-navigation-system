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

    # Normalize and remove duplicates + short skills
    user_skills = list({
        normalize(s) for s in user_skills
        if isinstance(s, str) and len(normalize(s)) > 1
    })

    user_skill_set = set(user_skills)

    recommendations = []

    for job in jobs_col.find():

        job_skills = job.get("skills_required", [])

        if not job_skills:
            job_skills = extract_skills_from_description(job.get("description", ""))
            job["skills_required"] = job_skills

        job_skills = list({
            normalize(s) for s in job_skills
            if isinstance(s, str) and len(normalize(s)) > 1
        })

        job_skill_set = set(job_skills)

        title = normalize(job.get("title", ""))

        score = 0

        explanation = {
            "direct": [],
            "category": [],
            "related": [],
            "title_boost": []
        }

        # -------- Direct Matches --------
        direct_matches = user_skill_set.intersection(job_skill_set)

        for skill in direct_matches:
            score += DIRECT_MATCH_WEIGHT
            explanation["direct"].append(skill)

        # -------- Category Partial Match --------
        for cat, skills in CATEGORY_ALIASES.items():

            cat = normalize(cat)

            if cat in job_skill_set:

                for us in user_skill_set:
                    if us in skills:
                        score += CATEGORY_MATCH_WEIGHT
                        explanation["category"].append(f"{us} → {cat}")

        # -------- Related Skills --------
        for us in user_skill_set:

            related_skills = SKILL_GRAPH.get(us, {}).get("related", [])

            for rs in related_skills:
                rs = normalize(rs)

                if rs in job_skill_set:
                    score += RELATED_MATCH_WEIGHT
                    explanation["related"].append(f"{us} → {rs}")

        # -------- Title Priority Boost --------
        for us in user_skill_set:

            if us in job_skill_set and f" {us} " in f" {title} ":
                score += PRIMARY_WEIGHT
                explanation["title_boost"].append(us)

        if score == 0:
            continue

        # -------- Final Score --------
        max_possible = max(len(job_skill_set) * PRIMARY_WEIGHT, 1)

        final_score = min(int((score / max_possible) * 100), 100)

        skill_gaps = sorted(job_skill_set - user_skill_set)

        recommendations.append({
            "job": job,
            "match_score": final_score,
            "explanation": explanation,
            "skill_gaps": skill_gaps
        })

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)

    return recommendations[:top_n]
