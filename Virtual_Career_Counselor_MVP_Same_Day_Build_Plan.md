# Virtual Career Counselor — Same-Day MVP Build Plan

**Project:** Virtual Career Counselor  
**Version:** v3.0 (February 2026)  
**Tech Stack:** Flask 3.1 + Groq API (Llama 3.3 70B) + AWS (EC2, DynamoDB, SNS, IAM) + Bootstrap 5.3 + Chart.js 4.4  
**Target:** Fully deployed, feature-rich MVP by end of today  
**New in v2.0:** 8 killer AI-powered features — Resume Analysis, Learning Path, Salary Negotiation Simulator, Interview Prep, Career Pivot Analyzer, Market Trends Dashboard, Peer Comparison, Gamification (Badges & Leaderboard)  
**New in v3.0:** 16 advanced features — AI Chatbot (RAG-enhanced), Cover Letter Generator, GitHub Profile Analyzer, Skill Gap Heatmap, Query History & PDF Export, Dark Mode, Bookmarks, Voice Input, Mock Group Discussion, AI Mentor Chat, RAG Job Matching, Weekly Digest, Team/Classroom Mode, Multi-language support

## IMPORTANT — Use Context7 for Latest Tech

Before implementing any major feature, use Context7 to fetch the latest official documentation and examples for:
- Flask and Flask-Session
- Groq Python SDK
- boto3 (DynamoDB, SNS, IAM usage)
- Gunicorn and Nginx deployment best practices

This is mandatory for this project to avoid outdated code patterns and to ensure you use current libraries, APIs, and recommended configurations.

**Execution Rule:** At the start of each phase, quickly verify package versions and implementation examples from Context7, then apply that guidance in code.

---

## 1) Build Day Strategy (Finish Today)

### Recommended Timebox (16 Hours)
- **Phase 0 (30 min):** Prerequisites, repo scaffold, secrets management
- **Phase 1 (90 min):** Authentication + session management + Users table
- **Phase 2 (90 min):** Career Path AI feature + query persistence
- **Phase 3 (90 min):** Course Recommendation AI feature + persistence
- **Phase 4 (75 min):** Job Market Insights AI feature + persistence
- **Phase 5 (60 min):** SNS notifications (welcome + report emails)
- **Phase 6 (75 min):** Admin dashboard (users, queries, health)
- **Phase 7 (45 min):** Resume Analysis + Job Matching (AI)
- **Phase 8 (45 min):** Personalized Learning Path with Progress Tracking
- **Phase 9 (60 min):** Salary Negotiation Simulator (multi-turn AI chat)
- **Phase 10 (60 min):** Interview Prep Simulator (company-specific AI)
- **Phase 11 (30 min):** Career Pivot Analyzer (AI)
- **Phase 12 (30 min):** Real-Time Market Trends Dashboard (AI)
- **Phase 13 (30 min):** Peer Comparison & Benchmarking (AI)
- **Phase 14 (30 min):** Gamification — Badges & Leaderboard + 3 new DynamoDB tables
- **Phase 15 (30 min):** AI Chatbot with RAG toggle
- **Phase 16 (30 min):** Cover Letter Generator (AI)
- **Phase 17 (30 min):** GitHub Profile Analyzer (GitHub API + AI)
- **Phase 18 (30 min):** Skill Gap Heatmap (AI + Chart.js)
- **Phase 19 (30 min):** Query History + PDF Export
- **Phase 20 (20 min):** Bookmarks (save/remove AI results)
- **Phase 21 (20 min):** Dark Mode (CSS + JS + localStorage)
- **Phase 22 (15 min):** Voice Input (Web Speech API)
- **Phase 23 (45 min):** Mock Group Discussion (multi-round AI-moderated)
- **Phase 24 (30 min):** AI Mentor Chat (persistent goal-based mentorship)
- **Phase 25 (30 min):** RAG Job Matching (TF-IDF knowledge base)
- **Phase 26 (30 min):** Weekly Career Digest (15 industries)
- **Phase 27 (30 min):** Team/Classroom Mode (create/join/share)
- **Phase 28 (60 min):** Navigation overhaul + Dashboard redesign (22 features)
- **Phase 29 (90 min):** QA + bug fix pass + hardening
- **Phase 30 (60 min):** EC2 deployment with Gunicorn + Nginx + go-live checks

### Critical Path
Environment setup → Auth → Career AI → Course AI → Insights AI → SNS → Admin → Resume → Learning Path → Negotiation → Interview → Pivot → Trends → Peers → Gamification → Chatbot → Cover Letter → GitHub → Skill Gap → History/PDF → Bookmarks → Dark Mode → Voice → GD → Mentor → RAG Job Match → Digest → Classroom → Nav/Dashboard → QA → Deployment.

---

## 2) Project Folder Structure and File Organization

Use this exact structure:

