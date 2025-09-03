import json
import os
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def tailor_resume_with_jd(resume_json: dict, job_description: str, use_demo: bool = False) -> dict:
    """
    Tailor resume JSON according to a job description.
    If use_demo=True, load from demo.json instead of calling OpenAI.
    """

    if use_demo:
        demo_path = os.path.join(os.path.dirname(__file__), "demo.json")
        with open(demo_path, "r", encoding="utf-8") as f:
            return json.load(f)

    prompt = f"""
    You are an expert resume writer.
    Given the resume JSON and the job description below,
    rewrite the SUMMARY, SKILLS, EXPERIENCE, and PROJECTS to highlight
    the most relevant aspects for this JD.

    - Keep all content truthful (do not invent fake experiences).
    - Improve impact with action verbs and metrics if possible.
    - Ensure ATS-friendly phrasing (keywords from JD).
    - Return valid JSON only.

    Resume JSON:
    {json.dumps(resume_json, indent=2)}

    Job Description:
    {job_description}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    tailored_json = json.loads(response.choices[0].message.content)
    return tailored_json
