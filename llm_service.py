
import json
import os
import re
from groq import Groq
from career_engine import load_knowledge

def _extract_json(text):
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("The model did not return a JSON object.")
    return json.loads(text[start:end + 1])

def generate_ai_plan(profile):
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key or api_key == "your_groq_api_key_here":
        return None, "Knowledge-base mode (no API key configured)"

    model = os.getenv("GROQ_API_MODEL", "openai/gpt-oss-120b").strip()
    knowledge = load_knowledge()
    client = Groq(api_key=api_key)

    prompt = f"""
Create a practical career guidance plan for this student using ONLY the supplied career knowledge base
for role facts, certification names and URLs. You may tailor explanations and learning sequence.
Do not invent live vacancies, salary figures, guaranteed outcomes, course availability or credentials.
Recommend exactly 3 suitable roles when possible. Explain why each role fits this student's profile.
Separate skills the student already has from skills they need to develop.
Create a realistic roadmap in 3 stages. Keep recommendations suitable for the student's education level.
Return ONLY valid JSON with this exact structure:
{{
 "profile_summary": "string",
 "career_paths": [
  {{"role":"", "why_it_fits":"", "responsibilities":[""], "required_skills":[""], "qualification":"", "certifications":[""]}}
 ],
 "skill_gap": {{"existing_skills":[""], "missing_skills":[""], "actions":[""]}},
 "roadmap": [
  {{"stage":"", "goal":"", "topics":[""], "activities":[""], "project":""}}
 ],
 "learning_resources": [{{"name":"", "url":"", "purpose":""}}],
 "job_search_resources": [{{"name":"", "url":"", "purpose":""}}],
 "disclaimer":""
}}
Use only resource URLs found in the knowledge base. Return 3 roadmap stages.
STUDENT PROFILE:
{json.dumps(profile, ensure_ascii=False)}
CAREER KNOWLEDGE BASE:
{json.dumps(knowledge, ensure_ascii=False)}
"""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a careful student career counsellor. Be realistic, specific and transparent. Output valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=5000,
        )
        content = response.choices[0].message.content or ""
        plan = _extract_json(content)
        if not isinstance(plan.get("career_paths"), list) or not plan["career_paths"]:
            raise ValueError("Career paths were missing from the response.")
        plan["career_paths"] = plan["career_paths"][:3]
        return plan, f"Groq AI ({model})"
    except Exception as exc:
        # Keep the app usable if the API is down, rate-limited or returns malformed output.
        return None, f"Knowledge-base fallback (AI request failed: {type(exc).__name__})"