```text
virtual-career-counselor/
├── app/
│   ├── __init__.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── forms.py
│   │   └── utils.py
│   ├── career/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── prompts.py
│   ├── courses/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── prompts.py
│   ├── insights/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── prompts.py
│   ├── admin/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── resume/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── learning/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── negotiation/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── interview/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── pivot/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── trends/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── peers/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── gamification/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── chatbot/                    # v3.0
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── cover_letter/               # v3.0
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── github_analyzer/            # v3.0
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── skill_gap/                  # v3.0
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── history/                    # v3.0
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── mentor/                     # v3.0
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── group_discussion/           # v3.0
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── job_match/                  # v3.0
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── classroom/                  # v3.0
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── digest/                     # v3.0
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── groq_service.py
│   │   ├── dynamo_service.py
│   │   ├── sns_service.py
│   │   ├── auth_service.py
│   │   ├── health_service.py
│   │   ├── resume_parser.py
│   │   ├── rag_service.py          # v3.0 — lightweight TF-IDF RAG engine
│   │   └── pdf_service.py          # v3.0 — xhtml2pdf report generator
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── register.html
│   │   │   └── login.html
│   │   ├── dashboard.html
│   │   ├── career/
│   │   │   └── career_result.html
│   │   ├── courses/
│   │   │   └── course_result.html
│   │   ├── insights/
│   │   │   └── insights_result.html
│   │   ├── admin/
│   │   │   └── dashboard.html
│   │   ├── resume/
│   │   │   └── upload.html
│   │   ├── learning/
│   │   │   └── roadmap.html
│   │   ├── negotiation/
│   │   │   └── simulator.html
│   │   ├── interview/
│   │   │   └── prep.html
│   │   ├── pivot/
│   │   │   └── analyzer.html
│   │   ├── trends/
│   │   │   └── dashboard.html
│   │   ├── peers/
│   │   │   └── comparison.html
│   │   ├── gamification/
│   │   │   └── badges.html
│   │   ├── chatbot/                # v3.0
│   │   │   └── chat.html
│   │   ├── cover_letter/           # v3.0
│   │   │   └── generate.html
│   │   ├── github_analyzer/        # v3.0
│   │   │   └── analyze.html
│   │   ├── skill_gap/              # v3.0
│   │   │   └── analyze.html
│   │   ├── history/                # v3.0
│   │   │   ├── index.html
│   │   │   ├── detail.html
│   │   │   └── bookmarks.html
│   │   ├── mentor/                 # v3.0
│   │   │   └── chat.html
│   │   ├── group_discussion/       # v3.0
│   │   │   ├── start.html
│   │   │   └── discuss.html
│   │   ├── job_match/              # v3.0
│   │   │   └── match.html
│   │   ├── classroom/              # v3.0
│   │   │   ├── index.html
│   │   │   └── view.html
│   │   └── digest/                 # v3.0
│   │       ├── preferences.html
│   │       └── result.html
│   └── static/
│       ├── css/
│       │   └── styles.css          # includes dark mode styles
│       └── js/
│           └── app.js              # includes dark mode toggle + voice input
├── scripts/
│   ├── create_dynamodb_tables.py
│   └── seed_admin.py
├── tests/
│   ├── test_auth.py
│   ├── test_career.py
│   ├── test_courses.py
│   └── test_insights.py
├── rag_store.json                  # v3.0 — TF-IDF knowledge base storage
├── .env
├── .env.example
├── .gitignore
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

---

## 3) Phase-by-Phase Build Plan (Step-by-Step Checklist)

## Phase 0 — Bootstrap, Environment, and Baseline
**Goal:** Get local development environment and project skeleton ready.

### Tasks
- [ ] Create repository and initialize Python virtual environment.
- [ ] Install core dependencies (`Flask`, `Flask-Session`, `groq`, `boto3`, `bcrypt`, `python-dotenv`, `gunicorn`).
- [ ] Create base project folders and starter files (see structure above).
- [ ] Configure `.env` and `.env.example` with all required variables.
- [ ] Build Flask app factory in `app/__init__.py` and register all blueprints.
- [ ] Add base template with navigation, flash messages, and responsive layout.
- [ ] Add global error handlers (`404`, `500`) and logging setup.

### Done Criteria
- App runs locally with `flask run`.
- Base routes render without errors.

---

## Phase 1 — Authentication & Account Management
**Goal:** Implement secure register/login/logout with hashed passwords and session state.

### Tasks
- [ ] Create `Users` DynamoDB table and required indexes.
- [ ] Implement registration route (`/register`) with validation (name, email, password).
- [ ] Hash passwords with `bcrypt` before save.
- [ ] Enforce unique email check using GSI lookup.
- [ ] Implement login route (`/login`) with password verification.
- [ ] Store session keys on login (`user_id`, `email`, `role`, `is_authenticated`).
- [ ] Implement logout route (`/logout`) clearing session.
- [ ] Add `login_required` and `admin_required` decorators in `auth/utils.py`.
- [ ] Send SNS welcome email on successful registration.

### Done Criteria
- New user can register and log in.
- Wrong password fails safely.
- Password hashes (not plaintext) are stored.

---

## Phase 2 — Career Path Exploration (AI)
**Goal:** Build career search flow with structured AI output and persistence.

### Tasks
- [ ] Create career query page/form.
- [ ] Implement Groq service wrapper (`generate_career_overview`).
- [ ] Add structured prompt template for career overview.
- [ ] Parse AI response into UI sections:
  - required skills
  - certifications/courses
  - roles/progression
  - estimated entry timeline
- [ ] Save query + AI response to `Queries` table (`query_type='career'`).
- [ ] Add “Email this report” button (SNS publish).

### Done Criteria
- Authenticated user submits career name and receives response in < 5s (normal conditions).
- Result is saved in DynamoDB and visible on screen.

---

## Phase 3 — Personalized Course Recommendations (AI)
**Goal:** Generate personalized course plans based on user profile inputs.

### Tasks
- [ ] Build recommendation form fields:
  - interests
  - current skill level
  - learning goals
  - time availability (hours/week)
- [ ] Implement Groq wrapper (`generate_course_recommendations`).
- [ ] Add structured prompt for 5–8 course suggestions.
- [ ] Validate output includes: name, platform, description, level, duration.
- [ ] Store request and response in `Queries` (`query_type='course'`).
- [ ] Add option to email recommendations via SNS.

### Done Criteria
- Returns 5+ relevant courses with structured metadata.
- Records persist per user for retrieval.

---

## Phase 4 — Job Market Insights (AI)
**Goal:** Provide AI-generated market insight for role/industry queries.

### Tasks
- [ ] Create role/industry input UI for insights.
- [ ] Implement Groq wrapper (`generate_market_insights`).
- [ ] Add prompt requesting:
  - top in-demand skills
  - salary ranges (entry/mid/senior)
  - demand trend
  - geographic hotspots
- [ ] Display AI disclaimer prominently on results page.
- [ ] Save to `Queries` (`query_type='insights'`).

### Done Criteria
- Insights render with all required sections + disclaimer.
- Query history includes insights entries.

---

## Phase 5 — Notifications via AWS SNS
**Goal:** Integrate all required email notification triggers.

### Tasks
- [ ] Create SNS topic and capture topic ARN in `.env`.
- [ ] Add helper `publish_email(subject, message)` in `sns_service.py`.
- [ ] Trigger welcome email after registration.
- [ ] Trigger report emails for career/course/insights.
- [ ] Add admin alert sender for high error rate events.
- [ ] Add retry + log handling for SNS failures.

### Done Criteria
- Welcome and report emails are delivered within target window.
- SNS errors do not crash user requests.

---

## Phase 6 — Admin Dashboard
**Goal:** Add secure admin panel for user/query/system visibility.

### Tasks
- [ ] Implement admin login path using role check (`role='admin'`).
- [ ] Create admin dashboard route and template.
- [ ] Build user management table (name, email, created_at, query_count).
- [ ] Build query log view (query_type, user_id/email, timestamp).
- [ ] Compute system health metrics:
  - total users
  - total queries
  - error rate
- [ ] Add recent errors list from logs/AdminLogs table.

### Done Criteria
- Non-admin access is blocked.
- Admin can see core KPIs and activity logs.

---

## Phase 7 — Resume Analysis & Job Matching (AI)
**Goal:** Let users upload PDF/DOCX resumes and get AI-powered analysis with job matching.

### Tasks
- [ ] Create `resume_parser.py` service with PDF (PyPDF2) and DOCX (python-docx) text extraction.
- [ ] Install `PyPDF2` and `python-docx` dependencies.
- [ ] Implement `analyze_resume()` in `groq_service.py` with structured prompt (strengths, gaps, ATS score, matching roles).
- [ ] Create `/resume/` upload route with file validation (PDF/DOCX, max 5 MB).
- [ ] Create `resume/upload.html` template with file upload form and AI result display.
- [ ] Save analysis to `Queries` table (`query_type='resume'`).
- [ ] Award "Resume Pro" badge on first upload.
- [ ] Register `resume_bp` blueprint in app factory.

### Done Criteria
- User uploads resume and receives structured AI analysis.
- Supported formats: PDF, DOCX.
- Query saved to DynamoDB.

---

## Phase 8 — Personalized Learning Path with Progress Tracking
**Goal:** Generate week-by-week learning roadmaps with interactive progress tracking.

### Tasks
- [ ] Implement `generate_learning_path()` in `groq_service.py` with 8-week roadmap prompt.
- [ ] Create `/learning/` route with form (target role, current skills).
- [ ] Create `UserProgress` DynamoDB table (PK: `progress_id`, GSI on `user_id`).
- [ ] Implement `save_user_progress()` and `update_progress_weeks()` in `dynamo_service.py`.
- [ ] Create `learning/roadmap.html` with AI result + checkbox-based week tracker + progress bar.
- [ ] Award "Roadmap Ready" badge on first roadmap generation.
- [ ] Register `learning_bp` blueprint.

### Done Criteria
- User gets an 8-week learning roadmap.
- Progress persists across sessions (DynamoDB-backed).
- Progress bar updates visually.

---

## Phase 9 — Salary Negotiation Simulator (Multi-Turn AI Chat)
**Goal:** Build an interactive salary negotiation practice tool with AI acting as HR Manager.

### Tasks
- [ ] Implement `_multi_turn_chat()` helper and `negotiation_reply()` in `groq_service.py`.
- [ ] Create `Conversations` DynamoDB table (PK: `conversation_id`).
- [ ] Implement `save_conversation()` in `dynamo_service.py`.
- [ ] Create `/negotiation/` routes: `simulator` (GET), `begin` (POST), `reply` (POST).
- [ ] Support 4 negotiation rounds with scoring at the end.
- [ ] Store conversation history in Flask session (JSON-serialized).
- [ ] Create `negotiation/simulator.html` with chat UI, round counter, and auto-scroll.
- [ ] Award "Negotiator" badge on completing a full session.
- [ ] Register `negotiation_bp` blueprint.

### Done Criteria
- User starts negotiation with role/company/salary details.
- AI responds as an HR Manager for 4 rounds.
- Final scorecard with tips provided at end.

---

## Phase 10 — Interview Prep Simulator (Company-Specific AI)
**Goal:** Simulate company-specific interviews with AI interviewer asking role-relevant questions.

### Tasks
- [ ] Implement `get_interview_system_prompt()` and `interview_reply()` in `groq_service.py`.
- [ ] Create `/interview/` routes: `prep` (GET), `begin` (POST), `reply` (POST).
- [ ] Support 10 companies (Google, Amazon, Microsoft, Meta, Apple, Netflix, Goldman Sachs, McKinsey, Deloitte, Infosys) and 10 roles.
- [ ] AI asks 5 questions, then provides scored evaluation.
- [ ] Create `interview/prep.html` with company/role selectors, chat UI, question counter.
- [ ] Award "Interview Ready" badge on first completed interview.
- [ ] Register `interview_bp` blueprint.

### Done Criteria
- User selects company + role and gets 5 interview questions.
- AI evaluates each answer and gives final score.
- Conversation saved to DynamoDB.

---

## Phase 11 — Career Pivot Analyzer (AI)
**Goal:** Analyze transferable skills and generate transition roadmap for career switches.

### Tasks
- [ ] Implement `analyze_career_pivot()` in `groq_service.py` with transferable skills mapping prompt.
- [ ] Create `/pivot/` route with form (current role, target role, years experience, current skills).
- [ ] Create `pivot/analyzer.html` template.
- [ ] Save analysis to `Queries` table (`query_type='pivot'`).
- [ ] Add "Email Report" option.
- [ ] Register `pivot_bp` blueprint.

### Done Criteria
- User enters current and target career details.
- AI maps transferable skills and gives step-by-step transition plan.

---

## Phase 12 — Real-Time Market Trends Dashboard (AI)
**Goal:** Provide AI-generated hiring trend reports per industry.

### Tasks
- [ ] Implement `generate_trends_report()` in `groq_service.py` with trends prompt.
- [ ] Create `/trends/` route with industry dropdown (10 pre-set) + custom text input.
- [ ] Create `trends/dashboard.html` template.
- [ ] Save to `Queries` table (`query_type='trends'`).
- [ ] Register `trends_bp` blueprint.

### Done Criteria
- User selects or types industry and gets comprehensive trends report.

---

## Phase 13 — Peer Comparison & Benchmarking (AI)
**Goal:** Let users benchmark their skills and experience against anonymous industry peers.

### Tasks
- [ ] Implement `generate_peer_comparison()` in `groq_service.py` with benchmarking prompt.
- [ ] Create `/peers/` route with form (target role, skills, experience).
- [ ] Create `peers/comparison.html` template.
- [ ] Save to `Queries` table (`query_type='peer_compare'`).
- [ ] Award "Benchmarker" badge on first comparison.
- [ ] Register `peers_bp` blueprint.

### Done Criteria
- User gets percentile ranking and gap analysis compared to peers.

---

## Phase 14 — Gamification — Badges & Leaderboard
**Goal:** Motivate users with achievement badges and a competitive leaderboard.

### Tasks
- [ ] Create `UserBadges` DynamoDB table (PK: `badge_id`, GSI on `user_id`).
- [ ] Implement `award_badge()`, `get_user_badges()`, `get_leaderboard()`, `get_user_query_count()` in `dynamo_service.py`.
- [ ] Define badge rules: First Query, Explorer (5), Power User (10), Career Master (25), Legend (50).
- [ ] Define feature-specific badges: Resume Pro, Roadmap Ready, Negotiator, Interview Ready, Benchmarker.
- [ ] Create `/gamification/` route with badge grid + leaderboard table.
- [ ] Create `gamification/badges.html` with badge cards, stats, and top-20 leaderboard.
- [ ] Auto-award query-based badges on page visit.
- [ ] Register `gamification_bp` blueprint.

### Done Criteria
- Badges auto-awarded based on activity.
- User sees their badges, stats, and rank.
- Leaderboard shows top 20 users.

---

## Phase 15 — AI Chatbot with RAG Toggle (v3.0)
**Goal:** Build a multi-turn conversational AI assistant with optional RAG-enhanced context.

### Tasks
- [ ] Implement `chatbot_reply(messages)` in `groq_service.py` with `CHATBOT_SYSTEM` prompt.
- [ ] Create `/chatbot/` routes: index (GET), send (POST), clear (POST).
- [ ] Session-based message history (multi-turn).
- [ ] Add RAG toggle checkbox — when enabled, inject `get_rag_context()` into system prompt.
- [ ] Save conversations to `Queries` table (`query_type='chatbot'`).
- [ ] Create `chatbot/chat.html` with message bubbles, auto-scroll, voice input button.
- [ ] Register `chatbot_bp` blueprint.

### Done Criteria
- Multi-turn chat works with context retained.
- RAG toggle enriches responses with knowledge base context.

---

## Phase 16 — Cover Letter Generator (v3.0)
**Goal:** AI-generate tailored cover letters from resume text + job description.

### Tasks
- [ ] Implement `generate_cover_letter(resume_text, job_description, company_name)` in `groq_service.py`.
- [ ] Create `/cover-letter/` route with form (company name, job description, resume text).
- [ ] Add copy-to-clipboard button on result.
- [ ] Save to `Queries` table (`query_type='cover_letter'`).
- [ ] Create `cover_letter/generate.html` template.
- [ ] Register `cover_letter_bp` blueprint.

### Done Criteria
- User provides resume + JD + company and gets a tailored cover letter.

---

## Phase 17 — GitHub Profile Analyzer (v3.0)
**Goal:** Fetch GitHub repos via API and provide AI career analysis.

### Tasks
- [ ] Install `requests` library.
- [ ] Implement `analyze_github_profile(repos_info)` in `groq_service.py` with `GITHUB_SYSTEM` prompt.
- [ ] Create `_fetch_github_repos(username)` helper in `github_analyzer/routes.py` using GitHub REST API.
- [ ] Support optional `GITHUB_TOKEN` in config for higher rate limits.
- [ ] Create `/github/` route with username input.
- [ ] Save to `Queries` table (`query_type='github_analysis'`).
- [ ] Create `github_analyzer/analyze.html` template.
- [ ] Register `github_bp` blueprint.

### Done Criteria
- User enters GitHub username, app fetches repos and returns AI career analysis.

---

## Phase 18 — Skill Gap Heatmap with Chart.js (v3.0)
**Goal:** Visualize skill gaps with an interactive bar chart comparing current vs. required skills.

### Tasks
- [ ] Implement `analyze_skill_gap(current_skills, target_role, experience)` in `groq_service.py` with `SKILL_GAP_SYSTEM` prompt.
- [ ] Parse JSON response from AI (readiness score, chart data, priority skills, summary).
- [ ] Create `/skill-gap/` route with form (target role, experience, current skills).
- [ ] Integrate Chart.js 4.4.0 via CDN for bar chart rendering.
- [ ] Render readiness score with dynamic color coding (green/yellow/red).
- [ ] Create `skill_gap/analyze.html` template with chart + priority badges.
- [ ] Register `skill_gap_bp` blueprint.

### Done Criteria
- User sees visual bar chart comparing their skills vs. required levels.
- Readiness percentage and priority skills displayed.

---

## Phase 19 — Query History + PDF Export (v3.0)
**Goal:** Let users browse, search, and export all past AI interactions.

### Tasks
- [ ] Implement `get_user_queries(user_id, limit)` and `get_query_by_id(query_id)` in `dynamo_service.py`.
- [ ] Install `xhtml2pdf` and `markdown` libraries.
- [ ] Create `pdf_service.py` with `generate_pdf(title, html_content, user_name)` function.
- [ ] Create `/history/` routes: index (with type filter), detail, export_pdf.
- [ ] Convert AI markdown to HTML, then HTML to styled PDF via xhtml2pdf.
- [ ] Create `history/index.html` (table with filter buttons) and `history/detail.html`.
- [ ] Register `history_bp` blueprint.

### Done Criteria
- User can browse all past queries, filter by type, view details, and download PDF.

---

## Phase 20 — Bookmarks (v3.0)
**Goal:** Let users save and revisit favorite AI results.

### Tasks
- [ ] Create `Bookmarks` DynamoDB table (PK: `bookmark_id`, GSI on `user_id`).
- [ ] Implement `save_bookmark()`, `get_user_bookmarks()`, `delete_bookmark()` in `dynamo_service.py`.
- [ ] Add bookmark add/remove routes to `history_bp`.
- [ ] Create `history/bookmarks.html` template with grid of saved items.
- [ ] Add bookmark buttons on history detail and index pages.

### Done Criteria
- User can bookmark/unbookmark any query result and view all bookmarks in one place.

---

## Phase 21 — Dark Mode (v3.0)
**Goal:** Full dark theme toggle with persistence across sessions.

### Tasks
- [ ] Add `data-bs-theme="light"` attribute to `<html>` tag in `base.html`.
- [ ] Add dark mode toggle button (moon/sun icon) in navbar.
- [ ] Implement JS toggle in `app.js` that flips `data-bs-theme` between `light` and `dark`.
- [ ] Store preference in `localStorage` and apply on page load.
- [ ] Add CSS overrides for `[data-bs-theme="dark"]` covering cards, forms, tables, dropdowns, chat windows.

### Done Criteria
- User clicks toggle, entire UI switches theme. Persists across page reloads.

---

## Phase 22 — Voice Input (v3.0)
**Goal:** Enable speech-to-text input on any form field using Web Speech API.

### Tasks
- [ ] Implement `startVoiceInput(inputId)` function in `app.js`.
- [ ] Use `SpeechRecognition` / `webkitSpeechRecognition` API (en-US).
- [ ] Add visual recording indicator (pulsing red animation) via CSS.
- [ ] Add microphone buttons next to text inputs in chatbot, mentor, and GD templates.

### Done Criteria
- User clicks mic icon, speaks, and text appears in the input field.

---

## Phase 23 — Mock Group Discussion (v3.0)
**Goal:** Multi-round AI-moderated group discussion practice with evaluation.

### Tasks
- [ ] Implement `group_discussion_reply(messages)` in `groq_service.py` with `GD_SYSTEM` prompt.
- [ ] Create `/gd/` routes: start (topic selection), discuss (multi-turn), reset.
- [ ] Provide 7 preset topics + custom topic input.
- [ ] Track discussion rounds in session; trigger AI evaluation after 5+ rounds.
- [ ] Create `group_discussion/start.html` (topic picker) and `group_discussion/discuss.html` (chat UI with round counter).
- [ ] Register `gd_bp` blueprint.

### Done Criteria
- User picks a topic, discusses for 5+ rounds, and gets scored evaluation.

---

## Phase 24 — AI Mentor Chat (v3.0)
**Goal:** Persistent, goal-based mentorship conversations with AI.

### Tasks
- [ ] Implement `mentor_reply(messages)` in `groq_service.py` with `MENTOR_SYSTEM` prompt.
- [ ] Create `MentorChats` DynamoDB table (PK: `user_id`).
- [ ] Implement `save_mentor_chat()` and `get_mentor_chat()` in `dynamo_service.py`.
- [ ] Create `/mentor/` routes: chat (GET/POST with set_goals + send actions), clear.
- [ ] Persist conversation + goals in DynamoDB and session.
- [ ] Create `mentor/chat.html` with goals card + chat interface + voice input.
- [ ] Register `mentor_bp` blueprint.

### Done Criteria
- User sets career goals, then has ongoing mentorship conversation. Persists across sessions.

---

## Phase 25 — RAG Job Matching (v3.0)
**Goal:** Lightweight TF-IDF knowledge base for career-related Q&A without external vector DB.

### Tasks
- [ ] Create `rag_service.py` with TF-IDF cosine similarity engine.
- [ ] Store documents in `rag_store.json` (no external DB dependency).
- [ ] Implement `add_documents()`, `query_knowledge()`, `get_rag_context()`, `seed_knowledge_base()`.
- [ ] Include 10 seed documents covering major career domains.
- [ ] Implement `rag_enhanced_query(user_question, rag_context)` in `groq_service.py`.
- [ ] Create `/job-match/` routes: match (query), seed (populate KB), add_doc (custom upload).
- [ ] Create `job_match/match.html` with query form + KB stats + add document form.
- [ ] Register `job_match_bp` blueprint.

### Done Criteria
- User queries get matched against knowledge base; AI response enriched with RAG context.
- Admin can seed KB or add custom documents.

---

## Phase 26 — Weekly Career Digest (v3.0)
**Goal:** On-demand AI career digest for user-selected industries.

### Tasks
- [ ] Implement `generate_weekly_digest(industries)` in `groq_service.py`.
- [ ] Create `DigestPreferences` DynamoDB table (PK: `user_id`).
- [ ] Implement `save_digest_prefs()` and `get_digest_prefs()` in `dynamo_service.py`.
- [ ] Create `/digest/` routes: preferences (15 industry checkboxes + enable toggle), generate (on-demand).
- [ ] Support 15 industries: Technology, Healthcare, Finance, Education, Marketing, Design, Data Science, Cybersecurity, E-Commerce, Manufacturing, Consulting, Media & Entertainment, Legal, Real Estate, AI/ML.
- [ ] Create `digest/preferences.html` and `digest/result.html` templates.
- [ ] Register `digest_bp` blueprint.

### Done Criteria
- User selects industries, clicks generate, and gets AI-written career digest.

---

## Phase 27 — Team/Classroom Mode (v3.0)
**Goal:** Create and join classrooms to share AI activity with peers.

### Tasks
- [ ] Create `Classrooms` DynamoDB table (PK: `classroom_id`).
- [ ] Implement `create_classroom()`, `get_classroom_by_code()`, `join_classroom()`, `get_user_classrooms()` in `dynamo_service.py`.
- [ ] Generate unique 8-character join codes.
- [ ] Create `/classroom/` routes: index, create, join (by code), view (member activity).
- [ ] Display member names, roles, recent query counts, last active dates.
- [ ] Create `classroom/index.html` (create/join cards + my classrooms grid) and `classroom/view.html` (member activity table).
- [ ] Register `classroom_bp` blueprint.

### Done Criteria
- User creates classroom with join code; others join by code; all members see shared activity.

---

## Phase 28 — Navigation Overhaul + Dashboard Redesign (v3.0)
**Goal:** Update navbar and dashboard to showcase all 27 features.

### Tasks
- [ ] Redesign `base.html` navbar with 2 mega dropdowns:
  - **AI Tools** dropdown: Analysis section (Career, Courses, Insights, Resume, Skill Gap, GitHub, Pivot, Peers), Practice section (Negotiation, Interview, GD), Generate section (Cover Letter, Trends, Learning Path), Explore section (Job Match).
  - **More** dropdown: Chatbot, Mentor, History, Bookmarks, Digest, Classrooms, Badges.
- [ ] Add dark mode toggle button in navbar.
- [ ] Update footer to v3.0 branding.
- [ ] Redesign `dashboard.html` with 22 feature cards in 5 sections.

### Done Criteria
- All features accessible from nav within 1 click. Dashboard shows all features with icons and descriptions.

---

## Phase 29 — Testing, QA, and Hardening (v3.0)
**Goal:** Confirm full app readiness (core + 8 killer + 16 advanced features) before deployment.

### Tasks
- [ ] Run template rendering test for all 15+ routes.
- [ ] Verify all 23 blueprints and 53 routes load without errors.
- [ ] Test all DynamoDB operations with try/except guards for missing tables.
- [ ] Verify dark mode toggle, voice input, and Chart.js rendering.
- [ ] Manually test full user journey: register → login → chatbot → history → PDF → bookmark.
- [ ] Verify RAG knowledge base seed + query.
- [ ] Test classroom create/join flow.
- [ ] Validate error handling + user-safe messages on all routes.

### Done Criteria
- No blocker defects.
- All 27 features pass basic smoke tests.

---

## Phase 30 — Production Deployment on AWS EC2
**Goal:** Deploy and validate live MVP.

### Tasks
- [ ] Launch EC2 (Ubuntu 22.04) and attach IAM app role.
- [ ] Install Python, pip, nginx, gunicorn, git.
- [ ] Clone repo and set up virtual environment.
- [ ] Add production `.env` and verify secrets.
- [ ] Start app with Gunicorn.
- [ ] Configure Nginx reverse proxy.
- [ ] Open ports 80/443 and set security rules.
- [ ] Add HTTPS (Let’s Encrypt or ACM + ALB).
- [ ] Restart services and run smoke tests.

### Done Criteria
- Public URL works.
- Core flows succeed in production.

---

## 4) Complete AWS Setup Steps

## 4.1 DynamoDB Setup

### Table A: `Users`
- Partition key: `user_id` (String)
- Attributes:
  - `email` (String)
  - `name` (String)
  - `password_hash` (String)
  - `created_at` (String ISO8601)
  - `role` (String: `user` / `admin`)
- Add GSI:
  - `email-index` with partition key `email`

### Table B: `Queries`
- Partition key: `query_id` (String)
- Sort key: `user_id` (String)
- Attributes:
  - `query_type` (`career` / `course` / `insights`)
  - `input_text` (String)
  - `ai_response` (String)
  - `timestamp` (String ISO8601)

### Table C (Optional but recommended for MVP admin alerts): `AdminLogs`
- Partition key: `log_id` (String)
- Attributes: `level`, `message`, `timestamp`, `source`

### Table D: `Conversations`
- Partition key: `conversation_id` (String)
- Attributes:
  - `user_id` (String)
  - `conv_type` (String: `negotiation` / `interview`)
  - `messages` (List of maps: `{role, content}`)
  - `metadata` (Map: company, role, score, etc.)
  - `created_at` (String ISO8601)

### Table E: `UserProgress`
- Partition key: `progress_id` (String)
- Attributes:
  - `user_id` (String)
  - `target_role` (String)
  - `completed_weeks` (List of Strings)
  - `created_at` (String ISO8601)
- Add GSI:
  - `user-index` with partition key `user_id`

### Table F: `UserBadges`
- Partition key: `badge_id` (String)
- Attributes:
  - `user_id` (String)
  - `badge_name` (String)
  - `icon` (String — Bootstrap Icon class)
  - `description` (String)
  - `awarded_at` (String ISO8601)
- Add GSI:
  - `user-index` with partition key `user_id`

### Capacity Mode
- Use **On-Demand** for MVP speed and auto-scaling.

### Table G (v3.0): `Bookmarks`
- Partition key: `bookmark_id` (String)
- Attributes:
  - `user_id` (String)
  - `query_id` (String)
  - `title` (String)
  - `query_type` (String)
  - `created_at` (String ISO8601)
- Add GSI: `user-index` with partition key `user_id`

### Table H (v3.0): `MentorChats`
- Partition key: `user_id` (String)
- Attributes:
  - `messages` (List of maps: `{role, content}`)
  - `goals` (String)
  - `updated_at` (String ISO8601)

### Table I (v3.0): `Classrooms`
- Partition key: `classroom_id` (String)
- Attributes:
  - `name` (String)
  - `join_code` (String — unique 8-char alphanumeric)
  - `created_by` (String — user_id)
  - `members` (List of maps: `{user_id, name, role, joined_at}`)
  - `created_at` (String ISO8601)

### Table J (v3.0): `DigestPreferences`
- Partition key: `user_id` (String)
- Attributes:
  - `industries` (List of Strings)
  - `enabled` (Boolean)
  - `updated_at` (String ISO8601)

---

## 4.2 IAM Roles and Policies

### Role 1: `ec2-app-role` (attach to EC2 instance)
Allow:
- `dynamodb:PutItem`
- `dynamodb:GetItem`
- `dynamodb:Query`
- `dynamodb:Scan`
- `dynamodb:UpdateItem`
- `dynamodb:DeleteItem`
- `sns:Publish`

Resources:
- `arn:aws:dynamodb:<region>:<account-id>:table/Users`
- `arn:aws:dynamodb:<region>:<account-id>:table/Queries`
- `arn:aws:dynamodb:<region>:<account-id>:table/AdminLogs`
- `arn:aws:dynamodb:<region>:<account-id>:table/Conversations`
- `arn:aws:dynamodb:<region>:<account-id>:table/UserProgress`
- `arn:aws:dynamodb:<region>:<account-id>:table/UserBadges`
- `arn:aws:sns:<region>:<account-id>:VirtualCareerCounselorNotifications`

### Role/User 2: `admin-user`
- DynamoDB full access for operational/admin tasks.

### Role/User 3: `readonly-user`
- DynamoDB read-only access for analytics/monitoring.

### Security Requirement
- Apply least privilege; deny unrelated services.

---

## 4.3 SNS Setup

1. Create topic: `VirtualCareerCounselorNotifications` (Standard).
2. Add email subscriptions:
   - Admin email (always)
   - Optional user emails if using topic fanout approach
3. Confirm subscription links via email.
4. Save topic ARN to `.env` (`SNS_TOPIC_ARN`).
5. Implement Flask call: `sns.publish(TopicArn=..., Subject=..., Message=...)`.

---

## 4.4 EC2 Setup

1. Launch `Ubuntu 22.04 LTS` EC2 (`t2.micro` MVP or `t2.medium` recommended).
2. Attach IAM role `ec2-app-role`.
3. Security Group inbound rules:
   - 22 (SSH) from your IP
   - 80 (HTTP) from anywhere
   - 443 (HTTPS) from anywhere
4. SSH into instance and install stack.

---

## 5) Groq API Integration Guide

## 5.1 Environment Variables
Add to `.env`:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
AWS_REGION=ap-south-1
SNS_TOPIC_ARN=arn:aws:sns:...
SECRET_KEY=replace_with_long_random_secret
DYNAMODB_USERS_TABLE=Users
DYNAMODB_QUERIES_TABLE=Queries
DYNAMODB_ADMINLOGS_TABLE=AdminLogs
DYNAMODB_CONVERSATIONS_TABLE=Conversations
DYNAMODB_PROGRESS_TABLE=UserProgress
DYNAMODB_BADGES_TABLE=UserBadges
DYNAMODB_BOOKMARKS_TABLE=Bookmarks
DYNAMODB_MENTOR_TABLE=MentorChats
DYNAMODB_CLASSROOMS_TABLE=Classrooms
DYNAMODB_DIGEST_TABLE=DigestPreferences
GITHUB_TOKEN=optional_github_personal_access_token
FLASK_ENV=production
```

