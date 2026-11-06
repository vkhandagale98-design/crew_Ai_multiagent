
import json

def make_download(profile, plan, markdown=False):
    if not markdown:
        return json.dumps({"student_profile": profile, "career_plan": plan}, indent=2, ensure_ascii=False)

    lines = ["# Student Career Guidance Plan", "", "## Student profile"]
    for key, value in profile.items():
        lines.append(f"- **{key.replace('_', ' ').title()}:** {', '.join(value) if isinstance(value, list) else value}")
    lines += ["", "## Profile summary", plan.get("profile_summary", "")]
    lines += ["", "## Recommended career paths"]
    for role in plan.get("career_paths", []):
        lines += [f"### {role.get('role', 'Career role')}", role.get("why_it_fits", ""), "",
                  "**Responsibilities**"]
        lines += [f"- {x}" for x in role.get("responsibilities", [])]
        lines += ["", "**Required skills**", ", ".join(role.get("required_skills", []))]
        lines += ["", "**Certifications**"]
        lines += [f"- {x}" for x in role.get("certifications", [])]
        lines.append("")
    gaps = plan.get("skill_gap", {})
    lines += ["## Skill-gap analysis", "", "**Existing skills**"]
    lines += [f"- {x}" for x in gaps.get("existing_skills", [])]
    lines += ["", "**Skills to develop**"]
    lines += [f"- {x}" for x in gaps.get("missing_skills", [])]
    lines += ["", "## Learning roadmap"]
    for stage in plan.get("roadmap", []):
        lines += [f"### {stage.get('stage', '')}", stage.get("goal", ""),
                  f"- **Topics:** {', '.join(stage.get('topics', []))}"]
        lines += [f"- {x}" for x in stage.get("activities", [])]
        lines += [f"- **Project:** {stage.get('project', '')}", ""]
    lines += ["## Learning resources"]
    for r in plan.get("learning_resources", []):
        lines.append(f"- [{r.get('name', '')}]({r.get('url', '')}) — {r.get('purpose', '')}")
    lines += ["", "## Job-search resources"]
    for r in plan.get("job_search_resources", []):
        lines.append(f"- [{r.get('name', '')}]({r.get('url', '')}) — {r.get('purpose', '')}")
    lines += ["", "> Career guidance is informational. Verify current course details, eligibility and job postings on official websites."]
    return "\n".join(lines)
