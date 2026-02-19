"""
RAG (Retrieval-Augmented Generation) Service — Lightweight implementation.
Uses TF-IDF similarity for document retrieval without heavy dependencies.
Stores career-related documents and retrieves relevant context for AI prompts.
"""
import os
import json
import math
import re
from typing import Any, Dict, List, Optional, Set
from collections import Counter

# Persistent storage in project directory
_STORE_PATH: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "rag_store.json")
_documents: Optional[List[Dict[str, Any]]] = None


def _load_store() -> List[Dict[str, Any]]:
    """Load documents from JSON file."""
    global _documents
    if _documents is not None:
        return _documents
    if os.path.exists(_STORE_PATH):
        with open(_STORE_PATH, "r", encoding="utf-8") as f:
            _documents = json.load(f)
    else:
        _documents = []
    return _documents or []


def _save_store() -> None:
    """Persist documents to JSON file."""
    with open(_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(_documents or [], f, indent=2, ensure_ascii=False)


def _tokenize(text: str) -> List[str]:
    """Simple tokenizer: lowercase, split on non-alpha, remove stop words."""
    stop_words: Set[str] = {"the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to", "for",
                  "of", "and", "or", "but", "with", "this", "that", "it", "be", "as", "by",
                  "from", "has", "have", "had", "not", "no", "can", "will", "do", "does"}
    tokens: List[str] = re.findall(r"[a-z0-9]+", text.lower())
    return [t for t in tokens if t not in stop_words and len(t) > 1]


def _tfidf_similarity(query: str, document: str) -> float:
    """Calculate TF-IDF cosine similarity between query and document."""
    q_tokens: List[str] = _tokenize(query)
    d_tokens: List[str] = _tokenize(document)
    if not q_tokens or not d_tokens:
        return 0.0

    # Term frequency
    q_tf: Counter[str] = Counter(q_tokens)
    d_tf: Counter[str] = Counter(d_tokens)

    # All terms
    all_terms: Set[str] = set(q_tokens) | set(d_tokens)

    # Simple cosine similarity on TF vectors
    dot_product: float = sum(q_tf.get(t, 0) * d_tf.get(t, 0) for t in all_terms)
    q_norm: float = math.sqrt(sum(v ** 2 for v in q_tf.values()))
    d_norm: float = math.sqrt(sum(v ** 2 for v in d_tf.values()))

    if q_norm == 0 or d_norm == 0:
        return 0.0
    return dot_product / (q_norm * d_norm)


def add_documents(docs: List[Dict[str, Any]]) -> int:
    """
    Add documents to the knowledge base.
    Each doc: {"id": str, "content": str, "metadata": dict}
    """
    store: List[Dict[str, Any]] = _load_store()
    existing_ids: Set[str] = {d["id"] for d in store}
    added: int = 0
    for doc in docs:
        if doc["id"] in existing_ids:
            # Update existing
            for i, d in enumerate(store):
                if d["id"] == doc["id"]:
                    store[i] = doc
                    break
        else:
            store.append(doc)
        added += 1
    _save_store()
    return added


def query_knowledge(query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve the most relevant documents for a query using TF-IDF similarity.
    Returns list of {"content": str, "metadata": dict, "score": float}.
    """
    store: List[Dict[str, Any]] = _load_store()
    if not store:
        return []

    scored: List[Dict[str, Any]] = []
    for doc in store:
        text: str = doc.get("content", "")
        score: float = _tfidf_similarity(query_text, text)
        scored.append({
            "content": text,
            "metadata": doc.get("metadata", {}),
            "score": score,
            "id": doc.get("id", ""),
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:n_results]


def get_rag_context(query: str, n_results: int = 3) -> str:
    """
    Get formatted context string for injection into AI prompts.
    """
    docs: List[Dict[str, Any]] = query_knowledge(query, n_results)
    if not docs:
        return "No relevant context found in knowledge base."
    context_parts: List[str] = []
    for i, doc in enumerate(docs, 1):
        source: str = doc["metadata"].get("source", "Knowledge Base")
        context_parts.append(f"[Source {i}: {source}]\n{doc['content']}")
    return "\n\n---\n\n".join(context_parts)


def get_doc_count() -> int:
    """Return total documents in knowledge base."""
    store: List[Dict[str, Any]] = _load_store()
    return len(store)


def delete_document(doc_id: str) -> None:
    """Remove a document by ID."""
    global _documents
    store: List[Dict[str, Any]] = _load_store()
    _documents = [d for d in store if d.get("id") != doc_id]
    _save_store()


def list_documents(limit: int = 50) -> List[Dict[str, Any]]:
    """List documents in the store."""
    store: List[Dict[str, Any]] = _load_store()
    return store[:limit]


# ── Pre-built career knowledge seed data ─────────────────────────────
SEED_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "tech_trends_2026",
        "content": (
            "Top Technology Trends 2026: AI/ML engineering roles grew 45% YoY. "
            "Cloud-native development (Kubernetes, serverless) is standard. "
            "Cybersecurity roles command 20-30% salary premium. "
            "Full-stack developers average $95K-$180K depending on experience. "
            "Data Engineering surpassed Data Science in job postings. "
            "Key skills: Python, TypeScript, Rust, Go, Terraform, Kubernetes, LLM fine-tuning."
        ),
        "metadata": {"source": "Industry Report 2026", "category": "trends"},
    },
    {
        "id": "salary_data_india_2026",
        "content": (
            "India Tech Salary Benchmarks 2026: "
            "Software Engineer (0-2 yrs): 6-12 LPA | (3-5 yrs): 12-25 LPA | (5-10 yrs): 25-50 LPA. "
            "Data Scientist (0-2 yrs): 8-15 LPA | (3-5 yrs): 18-35 LPA. "
            "Cloud Engineer (0-2 yrs): 7-14 LPA | (3-5 yrs): 15-30 LPA. "
            "DevOps Engineer (3-5 yrs): 15-28 LPA. "
            "Product Manager (3-5 yrs): 20-40 LPA. "
            "Top companies: Google, Microsoft, Amazon, Flipkart, Razorpay, CRED pay 2-3x market."
        ),
        "metadata": {"source": "Salary Survey India 2026", "category": "salary"},
    },
    {
        "id": "salary_data_us_2026",
        "content": (
            "US Tech Salary Benchmarks 2026: "
            "Software Engineer: $90K-$200K+ | Senior: $150K-$350K (FAANG). "
            "Data Scientist: $100K-$180K | ML Engineer: $120K-$250K. "
            "Cloud Architect: $140K-$220K. DevOps: $110K-$180K. "
            "Product Manager: $120K-$220K. Cybersecurity: $100K-$200K. "
            "Remote roles typically 10-15% less than on-site Bay Area rates."
        ),
        "metadata": {"source": "Salary Survey US 2026", "category": "salary"},
    },
    {
        "id": "interview_tips_faang",
        "content": (
            "FAANG Interview Preparation Guide: "
            "Google: Focus on system design + DSA. 5-6 rounds. Emphasis on scalability thinking. "
            "Amazon: Leadership Principles are KEY. Behavioral STAR method crucial. Bar raiser round. "
            "Meta: Move fast culture. Practical coding + system design. 45-min coding rounds. "
            "Apple: Domain expertise matters. Hardware-software integration knowledge valued. "
            "Microsoft: Collaborative problem solving. 4-5 rounds. Growth mindset evaluated. "
            "Preparation timeline: 3-6 months. LeetCode 200+ problems recommended."
        ),
        "metadata": {"source": "Interview Guide", "category": "interview"},
    },
    {
        "id": "career_paths_overview",
        "content": (
            "Popular Career Paths in Tech 2026: "
            "1. AI/ML Engineer: Python, TensorFlow/PyTorch, MLOps, LLM fine-tuning. Growth: 45% YoY. "
            "2. Full Stack Developer: React/Next.js + Node/Python backend. Highest volume of jobs. "
            "3. Cloud/DevOps Engineer: AWS/Azure/GCP, Terraform, K8s. Critical for every company. "
            "4. Data Engineer: Spark, Airflow, dbt, Snowflake. Fastest growing data role. "
            "5. Cybersecurity Analyst: Zero Trust, SIEM, incident response. Talent shortage. "
            "6. Product Manager: Technical PMs earn premium. AI product management emerging. "
            "7. Blockchain/Web3: Solidity, smart contracts. Volatile but high-paying niche."
        ),
        "metadata": {"source": "Career Guide 2026", "category": "career"},
    },
    {
        "id": "certifications_value",
        "content": (
            "Most Valuable Tech Certifications 2026: "
            "AWS Solutions Architect (Associate/Professional): Highest ROI, 20-30% salary boost. "
            "Google Cloud Professional: Growing demand, especially in AI/ML track. "
            "Kubernetes (CKA/CKAD): Essential for DevOps, high demand. "
            "Azure Administrator/Architect: Strong in enterprise market. "
            "CompTIA Security+/CISSP: Required for cybersecurity roles. "
            "Terraform Associate: Infrastructure as Code standard. "
            "PMP/Scrum Master: Still valued for management track. "
            "Google Data Analytics Certificate: Best entry-level credential."
        ),
        "metadata": {"source": "Certification Guide", "category": "certification"},
    },
    {
        "id": "remote_work_trends",
        "content": (
            "Remote Work Trends 2026: "
            "65% of tech companies offer hybrid (3 days office). "
            "Fully remote roles decreased from 2024 peak but stabilized at ~25%. "
            "Remote salaries: SF-based companies pay 85-100% of local rate for remote. "
            "Top remote-friendly companies: GitLab, Automattic, Zapier, Shopify, Coinbase. "
            "Skills for remote success: async communication, self-management, documentation. "
            "International remote hiring growing — companies hiring from India, Eastern Europe, LatAm."
        ),
        "metadata": {"source": "Remote Work Report", "category": "trends"},
    },
    {
        "id": "resume_best_practices",
        "content": (
            "Resume Best Practices 2026: "
            "ATS Optimization: Use standard section headers, avoid tables/columns, include keywords from JD. "
            "Format: 1 page for <5 yrs experience, 2 pages max for senior. PDF format preferred. "
            "Must-have sections: Summary, Experience (STAR format), Skills, Education, Projects. "
            "Quantify achievements: 'Reduced API latency by 40%' > 'Improved performance'. "
            "GitHub/Portfolio link: 85% of hiring managers check it. "
            "Avoid: Objective statements, photos, references section, generic skills like 'MS Office'."
        ),
        "metadata": {"source": "Resume Guide", "category": "resume"},
    },
    {
        "id": "negotiation_strategies",
        "content": (
            "Salary Negotiation Strategies 2026: "
            "Always negotiate — 87% of employers expect it. "
            "Research market rate on Levels.fyi, Glassdoor, Blind before negotiating. "
            "Never give your number first — ask for the company's budget range. "
            "Consider total compensation: base + bonus + equity + benefits + WFH stipend. "
            "Counter offer: Ask 10-20% above their initial offer as starting point. "
            "Leverage competing offers — even verbal ones strengthen your position. "
            "Best time to negotiate: After receiving offer, before accepting. "
            "For India: Negotiate on variable pay, joining bonus, and ESOP vesting schedule."
        ),
        "metadata": {"source": "Negotiation Guide", "category": "negotiation"},
    },
    {
        "id": "freelancing_guide",
        "content": (
            "Freelancing & Gig Economy 2026: "
            "Top platforms: Upwork, Toptal (vetted), Fiverr Pro, Arc.dev. "
            "Highest-paying freelance skills: AI/ML consulting ($150-300/hr), Cloud Architecture ($120-200/hr). "
            "Building clientele: Start on platforms, build portfolio, transition to direct clients. "
            "Pricing: Time-based for consulting, project-based for development. Value-based for senior. "
            "Tax considerations India: Register as sole proprietor or LLP, GST above 20L threshold. "
            "Essential: Strong portfolio website, LinkedIn presence, testimonials, niche specialization."
        ),
        "metadata": {"source": "Freelancing Guide", "category": "career"},
    },
]


def seed_knowledge_base() -> int:
    """Seed the knowledge base with pre-built career documents."""
    count: int = add_documents(SEED_DOCUMENTS)
    return count