## 5.2 Service Wrapper Design (`app/services/groq_service.py`)
- Single reusable client initializer.
- One method per feature:
  - `generate_career_overview(career_name)`
  - `generate_course_recommendations(interests, level, goals, time_available)`
  - `generate_market_insights(role_or_industry)`
  - `analyze_resume(resume_text)` — Resume strength/gap analysis + job matching
  - `generate_learning_path(target_role, current_skills)` — 8-week roadmap
  - `negotiation_reply(conversation, metadata)` — Multi-turn salary negotiation
  - `interview_reply(conversation, metadata)` — Multi-turn interview simulation
  - `get_interview_system_prompt(company, role, experience)` — Company-specific system prompt
  - `analyze_career_pivot(current_role, target_role, years_exp, skills)` — Transferable skills mapping
  - `generate_trends_report(industry)` — Industry hiring trends
  - `generate_peer_comparison(target_role, skills, experience)` — Peer benchmarking
  - `_multi_turn_chat(conversation)` — Helper for multi-turn AI conversations
  - `chatbot_reply(messages)` — v3.0 multi-turn chatbot with RAG toggle
  - `generate_cover_letter(resume_text, job_description, company_name)` — v3.0 cover letter
  - `analyze_github_profile(repos_info)` — v3.0 GitHub profile career analysis
  - `analyze_skill_gap(current_skills, target_role, experience)` — v3.0 skill gap with chart data
  - `group_discussion_reply(messages)` — v3.0 mock GD moderator
  - `mentor_reply(messages)` — v3.0 persistent mentor conversation
  - `rag_enhanced_query(user_question, rag_context)` — v3.0 RAG-enhanced career Q&A
  - `generate_weekly_digest(industries)` — v3.0 career digest generator
