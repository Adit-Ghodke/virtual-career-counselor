"""
Groq AI service — wrappers for all AI-powered features.
Uses groq Python SDK (latest Context7 patterns).
Automatically enriched with Tavily AI web search for real-time data.
"""
import os
import logging
from typing import Any, Dict, List, Optional, Tuple
from groq import Groq
from flask import current_app

logger: logging.Logger = logging.getLogger(__name__)

_client: Optional[Groq] = None


def _get_client() -> Groq:
    """Lazy-initialise and reuse the Groq client."""
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    return _client


def _enrich_with_web_search(user_prompt: str) -> Tuple[str, str]:
    """
    Call Tavily web search and return (enriched_prompt_prefix, sources_markdown).
    Falls back gracefully if search is unavailable.
    """
    try:
        from app.services.web_search_service import search_web, format_sources_markdown
        result: Dict[str, Any] = search_web(user_prompt, max_results=5, search_depth="basic")
        if result["success"] and result["context"]:
            prefix: str = (
                "\n\n[REAL-TIME WEB CONTEXT — use this to ground your answer with current data]\n"
                f"{result['context']}\n"
                "[END WEB CONTEXT]\n\n"
            )
            sources_md: str = format_sources_markdown(result["sources"])
            return prefix, sources_md
    except Exception as e:
        logger.debug(f"Web search enrichment skipped: {e}")
    return "", ""


def _chat(system_prompt: str, user_prompt: str, web_search: bool = True) -> str:
    """Send a system+user message pair and return the assistant text.
    Automatically enriches with Tavily web search unless web_search=False.
    """
    enrichment: str = ""
    sources_md: str = ""
    if web_search:
        enrichment, sources_md = _enrich_with_web_search(user_prompt)

    full_user_prompt: str = enrichment + user_prompt if enrichment else user_prompt

    # Add citation instruction to system prompt when web context is present
    effective_system: str = system_prompt
    if enrichment:
        effective_system += (
            "\n\nIMPORTANT: Real-time web search results are provided above the user's question. "
            "Incorporate relevant data points and cite sources where applicable. "
            "If web data conflicts with your knowledge, prefer the web data as it is more current."
        )

    client: Groq = _get_client()
    model: str = str(current_app.config.get("GROQ_MODEL", "llama-3.3-70b-versatile"))  # type: ignore[arg-type]
    completion: Any = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": effective_system},
            {"role": "user", "content": full_user_prompt},
        ],
        temperature=0.7,
        max_tokens=2048,
    )
    response: str = completion.choices[0].message.content or ""

    # Append source citations if available
    if sources_md:
        response += sources_md

    return response


def _multi_turn_chat(messages: List[Dict[str, str]], web_search: bool = True) -> str:
    """Send a full conversation (list of role/content dicts) and return assistant reply.
    Enriches the last user message with web search context.
    """
    enrichment: str = ""
    sources_md: str = ""

    if web_search and messages:
        # Find last user message for web search
        last_user_msg: str = ""
        for msg in reversed(messages):
            if msg["role"] == "user":
                last_user_msg = msg["content"]
                break
        if last_user_msg:
            enrichment, sources_md = _enrich_with_web_search(last_user_msg)

    # Inject web context into system message if present
    enriched_messages: List[Dict[str, str]] = list(messages)
    if enrichment and enriched_messages:
        if enriched_messages[0]["role"] == "system":
            enriched_messages[0] = {
                "role": "system",
                "content": enriched_messages[0]["content"] + (
                    "\n\nIMPORTANT: Real-time web search results are injected in the latest user message. "
                    "Use them to provide current, data-backed answers. Cite sources where applicable."
                ),
            }
        # Inject context into last user message
        for i in range(len(enriched_messages) - 1, -1, -1):
            if enriched_messages[i]["role"] == "user":
                enriched_messages[i] = {
                    "role": "user",
                    "content": enrichment + enriched_messages[i]["content"],
                }
                break

    client: Groq = _get_client()
    model: str = str(current_app.config.get("GROQ_MODEL", "llama-3.3-70b-versatile"))  # type: ignore[arg-type]
    completion: Any = client.chat.completions.create(
        model=model,
        messages=enriched_messages,  # type: ignore[arg-type]
        temperature=0.8,
        max_tokens=1024,
    )
    response: str = completion.choices[0].message.content or ""

    if sources_md:
        response += sources_md

    return response


# ─── Career Path ──────────────────────────────────────────────────────────────

