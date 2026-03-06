import subprocess
import json
import re


def safe_json_from_llm(text: str):
    """
    Extracts and safely parses JSON from LLM output.
    """

    # Remove non-printable characters
    text = re.sub(r"[\x00-\x1F\x7F]", "", text)

    try:
        return json.loads(text)
    except:
        pass

    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON found in LLM output")

    json_text = match.group()

    json_text = re.sub(r",\s*}", "}", json_text)
    json_text = re.sub(r",\s*]", "]", json_text)

    return json.loads(json_text)


def generate_mcqs(skill: str):
    """
    Generates 5 MCQs with sub-topics for a given skill
    """

    prompt = f"""
You are an expert technical interviewer.

Generate exactly 5 multiple-choice questions to assess knowledge of the skill: "{skill}".

Rules:
- Each question must have exactly 4 options (A, B, C, D)
- Only ONE option is correct
- Difficulty: beginner to intermediate
- Each question MUST include a sub-topic label
- Output MUST be valid JSON ONLY in this format:

{{
  "skill": "{skill}",
  "questions": [
    {{
      "question": "...",
      "topic": "Sub-topic name",
      "options": {{
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
      }},
      "answer": "A"
    }}
  ]
}}

DO NOT add explanations.
DO NOT add markdown.
DO NOT add extra text.
"""

    result = subprocess.run(
        ["ollama", "run", "gpt-oss:120b-cloud"], 
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True
    )

    raw_output = result.stdout.strip()

    try:
        return safe_json_from_llm(raw_output)
    except:
        return {"skill": skill, "questions": []}


def generate_learning_resources(skill: str):
    """
    Generates structured learning resources safely
    """

    prompt = f"""
Suggest learning resources to improve the skill "{skill}".

Return VALID JSON ONLY in this format:

{{
  "books": [
    {{ "title": "...", "reason": "..." }}
  ],
  "courses": [
    {{ "title": "...", "platform": "...", "reason": "..." }}
  ]
}}

Rules:
- 2 books
- 2 courses
- No markdown
- No extra text
"""

    result = subprocess.run(
        ["ollama", "run", "gpt-oss:120b-cloud"],
        input=prompt,
        text=True,
        encoding="utf-8",
        errors="ignore",
        capture_output=True
    )

    try:
        return safe_json_from_llm(result.stdout)
    except:
        return {
            "books": [],
            "courses": []
        }