- Add timeouts and exception handling.
- Normalize output format (JSON-like sections or strict bullet blocks).

## 5.3 Prompt Templates (All 3 AI Features)

### A) Career Path Prompt
**System Prompt**
```text
You are an expert career counselor. Give practical, structured, concise guidance.
Output with these exact sections:
1) Required Skills (Technical + Soft)
2) Recommended Certifications/Courses
3) Typical Job Roles and Career Progression
4) Estimated Time to Enter Field
5) Suggested Next 30-Day Action Plan
```

**User Prompt**
```text
Create a career overview for: {career_name}.
Target audience: student/fresher.
Keep it realistic and actionable.
```

### B) Course Recommendation Prompt
**System Prompt**
```text
You are an AI learning advisor.
Return 5 to 8 course recommendations in this format for each item:
- Course Name
- Platform
- Why this course matches the user
- Difficulty (Beginner/Intermediate/Advanced)
- Estimated Duration
- Expected Outcome after completion
```

**User Prompt**
```text
Recommend courses based on:
Interests: {interests}
Current Skill Level: {skill_level}
Learning Goals: {learning_goals}
Time Availability: {time_availability} hours/week
```

### C) Job Market Insights Prompt
**System Prompt**
```text
You are a labor market analyst. Provide estimated trends (not real-time scraped data).
Output sections:
1) Top In-Demand Skills
2) Salary Range (Entry/Mid/Senior)
3) Demand Trend (Growing/Stable/Declining) with brief reason
4) Geographic Hotspots
5) Hiring Tips for Next 3 Months
```