CAREER_SYSTEM = (
    "You are an expert career counselor. Give practical, structured, concise guidance.\n"
    "Output with these exact section headings (use markdown):\n"
    "## 1) Required Skills (Technical + Soft)\n"
    "## 2) Recommended Certifications & Courses\n"
    "## 3) Typical Job Roles and Career Progression\n"
    "## 4) Estimated Time to Enter the Field\n"
    "## 5) Suggested Next 30-Day Action Plan"
)


def generate_career_overview(career_name: str) -> str:
    """Return a structured career overview for the given career."""
    user_prompt = (
        f"Create a comprehensive career overview for: {career_name}.\n"
        "Target audience: students and fresh graduates.\n"
        "Keep it realistic and actionable."
    )
    return _chat(CAREER_SYSTEM, user_prompt)


# ─── Course Recommendations ──────────────────────────────────────────────────

COURSE_SYSTEM = (
    "You are an AI learning advisor.\n"
    "Return 5 to 8 course recommendations. For EACH course use this format:\n"
    "### Course Name\n"
    "- **Platform:** (e.g. Coursera, Udemy, edX)\n"
    "- **Why this course:** one-sentence match reason\n"
    "- **Difficulty:** Beginner / Intermediate / Advanced\n"
    "- **Duration:** estimated hours or weeks\n"
    "- **Outcome:** what the learner will be able to do after completion"
)


def generate_course_recommendations(
    interests: str,
    skill_level: str,
    learning_goals: str,
    time_availability: str,
) -> str:
    """Return personalised course suggestions."""
    user_prompt = (
        f"Recommend courses based on:\n"
        f"- Interests: {interests}\n"
        f"- Current Skill Level: {skill_level}\n"
        f"- Learning Goals: {learning_goals}\n"
        f"- Time Availability: {time_availability} hours/week"
    )
    return _chat(COURSE_SYSTEM, user_prompt)


# ─── Job Market Insights ─────────────────────────────────────────────────────

INSIGHTS_SYSTEM = (
    "You are a labor market analyst. Provide estimated trends "
    "(not real-time scraped data).\n"
    "Output with these exact section headings (use markdown):\n"
    "## 1) Top In-Demand Skills\n"
    "## 2) Salary Range (Entry / Mid / Senior)\n"
    "## 3) Demand Trend (Growing / Stable / Declining) with brief reason\n"
    "## 4) Geographic Hotspots\n"
    "## 5) Hiring Tips for the Next 3 Months"
)


def generate_market_insights(role_or_industry: str) -> str:
    """Return AI-generated job market insights."""
    user_prompt = (
        f"Provide job-market insights for role/industry: {role_or_industry}.\n"
        "Focus on practical guidance for job seekers."
    )
    return _chat(INSIGHTS_SYSTEM, user_prompt)


# ─── Resume Analysis ─────────────────────────────────────────────────────────

RESUME_SYSTEM = (
    "You are an expert resume analyst and career advisor.\n"
    "Analyze the resume text provided and output with these exact section headings (use markdown):\n"
    "## 1) Extracted Skills\n"
    "List all technical and soft skills found in the resume.\n"
    "## 2) Skill Gaps for Target Role\n"
    "Compare extracted skills with the target role requirements. List missing skills.\n"
    "## 3) Personalized Upskilling Roadmap\n"
    "A week-by-week plan to fill the skill gaps (4-8 weeks).\n"
    "## 4) Resume Strengths\n"
    "What's good about this resume.\n"
    "## 5) Resume Improvement Tips\n"
    "Specific actionable improvements.\n"
    "## 6) Matching Job Titles\n"
    "List 5-8 job titles this person is qualified for or close to qualifying for, with match percentage."
)


def analyze_resume(resume_text: str, target_role: str) -> str:
    """Analyze resume text against a target role."""
    user_prompt = (
        f"Here is the resume text:\n\n{resume_text[:4000]}\n\n"
        f"Target Role: {target_role}\n\n"
        "Provide a comprehensive analysis."
    )
    return _chat(RESUME_SYSTEM, user_prompt)


# ─── Learning Path Generator ─────────────────────────────────────────────────

LEARNING_PATH_SYSTEM = (
    "You are a personalized learning path architect.\n"
    "Create a detailed week-by-week learning roadmap. Use this format:\n"
    "## Learning Roadmap: [Role]\n"
    "### Week 1: [Topic]\n"
    "- **Focus:** what to learn\n"
    "- **Resources:** specific courses/tutorials\n"
    "- **Practice:** hands-on project/exercise\n"
    "- **Milestone:** what you should be able to do by end of week\n\n"
    "Repeat for each week. Include 6-12 weeks depending on complexity.\n"
    "At the end add:\n"
    "## Recommended Certifications\n"
    "## Portfolio Projects to Build"
)


