from typing import List, Dict
from pymongo import MongoClient
from src.helper import extract_skills_from_description

client = MongoClient("mongodb://localhost:27017/")
db = client["job_recommender"]
jobs_col = db["jobs"]

def recommend_jobs(user_skills: List[str], top_n: int = 5) -> List[Dict]:
    """
    Recommend jobs based on user's skills.
    
    Args:
        user_skills (List[str]): List of skills input by the user.
        top_n (int): Number of top jobs to return.
    
    Returns:
        List[Dict]: List of recommended job documents with matched skills.
    """
    if not user_skills:
        return []

    # Normalize user skills
    user_skills_normalized = [skill.strip().lower() for skill in user_skills]

    recommendations = []

    for job in jobs_col.find():
        # Extract skills from job description if not already present
        job_skills = job.get("skills_required", [])
        if not job_skills:
            job_skills = extract_skills_from_description(job.get("description", ""))
            job["skills_required"] = job_skills  # optional: update DB for future use

        job_skills_normalized = [skill.lower() for skill in job_skills]

        # Find matched skills
        matched = list(set(user_skills_normalized) & set(job_skills_normalized))
        score = len(matched)

        if score > 0:
            recommendations.append({
                "job": job,
                "matched_skills": matched,
                "score": score
            })

    # Sort by descending score (most matches first)
    recommendations = sorted(recommendations, key=lambda x: x["score"], reverse=True)

    # Return only top_n jobs
    return recommendations[:top_n]
