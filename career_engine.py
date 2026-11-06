
import json
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "career_knowledge.json"

def load_knowledge():
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

def _tokens(values):
    return {word.lower().strip(".,-/") for value in values for word in value.lower().replace("&", " ").split()}

def generate_rule_based_plan(profile):
    """Transparent fallback used when no LLM key is configured or the API is unavailable."""
    knowledge = load_knowledge()
    interests = _tokens(profile.get("interests", []))
    skills = _tokens(profile.get("skills", []))
    industry = profile.get("industry", "").lower()
    goal = profile.get("goal", "").lower()

    scored = []
    for role in knowledge["roles"]:
        role_text = " ".join([
            role["role"], role["industry"], role["why_relevant"],
            " ".join(role["required_skills"]), " ".join(role["keywords"])
        ]).lower()
        score = sum(2 for token in interests if len(token) > 2 and token in role_text)
        score += sum(1 for token in skills if len(token) > 2 and token in role_text)
        if industry != "not sure yet" and industry in role["industry"].lower():
            score += 3
        if any(word in role["role"].lower() for word in goal.split() if len(word) > 3):
            score += 3
        scored.append((score, role))

    selected = [role for _, role in sorted(scored, key=lambda x: x[0], reverse=True)[:3]]
    if not selected:
        selected = knowledge["roles"][:3]

    required = []
    for role in selected:
        required.extend(role["required_skills"])
    required_unique = list(dict.fromkeys(required))
    existing = profile.get("skills", [])
    existing_tokens = _tokens(existing)
    missing = [skill for skill in required_unique if skill.lower() not in existing_tokens]

    roadmap = []
    stages = [
        ("Stage 1 — Foundations", "Build core concepts and vocabulary", 0, 3),
        ("Stage 2 — Applied skills", "Practice tools and job-relevant techniques", 3, 6),
        ("Stage 3 — Portfolio and readiness", "Demonstrate ability through projects and interview preparation", 6, 9),
    ]
    for title, goal_text, start, end in stages:
        stage_skills = missing[start:end]
        roadmap.append({
            "stage": title,
            "goal": goal_text,
            "topics": stage_skills or required_unique[:3],
            "activities": [
                "Complete a structured course or guided module.",
                "Practice with a small real-world exercise and document what you learned."
            ],
            "project": selected[0]["project_ideas"][0] if selected and selected[0].get("project_ideas") else "Create a small portfolio project related to your target role."
        })

    resources = knowledge["learning_resources"]
    return {
        "profile_summary": (
            f"Based on your {profile.get('degree') or profile.get('qualification')} background, "
            f"interests in {', '.join(profile.get('interests', []))}, and goal to {profile.get('goal')}, "
            "these are starting career directions. Validate them through projects, conversations with professionals and internships."
        ),
        "career_paths": [{
            "role": r["role"],
            "why_it_fits": r["why_relevant"],
            "responsibilities": r["responsibilities"],
            "required_skills": r["required_skills"],
            "qualification": r["qualification"],
            "certifications": r["certifications"],
        } for r in selected],
        "skill_gap": {
            "existing_skills": existing,
            "missing_skills": missing[:12],
            "actions": [
                "Prioritize two missing skills that appear across more than one recommended role.",
                "Practice each skill through a small project and add evidence to a portfolio.",
                "Ask a mentor or professional to review your work."
            ]
        },
        "roadmap": roadmap,
        "learning_resources": resources,
        "job_search_resources": knowledge["job_search_resources"],
        "disclaimer": "Recommendations are informational and should be validated against current employer requirements."
    }