def generate_learning_path(target_role: str, current_skills: str, hours_per_day: str) -> str:
    """Generate a personalized week-by-week learning roadmap."""
    user_prompt = (
        f"Create a personalized learning path for:\n"
        f"- Target Role: {target_role}\n"
        f"- Current Skills: {current_skills}\n"
        f"- Available Time: {hours_per_day} hours/day\n\n"
        "Make it practical with real course names and projects."
    )
    return _chat(LEARNING_PATH_SYSTEM, user_prompt)


# ─── Salary Negotiation Simulator ────────────────────────────────────────────

NEGOTIATION_SYSTEM = (
    "You are an HR manager conducting a salary negotiation with a job candidate.\n"
    "Rules:\n"
    "- Play the HR role realistically — push back on the candidate's asks\n"
    "- After each candidate response, give your HR reply AND a brief coaching note in this format:\n"
    "  **HR Response:** [your reply as HR]\n"
    "  **Coach's Note:** [feedback on the candidate's negotiation — what was good/bad, tips]\n"
    "  **Confidence Score:** [rate candidate's response 1-10]\n"
    "- Be challenging but fair\n"
    "- After 4 rounds, end with a final summary:\n"
    "  ## Final Negotiation Score\n"
    "  ## What You Did Well\n"
    "  ## Areas to Improve\n"
    "  ## Recommended Counter-Offer Strategy"
)


def negotiation_reply(conversation_history: List[Dict[str, str]]) -> str:
    """Continue a salary negotiation conversation."""
    return _multi_turn_chat(conversation_history)


# ─── Interview Prep ──────────────────────────────────────────────────────────

INTERVIEW_SYSTEM_TEMPLATE = (
    "You are a senior interviewer at {company} hiring for the role of {role}.\n"
    "Conduct a realistic interview:\n"
    "- Ask one question at a time\n"
    "- Mix behavioral, technical, and situational questions\n"
    "- After the candidate answers, provide:\n"
    "  **Rating:** [1-10]\n"
    "  **Feedback:** [what was good/bad]\n"
    "  **Model Answer:** [ideal answer for this question]\n"
    "  **Next Question:** [your next interview question]\n"
    "- After 5 questions, end with:\n"
    "  ## Overall Interview Score\n"
    "  ## Strengths\n"
    "  ## Areas to Improve\n"
    "  ## Hiring Recommendation (Hire / Maybe / No Hire)"
)


def interview_reply(conversation_history: List[Dict[str, str]]) -> str:
    """Continue an interview simulation conversation."""
    return _multi_turn_chat(conversation_history)


def get_interview_system_prompt(company: str, role: str) -> str:
    """Return a formatted interview system prompt."""
    return INTERVIEW_SYSTEM_TEMPLATE.format(company=company, role=role)


# ─── Career Pivot Analyzer ───────────────────────────────────────────────────

PIVOT_SYSTEM = (
    "You are a career transition specialist.\n"
    "Analyze the career pivot and output with these section headings (use markdown):\n"
    "## 1) Transferable Skills\n"
    "Map skills from current role that apply to target role.\n"
    "## 2) Skill Gaps\n"
    "What's missing and needs to be learned.\n"
    "## 3) Bridge Courses & Certifications\n"
    "Specific courses to bridge the gap (with platforms).\n"
    "## 4) Transition Timeline\n"
    "Realistic month-by-month plan.\n"
    "## 5) Success Stories\n"
    "3-4 real examples of people who made similar transitions.\n"
    "## 6) Potential Challenges & How to Overcome Them\n"
    "## 7) First Steps (Start This Week)"
)


def analyze_career_pivot(current_role: str, years_exp: str, target_role: str, current_skills: str) -> str:
    """Analyze a career pivot from current to target role."""
    user_prompt = (
        f"Analyze this career pivot:\n"
        f"- Current Role: {current_role}\n"
        f"- Years of Experience: {years_exp}\n"
        f"- Target Role: {target_role}\n"
        f"- Current Skills: {current_skills}\n\n"
        "Provide realistic, actionable advice."
    )
    return _chat(PIVOT_SYSTEM, user_prompt)


# ─── Job Market Trends ───────────────────────────────────────────────────────