**User Prompt**
```text
Provide market insights for role/industry: {role_or_industry}.
Focus on practical guidance for job seekers.
```

### D) Resume Analysis Prompt
**System Prompt**
```text
You are an expert resume analyst and career advisor. Analyze the resume text provided.
Output with these exact sections:
1) **Overall Score** (out of 100)
2) **Key Strengths** (top 5)
3) **Critical Gaps** (areas to improve)
4) **ATS Compatibility Score** (out of 100)
5) **Top 5 Matching Job Roles** (with fit percentage)
6) **Action Items** (immediate improvements)
```

### E) Learning Path Prompt
**System Prompt**
```text
You are an expert learning advisor. Create an 8-week learning roadmap.
For each week include:
- Week number and theme
- Specific topics to study
- Recommended resources (free + paid)
- Mini-project or practice exercise
- Expected outcome by week end
```

### F) Salary Negotiation System Prompt
```text
You are an experienced HR Manager conducting a salary discussion.
Be firm but fair. Push back on the candidate's first offer.
After 4 rounds, provide a scorecard: Confidence, Justification, Market Awareness, Overall Score.
```

### G) Interview Prep System Prompt
```text
You are a senior interviewer at {company} for the {role} position.
Ask one question at a time. After 5 questions, provide:
- Score for each answer (1-10)
- Overall score and hiring recommendation
- Areas of improvement
```

