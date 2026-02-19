# Virtual Career Counselor

AI-powered career guidance platform built with Flask, Groq API, and AWS (EC2, DynamoDB, SNS, IAM).

## Features
- **Career Path Explorer** — AI-generated career overviews with skills, certifications, and roadmaps
- **Course Recommendations** — Personalized course suggestions based on interests, skill level, and goals
- **Job Market Insights** — Salary ranges, in-demand skills, demand trends, and hiring hotspots
- **Email Reports** — Send any AI report to your email via AWS SNS
- **Admin Dashboard** — User management, query logs, and system health metrics

## Tech Stack
- Python 3.10+ / Flask 3.x
- Groq API (LLaMA 3 / Mixtral)
- AWS DynamoDB, SNS, IAM
- Bootstrap 5 frontend

## Quick Start

```bash
# 1. Clone and enter directory
cd virtual-career-counselor

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and fill environment variables
copy .env.example .env
# Edit .env with your actual keys

# 5. Create DynamoDB tables
python scripts/create_dynamodb_tables.py

# 6. Seed admin user
python scripts/seed_admin.py

# 7. Run the app
python run.py
```

Open http://localhost:5000 in your browser.

## Project Structure
```
app/
├── auth/        # Registration, Login, Logout
├── career/      # Career path AI exploration
├── courses/     # Course recommendations AI
├── insights/    # Job market insights AI
├── admin/       # Admin dashboard
├── services/    # groq_service, dynamo_service, sns_service
├── templates/   # Jinja2 HTML templates
└── static/      # CSS, JS
```

## Environment Variables
See `.env.example` for all required variables.

## Deployment (EC2)
See `Virtual_Career_Counselor_MVP_Same_Day_Build_Plan.md` Section 8 for full deployment steps.
