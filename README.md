
# Generative AI-Based Student Career Guidance Assistant

A Streamlit application that creates personalized career guidance using a curated career knowledge base and an optional Groq LLM.

## Features

- Collects only career-relevant student information.
- Recommends up to three career paths and explains fit.
- Separates current skills from skills to develop.
- Creates a three-stage learning roadmap with practice activities and project ideas.
- Includes learning and job-search resources.
- Exports the plan as JSON or Markdown.
- Includes four sample student profiles.
- Works without an API key using a transparent rule-based knowledge-base fallback.

## 1. Requirements

Recommended: Python 3.11 or 3.12. Some AI and Streamlit dependencies may not yet support the newest Python releases. If you have Python 3.15 installed, install Python 3.12 alongside it and use the `py -3.12` launcher.

## 2. Open the project folder

Open this folder in PyCharm or a terminal.

## 3. Create and activate a virtual environment (Windows PowerShell)

```powershell
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
venv\Scripts\activate.bat
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 5. Configure Groq (optional)

1. Create or use an API key from the Groq developer console.
2. Copy `.env.example` to a file named `.env`.
3. Replace the placeholder with your own key:

```env
GROQ_API_KEY=your_actual_key
GROQ_API_MODEL=openai/gpt-oss-120b
```

Do not share your API key, commit `.env` to GitHub, or paste it into source code. If a key was previously exposed publicly, revoke it and create a new one.

The app still runs without a key, using the local career knowledge base.

## 6. Run the application

```bash
streamlit run app.py
```

Streamlit prints a local URL, usually `http://localhost:8501`. Open it in your browser.

## 7. Test the four sample profiles

Choose one from **Load a sample profile**:

1. B.Com — Finance
2. Mechanical — Automobiles
3. Computer Science — AI
4. MBA — Business Analytics

Click **Generate Career Plan**.

## Project structure

```text
student_career_guidance_assistant/
│
├── app.py
├── career_engine.py
├── llm_service.py
├── utils.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── data/
│   └── career_knowledge.json
│
└── tests/
    └── test_career_engine.py
```

## How it works

1. `app.py` collects the student's profile through a Streamlit form.
2. `llm_service.py` sends the profile and curated knowledge base to Groq, if configured.
3. The model returns structured JSON containing roles, skills, roadmap and resources.
4. If the API key is missing or the request fails, `career_engine.py` generates a local fallback plan.
5. `utils.py` exports the plan as JSON or Markdown.

## Important notes

- Resource websites are official provider or platform entry points. Course enrollment, fees, eligibility, certification rules and availability can change; verify them on the provider's website.
- Job portals are search links, not claims of live vacancies.
- Recommendations are guidance, not a guarantee of employment.
- For a production deployment, add stronger input validation, API usage limits, privacy notices, logging controls and human review.