TRENDS_SYSTEM = (
    "You are a job market research analyst.\n"
    "Provide current market trends data in this exact format (use markdown):\n"
    "## Top 10 In-Demand Skills (2025-2026)\n"
    "Numbered list with brief reason for each.\n"
    "## Fastest Growing Job Roles\n"
    "Top 8 roles with growth percentage estimates.\n"
    "## Salary Comparison by City\n"
    "Compare salaries for tech roles across major cities (table format).\n"
    "## Declining Skills & Technologies\n"
    "Skills losing market demand.\n"
    "## Industry Predictions (Next 6 Months)\n"
    "Key hiring trends and predictions.\n"
    "Note: All data is AI-estimated based on market knowledge, not real-time scraped data."
)


def generate_trends_report(industry: str) -> str:
    """Generate a job market trends report for an industry."""
    user_prompt = (
        f"Generate a comprehensive job market trends report for: {industry}.\n"
        "Include salary data, skill demand, and growth predictions.\n"
        "Use tables where appropriate."
    )
    return _chat(TRENDS_SYSTEM, user_prompt)


# ─── Peer Comparison ─────────────────────────────────────────────────────────

PEER_SYSTEM = (
    "You are a career benchmarking analyst.\n"
    "Given the user's profile, provide a comparison against typical professionals in their target role.\n"
    "Output with these sections (use markdown):\n"
    "## Your Skill Assessment\n"
    "Rate each skill as Beginner/Intermediate/Advanced.\n"
    "## How You Compare to Peers\n"
    "For each skill, show where the user stands vs typical professionals in the target role.\n"
    "## Skills You're Ahead On\n"
    "## Skills You're Behind On\n"
    "## Top 3 Skills to Focus On Next\n"
    "## Your Competitive Edge\n"
    "What makes this user unique compared to others targeting the same role."
)


def generate_peer_comparison(target_role: str, skills: str, experience: str) -> str:
    """Generate a peer comparison analysis."""
    user_prompt = (
        f"Compare this user against peers:\n"
        f"- Target Role: {target_role}\n"
        f"- Current Skills: {skills}\n"
        f"- Experience Level: {experience}\n\n"
        "Be specific and actionable."
    )
    return _chat(PEER_SYSTEM, user_prompt)


# ── NEW FEATURES v3.0 ────────────────────────────────────────────────

CHATBOT_SYSTEM = (
    "You are a friendly, expert AI career counselor chatbot. "
    "Answer any career-related question — job search, skills, interviews, salary, "
    "work-life balance, career changes, education, certifications, freelancing, etc. "
    "Be conversational but give practical, actionable advice. "
    "If the user asks something unrelated to careers, politely redirect them. "
    "Format responses in clear markdown with bullet points and sections where helpful."
)

COVER_LETTER_SYSTEM = (
    "You are an expert cover letter writer. Generate a professional, tailored cover letter. "
    "Output in markdown with these sections:\n"
    "1. **Header** (applicant greeting)\n"
    "2. **Opening Paragraph** — Hook with enthusiasm + why this company\n"
    "3. **Body Paragraph 1** — Key achievements matching the job description\n"
    "4. **Body Paragraph 2** — Skills and cultural fit\n"
    "5. **Closing Paragraph** — Call to action\n"
    "6. **Sign-off**\n\n"
    "Make it specific to the job description. Avoid generic filler. Keep it to ~350 words."
)

GITHUB_SYSTEM = (
    "You are a tech recruiter and code reviewer analyzing a developer's GitHub profile. "
    "Based on the repository information provided, give a thorough analysis with:\n"
    "1. **Profile Score** (out of 100)\n"
    "2. **Top Strengths** — What stands out positively\n"
    "3. **Technology Stack** — Languages/frameworks they use\n"
    "4. **Project Quality Assessment** — Code organization, documentation, activity\n"
    "5. **Areas for Improvement** — What could make the profile stronger\n"
    "6. **Matching Job Roles** — Roles this profile could qualify for\n"
    "7. **Recommended Actions** — Specific next steps to improve the profile\n\n"
    "Be honest but constructive. Format in clean markdown."
)

SKILL_GAP_SYSTEM = (
    "You are a skills assessment expert. Analyze the gap between a user's current skills "
    "and the requirements for their target role. Return a JSON-formatted analysis with:\n"
    "1. A skills breakdown as a JSON array where each item has: "
    '{"skill": "name", "current": 0-100, "required": 0-100, "gap": -100 to 100}\n'
    "2. Overall readiness percentage\n"
    "3. Priority skills to learn (ordered by importance)\n"
    "4. Recommended learning timeline\n\n"
    "Return ONLY valid JSON in this format:\n"
    '{"readiness": 65, "skills": [{"skill": "Python", "current": 80, "required": 90, "gap": -10}], '
    '"priority_skills": ["skill1", "skill2"], "timeline": "3-6 months", '
    '"summary": "Brief text summary of the analysis"}'
)

