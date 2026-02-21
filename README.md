# Virtual Career Counselor

> **Live:** [https://virtual-career-counselor.onrender.com](https://virtual-career-counselor.onrender.com)

AI-powered career guidance platform with 24 features + real job market data (Adzuna API), built with Flask, Groq AI (Llama 3.3 70B), and AWS services (DynamoDB, SNS, IAM). Deployed on Render.com with Gunicorn.

**Built using Vibe Coding** — AI-assisted rapid development with GitHub Copilot (Claude) for architecture, code generation, testing, and iterative refinement. See the [Build Plan](Virtual_Career_Counselor_MVP_Same_Day_Build_Plan.md) for methodology details.

---

## Features (24 Features + 3 UX Utilities)

### Core AI Features
| # | Feature | Description |
|---|---------|-------------|
| 1 | **Career Path Explorer** | AI career overviews with 10 sections: industry landscape, skills matrix, salary data (Adzuna), career ladder, day-in-the-life, remote potential, project ideas, networking, and 30-day action plan |
| 2 | **Course Recommendations** | 5-8 ranked courses with ROI scores, free alternatives, budget learning path, and optimal learning order |
| 3 | **Job Market Insights** | Real salary data (Adzuna API) + 10-section AI analysis: demand trends, geographic hotspots, emerging niches, and 90-day hiring strategies |
| 4 | **Resume Analyzer** | Upload PDF/DOCX for 100-point scoring rubric (7 categories), ATS compatibility check, auto-rewritten professional summary, and real market matching |
| 5 | **Learning Path Generator** | 4-phase week-by-week roadmaps with daily schedules, assessments, portfolio projects, community resources, and progress tracker |
| 6 | **Salary Negotiation Simulator** | Multi-turn AI HR negotiation with tactic identification, power dynamics, scorecard, ideal scripts, and follow-up email templates |
| 7 | **Interview Prep Simulator** | Company-specific mock interviews with STAR assessment, progressive difficulty, scorecard table, and study guide |
| 8 | **Career Pivot Analyzer** | 11-section analysis: feasibility score, financial planning, salary comparison (Adzuna), 90-day timeline, portfolio conversion, and networking strategy |
| 9 | **Market Trends Dashboard** | Real salary + hiring data (Adzuna) with AI & automation impact analysis, 12-month predictions, and actionable next steps |
| 10 | **Peer Comparison** | Benchmark against real market salaries (Adzuna) with percentile rankings, skill matrix, competitive edge, and 60-day improvement roadmap |
| 11 | **AI Chatbot** | Career Q&A powered by frameworks (STAR, SMART, Ikigai) with real-time web search + PDF export |
| 12 | **Cover Letter Generator** | ATS-optimized cover letters with keyword match report, ATS score, tone analysis, and LinkedIn outreach message |
| 13 | **GitHub Profile Analyzer** | 100-point scoring rubric (6 categories), recruiter first impression, tech stack analysis, and prioritized improvement plan |
| 14 | **Skill Gap Heatmap** | JSON skill analysis with priority levels, learning resources per skill, milestone timeline, and job market fit estimate |
| 15 | **Mock Group Discussion** | 3 distinct AI panelists (Analyst, Contrarian, Pragmatist) with live coaching whispers and 6-category scorecard |
| 16 | **AI Mentor Chat** | Stage-adaptive mentorship (student/mid/senior) with frameworks, action items, and thought-provoking questions |
| 17 | **Smart Career Search** | Tavily + Adzuna real data + Groq AI for live job market intelligence + PDF export |
| 18 | **Weekly Career Digest** | Personalized weekly digest across 15 industries |

### Platform Features
| # | Feature | Description |
|---|---------|-------------|
| 19 | **Email Reports (SNS)** | Send any AI report to your email via AWS SNS |
| 20 | **Admin Dashboard** | User management, query logs, and system health metrics |
| 21 | **Gamification** | Badges and leaderboard for engagement tracking |
| 22 | **Query History + PDF Export** | Browse past queries and export as styled PDFs |
| 23 | **Bookmarks** | Save and manage favorite AI results |
| 24 | **Team/Classroom Mode** | Create and join collaborative career rooms |

### UX Utilities
| Utility | Description |
|---------|-------------|
| **Dark Mode** | Full dark theme via CSS + localStorage toggle |
| **Voice Input** | Browser-based speech-to-text via Web Speech API |
| **Multi-language Support** | AI responses in user-preferred language (prompt parameter) |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.10+ / Flask 3.1 |
| **AI Engine** | Groq API (Llama 3.3 70B Versatile) — groq 1.0 |
| **Web Search** | Tavily AI (real-time web context for AI) — tavily-python 0.7 |
| **Job Market Data** | Adzuna API (real salaries, live listings, top employers) |
| **Database** | AWS DynamoDB (10 tables, PAY_PER_REQUEST) |
| **Notifications** | AWS SNS (email reports) |
| **Auth** | bcrypt 5.0 password hashing + Flask-Session |
| **Security** | Flask-WTF 1.2 (CSRF) + Flask-Limiter 4.1 (rate limiting) |
| **PDF Export** | xhtml2pdf 0.2.17 |
| **Testing** | pytest (62 tests across 7 test modules) |
| **CI/CD** | GitHub Actions (lint + test on push/PR) |
| **Markdown Rendering** | markdown 3.10 (tables, fenced_code, nl2br) via custom Jinja2 `md` filter |
| **Resume Parsing** | pypdf 6.7 (PDF) + python-docx 1.2 (DOCX) |
| **Frontend** | Bootstrap 5.3 + Chart.js 4.4 + Jinja2 |
| **Hosting** | Render.com (PaaS) + Gunicorn 25.x |

---

## Quick Start (Local Development)

```bash
# 1. Clone and enter directory
git clone https://github.com/YOUR_USERNAME/virtual-career-counselor.git
cd virtual-career-counselor

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and fill environment variables
copy .env.example .env        # Windows
# cp .env.example .env        # Linux/Mac
# Edit .env with your actual keys

# 5. Create DynamoDB tables
python scripts/create_dynamodb_tables.py

# 6. Seed admin user
python scripts/seed_admin.py

# 7. Run the app
python run.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Project Structure

```
virtual-career-counselor/
├── app/
│   ├── __init__.py              # App factory (23 blueprints)
│   ├── auth/                    # Registration, Login, Logout
│   ├── career/                  # Career Path Explorer
│   ├── courses/                 # Course Recommendations
│   ├── insights/                # Job Market Insights
│   ├── resume/                  # Resume Analyzer
│   ├── learning/                # Learning Path + Progress
│   ├── negotiation/             # Salary Negotiation Simulator
│   ├── interview/               # Interview Prep Simulator
│   ├── pivot/                   # Career Pivot Analyzer
│   ├── trends/                  # Market Trends Dashboard
│   ├── peers/                   # Peer Comparison
│   ├── gamification/            # Badges & Leaderboard
│   ├── chatbot/                 # AI Chatbot (Tavily-enhanced)
│   ├── cover_letter/            # Cover Letter Generator
│   ├── github_analyzer/         # GitHub Profile Analyzer
│   ├── skill_gap/               # Skill Gap Heatmap
│   ├── history/                 # Query History + PDF Export
│   ├── mentor/                  # AI Mentor Chat
│   ├── group_discussion/        # Mock Group Discussion
│   ├── job_match/               # Smart Career Search (Tavily)
│   ├── classroom/               # Team/Classroom Mode
│   ├── digest/                  # Weekly Career Digest
│   ├── admin/                   # Admin Dashboard
│   ├── services/
│   │   ├── groq_service.py      # Groq AI (all 18 AI functions + deep prompts)
│   │   ├── dynamo_service.py    # DynamoDB CRUD (10 tables)
│   │   ├── sns_service.py       # AWS SNS email service
│   │   ├── pdf_service.py       # PDF export (xhtml2pdf)
│   │   ├── resume_parser.py     # PDF/DOCX text extraction
│   │   ├── web_search_service.py # Tavily AI web search
│   │   └── adzuna_service.py    # Adzuna API (real salaries, jobs, companies)
│   ├── templates/               # 31 Jinja2 HTML templates
│   └── static/                  # CSS, JS, assets
├── scripts/
│   ├── create_dynamodb_tables.py # DynamoDB table creation
│   └── seed_admin.py            # Admin user seeding
├── config.py                    # App configuration
├── run.py                       # Entry point (gunicorn run:app)
├── tests/                       # pytest test suite (62 tests)
├── .github/workflows/ci.yml     # GitHub Actions CI pipeline
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
└── .gitignore
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in your values:

| Variable | Required | Description |
|----------|----------|-------------|
| `SECRET_KEY` | Yes | Flask session encryption key |
| `FLASK_ENV` | No | `development` (default) or `production` |
| `PORT` | No | Server port (default: `10000`; Render injects automatically) |
| `GROQ_API_KEY` | Yes | Groq API key for AI features |
| `GROQ_MODEL` | No | Model name (default: `llama-3.3-70b-versatile`) |
| `AWS_ACCESS_KEY_ID` | Yes | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | Yes | AWS IAM secret key |
| `AWS_REGION` | Yes | AWS region (default: `ap-south-1`) |
| `SNS_TOPIC_ARN` | Yes | AWS SNS topic ARN for email notifications |
| `DYNAMODB_USERS_TABLE` | No | Users table name (default: `Users`) |
| `DYNAMODB_QUERIES_TABLE` | No | Queries table name (default: `Queries`) |
| `DYNAMODB_ADMINLOGS_TABLE` | No | AdminLogs table name (default: `AdminLogs`) |
| `DYNAMODB_CONVERSATIONS_TABLE` | No | Conversations table name (default: `Conversations`) |
| `DYNAMODB_PROGRESS_TABLE` | No | UserProgress table name (default: `UserProgress`) |
| `DYNAMODB_BADGES_TABLE` | No | UserBadges table name (default: `UserBadges`) |
| `DYNAMODB_BOOKMARKS_TABLE` | No | Bookmarks table name (default: `Bookmarks`) |
| `DYNAMODB_MENTOR_TABLE` | No | MentorChats table name (default: `MentorChats`) |
| `DYNAMODB_CLASSROOMS_TABLE` | No | Classrooms table name (default: `Classrooms`) |
| `DYNAMODB_DIGEST_TABLE` | No | DigestPreferences table name (default: `DigestPreferences`) |
| `GITHUB_TOKEN` | No | GitHub personal access token (for GitHub Analyzer) |
| `TAVILY_API_KEY` | No | Tavily AI API key (enables real-time web search) |
| `ADZUNA_APP_ID` | No | Adzuna API app ID (enables real salary data & live listings) |
| `ADZUNA_APP_KEY` | No | Adzuna API app key (free at developer.adzuna.com) |
| `ADMIN_EMAIL` | No | Admin email for seeding (default: `admin@example.com`) |

---

## Security

| Feature | Implementation |
|---------|----------------|
| **CSRF Protection** | Flask-WTF `CSRFProtect` — hidden token auto-injected into every `POST` form; `fetch()` monkey-patched to add `X-CSRFToken` header on non-GET requests |
| **Rate Limiting** | Flask-Limiter — global default `200/hr, 50/min`; stricter `10/min` on all 18 AI endpoints. Uses in-memory storage (counters are per-worker and reset on deploy — acceptable for a portfolio-scale project; swap to Redis via `RATELIMIT_STORAGE_URI` for production) |
| **Password Hashing** | bcrypt (cost factor 12) |
| **Session Security** | Server-side filesystem sessions via Flask-Session |

---

## Testing

```bash
# Run the full test suite
pip install pytest
python -m pytest tests/ -v --tb=short
```

62 tests across 7 modules covering all 23 blueprints:

| Module | Coverage |
|--------|----------|
| `test_auth.py` | Login, register, logout, session guards |
| `test_core_features.py` | Career, courses, insights |
| `test_chat_features.py` | Chatbot, mentor, group discussion |
| `test_interactive_features.py` | Negotiation, interview, cover letter, resume |
| `test_analysis_features.py` | Pivot, trends, peers, skill gap, GitHub |
| `test_platform_features.py` | History, gamification, learning, job match, classroom, digest, admin |
| `test_security.py` | CSRF enforcement, rate limiter init, input length |

---

## CI/CD (GitHub Actions)

Every push to `main` and every pull request triggers the CI pipeline (`.github/workflows/ci.yml`):

1. Checkout code
2. Set up Python 3.12 with pip cache
3. Install dependencies
4. Run `pytest` (62 tests)

---

## Deployment (Render.com)

The app is deployed on [Render.com](https://render.com) with GitHub auto-deploy.

### Why Render instead of EC2?

| Concern | Render (chosen) | EC2 |
|---------|-----------------|-----|
| **Setup** | Zero-config PaaS — push to `main` and it deploys | Manual AMI, security groups, Nginx, systemd |
| **HTTPS** | Automatic TLS via Let's Encrypt | Manual Certbot / ACM + ALB |
| **Scaling** | One-click vertical scaling | Manual ASG / instance resize |
| **Cost** | Free tier sufficient for portfolio-scale | ~$8+/mo for t3.micro |
| **Maintenance** | Managed OS/runtime patches | Self-managed patching |

For a portfolio/demo project, Render eliminates ops overhead while keeping the same Flask + Gunicorn + DynamoDB architecture production-ready.

- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn run:app --bind 0.0.0.0:$PORT`
- **Environment:** Python 3
- **Branch:** `main` (auto-deploys on push)
- Manage secrets via Render's **Environment Variables** dashboard

See `Virtual_Career_Counselor_MVP_Same_Day_Build_Plan.md` Section 8 for full deployment steps.

---

## Architecture Highlights — Real-time Web Integration via Tavily API

- **App Factory Pattern** — modular Flask app with 23 registered blueprints
- **Lazy-init AI Clients** — Groq and Tavily clients initialized on first use
- **Real-time Web Integration via Tavily API** — Every AI feature auto-enriched with live web data; no local vector DB or static knowledge base
- **Real Job Market Data via Adzuna API** — Nine features (Insights, Trends, Peers, Skill Gap, Resume, Smart Search, Career Path, Career Pivot, Weekly Digest) inject real salary figures, live job listings, and top hiring companies into AI prompts so outputs cite actual market evidence
- **Smart Career Search** — Dedicated Tavily + Adzuna → Groq pipeline prioritizing salary data & job links
- **Markdown → HTML Rendering** — Global Jinja2 `| md` filter converts AI markdown to styled HTML with table, code, and link support across all 19 templates
- **Deep AI Prompts** — Every AI feature uses rich, structured system prompts with scoring rubrics, tables, multi-section output formats, and actionable frameworks (STAR, SMART, Ikigai, BATNA)
- **On-the-fly PDF Export** — Chatbot and Smart Career Search conversations downloadable as styled PDFs via xhtml2pdf (no disk storage)
- **Resume Parsing via pypdf** — Resumes read one-by-one on upload using `pypdf` (no file storage needed)
- **Type-Safe Codebase** — Full type hints across all modules (Pyright strict mode: 0 errors)
- **Security** — CSRF protection (Flask-WTF) + rate limiting (Flask-Limiter, 10 req/min on AI endpoints)
- **Automated Testing** — 62 pytest tests across all 23 blueprints; GitHub Actions CI on every push
- **Graceful Degradation** — Optional services (Tavily, GitHub, SNS) fail silently when unconfigured

---

## License

This project is for educational and portfolio purposes.