### H) Career Pivot Prompt
```text
You are a career transition expert. Analyze the career switch and provide:
1) Transferable Skills Map (current → target)
2) Skills Gap Analysis
3) Transition Difficulty Score (1-10)
4) Step-by-Step Transition Roadmap (3-6 months)
5) Success Stories / Role Models
```

### I) Market Trends Prompt
```text
You are an industry analyst. For the given industry provide:
1) Current Hiring Trends (hot vs cooling roles)
2) Top 10 In-Demand Skills
3) Salary Ranges by Experience Level
4) Growth Projections (next 2-3 years)
5) Emerging Roles & Technologies
6) Advice for Job Seekers
```

### J) Peer Comparison Prompt
```text
You are a career benchmarking analyst. Compare the user's profile against industry peers.
Provide:
1) Percentile Ranking (for their skills + experience)
2) Skills Gap vs Top Performers
3) Salary Benchmarking
4) Competitive Advantages
5) Action Plan to Reach Top 25%
```

### K) Chatbot System Prompt (v3.0)
```text
You are a friendly, knowledgeable AI career counselor chatbot.
Help users with career questions, job search tips, skill development, and professional growth.
Be conversational but data-driven. If RAG context is provided, use it to enrich your answers.
Keep responses concise (2-4 paragraphs) unless the user asks for detail.
```

### L) Cover Letter System Prompt (v3.0)
```text
You are an expert cover letter writer. Generate a professional cover letter.
Use the provided resume and job description to highlight the best-fit skills.
Structure: Opening hook → Relevant experience → Why this company → Enthusiastic close.
Keep it under 400 words. Tailor language to the company culture.
```

### M) GitHub Analysis System Prompt (v3.0)
```text
You are a tech career analyst. Analyze the developer's GitHub profile.
Based on their repositories, languages, and activity, provide:
1) Technical Skill Assessment
2) Top Languages & Expertise Level
3) Project Quality Analysis
4) Career Path Recommendations
5) Areas for Improvement
6) Suggested Open Source Contributions
```

### N) Skill Gap System Prompt (v3.0)
```text
You are a skill gap analyst. Compare the user's current skills against a target role.
Return VALID JSON with: readiness (0-100), chart_data (array of {skill, current, required}),
priority_skills (array of strings), timeline (string), summary (string).
```

### O) Group Discussion System Prompt (v3.0)
```text
You are a Group Discussion moderator and participant simulator.
Engage with the user's points, present counter-arguments, and ask probing questions.
After 5+ rounds, if asked for evaluation, provide: Communication score, Content quality,
Leadership indicators, Overall score, and Specific improvement tips.
```

### P) Mentor System Prompt (v3.0)
```text
You are an experienced career mentor. Reference the user's goals throughout conversations.
Give actionable advice, suggest resources, track progress, and provide encouragement.
Be warm but professional. Ask follow-up questions to understand context.
```

### Q) RAG-Enhanced System Prompt (v3.0)
```text
You are an AI career advisor with access to a curated knowledge base.
Use the provided context to give accurate, specific answers about career paths,
job markets, and skill requirements. Always indicate when information comes from the knowledge base.
```

### Prompt Safety Rules
- Cap input length (e.g., 300–500 chars per field).
- Strip suspicious prompt-injection patterns.
- Never include secrets/system config in user-visible responses.

---

## 6) Feature Implementation Order (Strict)

1. Environment setup and Flask app skeleton
2. Authentication and session management
3. Career path AI feature
4. Course recommendations AI feature
5. Job market insights AI feature
6. SNS notifications
7. Admin dashboard
8. Resume Analysis & Job Matching
9. Personalized Learning Path with Progress Tracking
10. Salary Negotiation Simulator (multi-turn AI chat)
11. Interview Prep Simulator (company-specific AI)
12. Career Pivot Analyzer
13. Real-Time Market Trends Dashboard
14. Peer Comparison & Benchmarking
15. Gamification — Badges & Leaderboard
16. AI Chatbot with RAG toggle (v3.0)
17. Cover Letter Generator (v3.0)
18. GitHub Profile Analyzer (v3.0)
19. Skill Gap Heatmap + Chart.js (v3.0)
20. Query History + PDF Export (v3.0)
21. Bookmarks (v3.0)
22. Dark Mode (v3.0)
23. Voice Input (v3.0)
24. Mock Group Discussion (v3.0)
25. AI Mentor Chat (v3.0)
26. RAG Job Matching (v3.0)
27. Weekly Career Digest (v3.0)
28. Team/Classroom Mode (v3.0)
29. Navigation overhaul + Dashboard redesign (v3.0)
30. Testing, QA, and Hardening
31. EC2 deployment and production checks
13. Real-Time Market Trends Dashboard
14. Peer Comparison & Benchmarking
15. Gamification — Badges & Leaderboard
16. AI Chatbot with RAG toggle (v3.0)

