import pdfplumber
import json
import subprocess
import re
from typing import Dict


def extract_text_from_pdf(file) -> str:
    """
    Extract raw text from uploaded PDF file using pdfplumber.
    """
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    return text.strip()


def llm_call(prompt: str) -> str:
    """
    Calls Ollama model: gpt-oss:120b-cloud
    """

    result = subprocess.run(
        ["ollama", "run", "gpt-oss:120b-cloud"],
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True
    )

    return result.stdout.strip()


def extract_json(text: str) -> str:
    """
    Safely extract JSON from LLM output.
    Handles reasoning text like 'Thinking...' or markdown blocks.
    """

    # remove markdown blocks
    text = text.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group(0)

    raise ValueError("No JSON found in LLM output")


def parse_resume_with_llm(resume_text: str) -> Dict:
    """
    Use LLM to extract structured information from resume text.
    """

    prompt = f"""
You are a resume parsing engine.

Extract the following fields from the resume.

Return ONLY valid JSON.

Schema:
{{
  "skills": [],
  "job_titles": [],
  "education": "",
  "years_experience": ""
}}

Rules:
- Extract ONLY what exists in the resume
- Do NOT invent skills
- Skills must be a list of strings

Resume:
{resume_text}
"""

    response = llm_call(prompt)

    try:
        json_text = extract_json(response)

        parsed = json.loads(json_text)

        structured = {
            "skills": parsed.get("skills", []),
            "job_titles": parsed.get("job_titles", []),
            "education": parsed.get("education", ""),
            "years_experience": parsed.get("years_experience", "")
        }

    except Exception:
        structured = {
            "skills": [],
            "job_titles": [],
            "education": "",
            "years_experience": ""
        }

    return structured


def parse_resume(file) -> Dict:
    """
    Full pipeline:
    PDF → Text → LLM → Structured JSON
    """

    text = extract_text_from_pdf(file)

    structured_data = parse_resume_with_llm(text)

    # Normalize skills safely
    structured_data["skills"] = [
        skill.lower().strip()
        for skill in structured_data.get("skills", [])
        if isinstance(skill, str)
    ]

    return structured_data