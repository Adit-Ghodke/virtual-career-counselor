# Virtual Career Counselor

> **Live:** [https://virtual-career-counselor.onrender.com](https://virtual-career-counselor.onrender.com)

AI-powered career guidance platform with 27 features, built with Flask, Groq AI (Llama 3.3 70B), and AWS services (DynamoDB, SNS, IAM). Deployed on Render.com with Gunicorn.

---

## Features (27 Total)

### Core AI Features
| # | Feature | Description |
|---|---------|-------------|
| 1 | **Career Path Explorer** | AI-generated career overviews with skills, certifications, and roadmaps |
| 2 | **Course Recommendations** | Personalized course suggestions based on interests, skill level, and goals |
| 3 | **Job Market Insights** | Salary ranges, in-demand skills, demand trends, and hiring hotspots |
| 4 | **Resume Analyzer** | Upload PDF/DOCX resumes for AI-powered feedback and scoring |
| 5 | **Learning Path Generator** | Personalized roadmaps with progress tracking |
| 6 | **Salary Negotiation Simulator** | Multi-turn AI chat to practice salary negotiations |
| 7 | **Interview Prep Simulator** | Company-specific mock interviews with AI feedback |
| 8 | **Career Pivot Analyzer** | Evaluate career change feasibility with transition plans |
| 9 | **Market Trends Dashboard** | Real-time industry trends analysis |
| 10 | **Peer Comparison** | Benchmark your profile against industry peers |
| 11 | **AI Chatbot** | General career Q&A with real-time web search enrichment + PDF export |
| 12 | **Cover Letter Generator** | AI-crafted cover letters tailored to job descriptions |
| 13 | **GitHub Profile Analyzer** | Analyze GitHub profiles for career insights via GitHub API |
| 14 | **Skill Gap Heatmap** | Visual skill gap analysis with Chart.js heatmaps |
| 15 | **Mock Group Discussion** | AI-moderated multi-round group discussions |
| 16 | **AI Mentor Chat** | Persistent goal-based mentorship conversations |
| 17 | **Smart Career Search** | Tavily web search + Groq AI for real-time job market intelligence + PDF export |
| 18 | **Weekly Career Digest** | Personalized weekly digest across 15 industries |

### Platform Features
| # | Feature | Description |
|---|---------|-------------|
| 19 | **Email Reports (SNS)** | Send any AI report to your email via AWS SNS |
| 20 | **Admin Dashboard** | User management, query logs, and system health metrics |
| 21 | **Gamification** | Badges and leaderboard for engagement tracking |
| 22 | **Query History + PDF Export** | Browse past queries and export as styled PDFs |
| 23 | **Bookmarks** | Save and manage favorite AI results |
| 24 | **Dark Mode** | Full dark theme via CSS + localStorage |
| 25 | **Voice Input** | Browser-based speech-to-text via Web Speech API |
| 26 | **Team/Classroom Mode** | Create and join collaborative career rooms |
| 27 | **Multi-language Support** | AI responses in user-preferred language |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.10+ / Flask 3.x |
| **AI Engine** | Groq API (Llama 3.3 70B Versatile) |
| **Web Search** | Tavily AI (real-time web context for AI) |
| **Database** | AWS DynamoDB (10 tables, PAY_PER_REQUEST) |
| **Notifications** | AWS SNS (email reports) |
| **Auth** | bcrypt password hashing + Flask-Session |
| **PDF Export** | xhtml2pdf |
| **Markdown Rendering** | markdown (tables, fenced_code, nl2br) via custom Jinja2 `md` filter |
| **Resume Parsing** | pypdf (PDF) + python-docx (DOCX) |
| **Frontend** | Bootstrap 5.3 + Chart.js 4.4 + Jinja2 |
| **Hosting** | Render.com (PaaS) + Gunicorn |

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
│   │   ├── groq_service.py      # Groq AI (all 17+ AI functions)
│   │   ├── dynamo_service.py    # DynamoDB CRUD (10 tables)
│   │   ├── sns_service.py       # AWS SNS email service
│   │   ├── pdf_service.py       # PDF export (xhtml2pdf)
│   │   ├── resume_parser.py     # PDF/DOCX text extraction
│   │   └── web_search_service.py # Tavily AI web search
│   ├── templates/               # 31 Jinja2 HTML templates
│   └── static/                  # CSS, JS, assets
├── scripts/
│   ├── create_dynamodb_tables.py # DynamoDB table creation
│   └── seed_admin.py            # Admin user seeding
├── config.py                    # App configuration
├── run.py                       # Entry point (gunicorn run:app)
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
| `ADMIN_EMAIL` | No | Admin email for seeding (default: `admin@example.com`) |

---

## Deployment (Render.com)

The app is deployed on [Render.com](https://render.com) with GitHub auto-deploy:

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
- **Smart Career Search** — Dedicated Tavily → Groq pipeline prioritizing salary data & job links
- **Markdown → HTML Rendering** — Global Jinja2 `| md` filter converts AI markdown to styled HTML with table, code, and link support across all 19 templates
- **On-the-fly PDF Export** — Chatbot and Smart Career Search conversations downloadable as styled PDFs via xhtml2pdf (no disk storage)
- **Resume Parsing via pypdf** — Resumes read one-by-one on upload using `pypdf` (no file storage needed)
- **Type-Safe Codebase** — Full type hints across all modules (Pyright strict mode: 0 errors)
- **Graceful Degradation** — Optional services (Tavily, GitHub, SNS) fail silently when unconfigured

---

## License

This project is for educational and portfolio purposes.