(Items 17-31 listed in section above)

---

## 7) Testing Checklist (Before Done)

## 7.1 Authentication
- [ ] Register with new email works.
- [ ] Duplicate email registration blocked.
- [ ] Password stored hashed.
- [ ] Login success and failure cases behave correctly.
- [ ] Logout clears session.

## 7.2 AI Features (Core)
- [ ] Career query returns all required sections.
- [ ] Course recommendations return 5+ structured items.
- [ ] Insights return skills/salary/trend/hotspots.
- [ ] Response time typically < 5 sec for normal prompts.

## 7.2b AI Features (8 Killer Features)
- [ ] Resume upload (PDF + DOCX) returns structured analysis with score.
- [ ] Learning path returns 8-week roadmap; progress checkboxes persist.
- [ ] Salary negotiation runs 4 rounds with final scorecard.
- [ ] Interview prep runs 5 questions for selected company/role with scoring.
- [ ] Career pivot returns transferable skills map and transition plan.
- [ ] Market trends returns industry-specific hiring report.
- [ ] Peer comparison returns percentile ranking and gap analysis.
- [ ] Badges auto-award correctly; leaderboard displays top 20.

## 7.2c AI Features (16 Advanced v3.0 Features)
- [ ] AI Chatbot: multi-turn conversation works; RAG toggle enriches context.
- [ ] Cover Letter: generates tailored cover letter from resume + JD + company.
- [ ] GitHub Analyzer: fetches repos, returns AI career analysis.
- [ ] Skill Gap Heatmap: Chart.js bar chart renders; readiness score color-coded.
- [ ] Query History: browse, filter by type, view detail pages.
- [ ] PDF Export: download any AI result as styled PDF.
- [ ] Bookmarks: save/remove queries; bookmarks page displays all saved items.
- [ ] Dark Mode: toggle switches theme; persists across reloads via localStorage.
- [ ] Voice Input: microphone button transcribes speech to text field.
- [ ] Mock GD: 5+ round discussion with AI; evaluation at the end.
- [ ] AI Mentor: goals set once; persistent multi-turn mentorship.
- [ ] RAG Job Match: knowledge base query returns enriched answers; seed + add docs work.
- [ ] Weekly Digest: select industries; generate on-demand digest.
- [ ] Classroom: create room with code; join by code; member activity visible.

## 7.3 Persistence
- [ ] Users written correctly to `Users` table.
- [ ] Each AI interaction written to `Queries` table.
- [ ] Query history retrieval works (last 10 queries).
- [ ] Conversations (negotiation/interview) saved to `Conversations` table.
- [ ] Learning path progress saved/updated in `UserProgress` table.
- [ ] Badges saved to `UserBadges` table; no duplicates on re-award.
- [ ] Bookmarks saved to `Bookmarks` table (v3.0); save/delete work.
- [ ] Mentor chat saved to `MentorChats` table (v3.0); persists across sessions.
- [ ] Classrooms saved to `Classrooms` table (v3.0); join codes unique.
- [ ] Digest preferences saved to `DigestPreferences` table (v3.0).
- [ ] RAG knowledge base stored in `rag_store.json` (v3.0); seed + add docs persist.

## 7.4 Notifications
- [ ] SNS welcome email received after registration.
- [ ] Report email received on button click.
- [ ] Admin alert can be triggered and received.

## 7.5 Admin Dashboard
- [ ] Admin route protected from non-admin users.
- [ ] User list, query logs, and health stats visible.

## 7.6 Security / Reliability
- [ ] `.env` not committed.
- [ ] IAM least privilege verified.
- [ ] Input validation on all forms.
- [ ] Error pages/logging work without exposing internals.

## 7.7 Production Smoke Test
- [ ] Register → login → career query → email report flow works on live URL.
- [ ] Course and insights flows work end-to-end.
- [ ] Resume upload → analysis → badge award works.
- [ ] Learning path → progress tracking works.
- [ ] Salary negotiation → 4 rounds → scorecard works.
- [ ] Interview prep → 5 questions → evaluation works.
- [ ] Career pivot, trends, peer comparison all return results.
- [ ] Gamification page shows badges and leaderboard.
- [ ] AI Chatbot multi-turn conversation with RAG toggle works (v3.0).
- [ ] Cover letter generates from resume + JD (v3.0).
- [ ] GitHub analysis fetches repos and returns results (v3.0).
- [ ] Skill gap heatmap renders Chart.js chart (v3.0).
- [ ] Query history lists all past queries; PDF export downloads (v3.0).
- [ ] Bookmarks save/remove works (v3.0).
- [ ] Dark mode toggle switches theme and persists (v3.0).
- [ ] Voice input microphone captures speech (v3.0).
- [ ] Group discussion runs 5+ rounds with evaluation (v3.0).
- [ ] AI Mentor chat persists goals and conversation (v3.0).
- [ ] RAG job match returns enriched results (v3.0).
- [ ] Weekly digest generates for selected industries (v3.0).
- [ ] Classroom create, join, view member activity works (v3.0).
- [ ] Navbar mega dropdowns work on mobile and desktop.
- [ ] Nginx + Gunicorn services restart cleanly.

---

## 8) EC2 Deployment Steps (Gunicorn + Nginx + Go Live)

## 8.1 Server Provisioning
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx git
```

## 8.2 App Setup
```bash
git clone <your-repo-url> virtual-career-counselor
cd virtual-career-counselor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 8.3 Environment Variables
Create `.env` with production values:
- `SECRET_KEY`
- `GROQ_API_KEY`
- `AWS_REGION`
- `SNS_TOPIC_ARN`
- DynamoDB table names

## 8.4 Run with Gunicorn (quick test)
```bash
gunicorn --bind 0.0.0.0:5000 run:app
```

## 8.5 Systemd Service for Gunicorn
Create `/etc/systemd/system/vcc.service` and configure working directory, venv path, and exec command. Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable vcc
sudo systemctl start vcc
sudo systemctl status vcc
```

## 8.6 Nginx Reverse Proxy
Create Nginx site config:
- Listen on port 80
- Proxy pass to `http://127.0.0.1:5000`
- Forward headers (`Host`, `X-Forwarded-For`, `X-Forwarded-Proto`)