GD_SYSTEM = (
    "You are simulating a Group Discussion (GD) panel. You play the role of a moderator "
    "AND 3 other panelists (Panelist A, Panelist B, Panelist C) with different viewpoints. "
    "The user is participating in the GD. After each user response:\n"
    "1. Have 1-2 panelists react or add points (with different perspectives)\n"
    "2. Optionally ask a follow-up or change direction\n"
    "3. After 5+ rounds, provide evaluation: Communication (1-10), Content (1-10), "
    "Leadership (1-10), Body Language Tips, Overall Score, and Verdict.\n\n"
    "Format each panelist's dialogue clearly:\n"
    "**Panelist A (agrees):** ...\n"
    "**Panelist B (counters):** ...\n"
    "**Moderator:** ...\n"
    "Keep it realistic and engaging."
)

MENTOR_SYSTEM = (
    "You are a senior career mentor with 20+ years of industry experience. "
    "You remember the user's career context provided below and give personalized guidance. "
    "Be warm, encouraging but realistic. Ask follow-up questions to understand deeper. "
    "Give concrete action items. Share relevant anecdotes when appropriate. "
    "Format responses in markdown."
)

RAG_ENHANCED_SYSTEM = (
    "You are an expert career counselor with access to the latest industry data. "
    "Use the CONTEXT provided below to ground your responses in real data and statistics. "
    "Always cite which source you're referencing. If the context doesn't cover something, "
    "use your general knowledge but note it's not from the provided data.\n\n"
    "CONTEXT:\n{context}\n\n"
    "Answer the user's question based on the above context and your expertise."
)


def chatbot_reply(messages: List[Dict[str, str]]) -> str:
    """Handle multi-turn chatbot conversation."""
    return _multi_turn_chat(messages)


def generate_cover_letter(resume_text: str, job_description: str, company_name: str) -> str:
    """Generate a tailored cover letter."""
    user_prompt = (
        f"Write a cover letter for a position at **{company_name}**.\n\n"
        f"**Job Description:**\n{job_description[:2000]}\n\n"
        f"**My Resume/Background:**\n{resume_text[:2000]}\n\n"
        "Tailor the letter specifically to this role and company."
    )
    return _chat(COVER_LETTER_SYSTEM, user_prompt)


def analyze_github_profile(repos_info: str) -> str:
    """Analyze GitHub profile based on repository data."""
    user_prompt = (
        f"Analyze this developer's GitHub profile:\n\n{repos_info}\n\n"
        "Give a thorough assessment of their profile strength and job readiness."
    )
    return _chat(GITHUB_SYSTEM, user_prompt)


def analyze_skill_gap(current_skills: str, target_role: str, experience: str) -> str:
    """Return JSON skill gap analysis."""
    user_prompt = (
        f"Analyze the skill gap:\n"
        f"- Current Skills: {current_skills}\n"
        f"- Target Role: {target_role}\n"
        f"- Experience: {experience}\n\n"
        "Return ONLY the JSON with no extra text."
    )
    return _chat(SKILL_GAP_SYSTEM, user_prompt)


def group_discussion_reply(messages: List[Dict[str, str]]) -> str:
    """Handle multi-turn group discussion."""
    return _multi_turn_chat(messages)


def mentor_reply(messages: List[Dict[str, str]]) -> str:
    """Handle multi-turn mentor conversation."""
    return _multi_turn_chat(messages)


def rag_enhanced_query(user_question: str, rag_context: str) -> str:
    """Answer a question using RAG-injected context."""
    system = RAG_ENHANCED_SYSTEM.replace("{context}", rag_context)
    return _chat(system, user_question)


def generate_weekly_digest(industries: List[str]) -> str:
    """Generate a weekly career digest for specified industries."""
    industries_str: str = ", ".join(industries)
    system: str = (
        "You are a career newsletter writer. Create a concise weekly digest covering:\n"
        "1. **Hot Jobs This Week** — 5 trending roles\n"
        "2. **Skill of the Week** — One skill gaining demand\n"
        "3. **Industry Updates** — Brief updates per industry\n"
        "4. **Pro Tip** — One actionable career tip\n"
        "5. **Upcoming Events** — 2-3 relevant webinars/conferences\n\n"
        "Keep it concise, engaging, and actionable. Use markdown formatting."
    )
    return _chat(system, f"Generate a weekly career digest for these industries: {industries_str}")