Enable and reload:
```bash
sudo ln -s /etc/nginx/sites-available/vcc /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 8.7 HTTPS (Recommended)
Use Let’s Encrypt (Certbot) or ACM + ALB setup.

## 8.8 Go-Live Validation
- [ ] Open public IP/domain and verify app loads.
- [ ] Complete full happy-path flow.
- [ ] Check logs for errors:
  - `journalctl -u vcc -f`
  - `sudo tail -f /var/log/nginx/error.log`

---

## 9) Same-Day Execution Checklist (Quick Master Tracker)

### Core MVP
- [x] Local project scaffold complete
- [x] Auth complete (register/login/logout/session)
- [x] DynamoDB `Users` + `Queries` + `AdminLogs` integrated
- [x] Career AI feature complete
- [x] Course AI feature complete
- [x] Insights AI feature complete
- [x] SNS notifications complete
- [x] Admin dashboard complete

### 8 Killer Features (v2.0)
- [x] Resume Analysis & Job Matching (PDF/DOCX upload + AI analysis)
- [x] Personalized Learning Path with Progress Tracking (8-week roadmap)
- [x] Salary Negotiation Simulator (4-round multi-turn AI chat)
- [x] Interview Prep Simulator (10 companies × 10 roles, 5 questions)
- [x] Career Pivot Analyzer (transferable skills + transition plan)
- [x] Real-Time Market Trends Dashboard (10 industries + custom)
- [x] Peer Comparison & Benchmarking (percentile ranking)
- [x] Gamification — Badges & Leaderboard (9+ badges, auto-award, top-20)
- [x] 3 New DynamoDB tables (`Conversations`, `UserProgress`, `UserBadges`)
- [x] Navigation updated with "AI Tools" dropdown
- [x] Dashboard redesigned with all 11 feature cards

### 16 Advanced Features (v3.0)
- [x] AI Chatbot with RAG toggle (multi-turn, session-based)
- [x] Cover Letter Generator (resume + JD + company → tailored letter)
- [x] GitHub Profile Analyzer (GitHub API → AI career analysis)
- [x] Skill Gap Heatmap (Chart.js 4.4 bar chart + readiness score)
- [x] Query History (browse, filter by type, view detail)
- [x] PDF Export (xhtml2pdf styled reports)
- [x] Dark Mode (CSS + JS + localStorage persistence)
- [x] Bookmarks (save/remove AI results)
- [x] Voice Input (Web Speech API on chatbot, mentor, GD)
- [x] Mock Group Discussion (5+ round AI-moderated with evaluation)
- [x] AI Mentor Chat (persistent goal-based mentorship via DynamoDB)
- [x] RAG Job Matching (lightweight TF-IDF engine, rag_store.json)
- [x] Weekly Career Digest (15 industries, on-demand generation)
- [x] Team/Classroom Mode (create/join by code, member activity)
- [x] Navigation overhaul (2 mega dropdowns, dark mode toggle)
- [x] Dashboard redesigned with 22 feature cards in 5 sections
- [x] 4 New DynamoDB tables (`Bookmarks`, `MentorChats`, `Classrooms`, `DigestPreferences`)
- [x] 2 New services (`rag_service.py`, `pdf_service.py`)
- [x] 8 New Groq AI functions + 7 system prompts
- [x] 10 New blueprints (23 total), 53 routes confirmed

### Final Steps
- [ ] Tests + QA complete
- [ ] EC2 deployed with Nginx + Gunicorn
- [ ] Live smoke tests passed

---

## 11) Complete Feature Summary (v3.0)

| # | Feature | Route | Blueprint | Template | AI Function | Version |
|---|---------|-------|-----------|----------|-------------|---------|
| 1 | Career Path Explorer | `/career/` | `career_bp` | `career_result.html` | `generate_career_overview()` | v1.0 |
| 2 | Course Recommendations | `/courses/` | `courses_bp` | `course_result.html` | `generate_course_recommendations()` | v1.0 |
| 3 | Job Market Insights | `/insights/` | `insights_bp` | `insights_result.html` | `generate_market_insights()` | v1.0 |
| 4 | Resume Analysis | `/resume/` | `resume_bp` | `upload.html` | `analyze_resume()` | v2.0 |
| 5 | Learning Path | `/learning/` | `learning_bp` | `roadmap.html` | `generate_learning_path()` | v2.0 |
| 6 | Salary Negotiation | `/negotiation/` | `negotiation_bp` | `simulator.html` | `negotiation_reply()` | v2.0 |
| 7 | Interview Prep | `/interview/` | `interview_bp` | `prep.html` | `interview_reply()` | v2.0 |
| 8 | Career Pivot | `/pivot/` | `pivot_bp` | `analyzer.html` | `analyze_career_pivot()` | v2.0 |
| 9 | Market Trends | `/trends/` | `trends_bp` | `dashboard.html` | `generate_trends_report()` | v2.0 |
| 10 | Peer Comparison | `/peers/` | `peers_bp` | `comparison.html` | `generate_peer_comparison()` | v2.0 |
| 11 | Badges & Leaderboard | `/gamification/` | `gamification_bp` | `badges.html` | Auto-award rules | v2.0 |
| 12 | AI Chatbot | `/chatbot/` | `chatbot_bp` | `chat.html` | `chatbot_reply()` | v3.0 |
| 13 | Cover Letter Generator | `/cover-letter/` | `cover_letter_bp` | `generate.html` | `generate_cover_letter()` | v3.0 |
| 14 | GitHub Analyzer | `/github/` | `github_bp` | `analyze.html` | `analyze_github_profile()` | v3.0 |
| 15 | Skill Gap Heatmap | `/skill-gap/` | `skill_gap_bp` | `analyze.html` | `analyze_skill_gap()` | v3.0 |
| 16 | Query History | `/history/` | `history_bp` | `index.html`, `detail.html` | — | v3.0 |
| 17 | PDF Export | `/history/export/<id>` | `history_bp` | — | `pdf_service.generate_pdf()` | v3.0 |
| 18 | Bookmarks | `/history/bookmarks` | `history_bp` | `bookmarks.html` | — | v3.0 |
| 19 | Mock Group Discussion | `/gd/` | `gd_bp` | `start.html`, `discuss.html` | `group_discussion_reply()` | v3.0 |
| 20 | AI Mentor Chat | `/mentor/` | `mentor_bp` | `chat.html` | `mentor_reply()` | v3.0 |
| 21 | RAG Job Matching | `/job-match/` | `job_match_bp` | `match.html` | `rag_enhanced_query()` | v3.0 |
| 22 | Weekly Digest | `/digest/` | `digest_bp` | `preferences.html`, `result.html` | `generate_weekly_digest()` | v3.0 |
| 23 | Team/Classroom | `/classroom/` | `classroom_bp` | `index.html`, `view.html` | — | v3.0 |
| 24 | Dark Mode | — | — | `base.html` + `app.js` | — | v3.0 |
| 25 | Voice Input | — | — | `app.js` | Web Speech API | v3.0 |
| 26 | Admin Dashboard | `/admin/` | `admin_bp` | `dashboard.html` | — | v1.0 |
| 27 | Auth System | `/auth/` | `auth_bp` | `login.html`, `register.html` | — | v1.0 |

**Total: 23 Blueprints | 53 Routes | 10 DynamoDB Tables | 20+ AI-Powered Functions | 27 Features**

### Technology Stack (v3.0)

| Component | Technology | Version |
|-----------|-----------|---------|
| Backend Framework | Flask | 3.1.x |
| AI Model | Groq (Llama 3.3 70B Versatile) | Latest |
| Database | AWS DynamoDB (On-Demand) | — |
| Notifications | AWS SNS | — |
| PDF Generation | xhtml2pdf | 0.2.x |
| RAG Engine | Custom TF-IDF (cosine similarity) | — |
| Resume Parsing | PyPDF2 + python-docx | — |
| HTTP Client | requests | 2.32.x |
| Password Hashing | bcrypt | 4.x |
| Frontend CSS | Bootstrap | 5.3.3 |
| Frontend Icons | Bootstrap Icons | 1.11.3 |
| Charts | Chart.js | 4.4.0 |
| Voice Input | Web Speech API | Browser native |
| Dark Mode | CSS + localStorage | — |
| Deployment | Gunicorn + Nginx on EC2 | — |

---

## 12) Post-MVP Enhancements (Future Sprints)
- Add CloudWatch alarms + SNS for operational alerts.
- Add stronger analytics and user feedback/rating collection.
- Add caching for repeated prompts (Redis or Flask-Caching).
- Add CI/CD pipeline (GitHub Actions).
- Add interview prep for custom companies (user-entered).
- Add resume version comparison (upload multiple resumes).
- Add social sharing for badges.
- Add multi-language AI prompt parameter support.
- Add scheduled weekly digest emails (AWS Lambda + EventBridge).
- Add OAuth login (Google, GitHub).
- Add file upload to classroom for shared resources.
- Add AI-powered career path visualization (interactive graph).

---

## Notes
- Keep scope strict to MVP features.
- Focus on reliability and clean UX over extra features.
- If blocked on optional features, prioritize core user flows and deployment first.
- All new DynamoDB table operations are guarded with try/except to work gracefully even if tables aren't created yet.
