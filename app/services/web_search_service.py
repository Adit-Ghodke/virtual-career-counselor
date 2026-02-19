"""
Tavily AI Web Search Service — provides real-time web context for AI features.
Automatically enriches every AI query with fresh web data and source citations.
"""
import os
import logging
from typing import Any, Dict, List, Optional

logger: logging.Logger = logging.getLogger(__name__)

_client: Optional[Any] = None


def _get_tavily_client() -> Optional[Any]:
    """Lazy-initialise the Tavily client. Returns None if no API key."""
    global _client
    if _client is None:
        api_key: str = os.environ.get("TAVILY_API_KEY", "") or ""
        if not api_key:
            logger.warning("TAVILY_API_KEY not set — web search disabled.")
            return None
        try:
            from tavily import TavilyClient  # type: ignore[import-untyped]
            _client = TavilyClient(api_key=api_key)
        except Exception as e:
            logger.error(f"Failed to initialise Tavily client: {e}")
            return None
    return _client


def search_web(query: str, max_results: int = 5, search_depth: str = "basic") -> Dict[str, Any]:
    """
    Search the web using Tavily AI and return structured results.

    Args:
        query: The search query (will be career-focused automatically).
        max_results: Number of results to return (default 5).
        search_depth: 'basic' (fast) or 'advanced' (thorough).

    Returns:
        dict with keys:
            - context: str — formatted text block to inject into AI prompts
            - sources: list[dict] — list of {title, url, snippet} for citations
            - success: bool — whether the search succeeded
    """
    client: Optional[Any] = _get_tavily_client()
    if client is None:
        return {"context": "", "sources": [], "success": False}

    try:
        # Enhance query with career focus for better results
        enhanced_query: str = f"{query} career jobs industry 2025 2026"

        response: Dict[str, Any] = client.search(
            query=enhanced_query,
            max_results=max_results,
            search_depth=search_depth,
            include_answer=True,
        )

        # Extract results
        sources: List[Dict[str, str]] = []
        context_parts: List[str] = []

        # Include Tavily's AI-generated answer if available
        if response.get("answer"):
            context_parts.append(f"Web Search Summary: {response['answer']}")

        # Process individual results
        for result in response.get("results", []):
            title: str = result.get("title", "")
            url: str = result.get("url", "")
            content: str = result.get("content", "")

            sources.append({
                "title": title,
                "url": url,
                "snippet": content[:200],
            })
            context_parts.append(f"- [{title}]({url}): {content[:300]}")

        context: str = "\n".join(context_parts) if context_parts else ""

        return {
            "context": context,
            "sources": sources,
            "success": True,
        }

    except Exception as e:
        logger.error(f"Tavily web search failed: {e}")
        return {"context": "", "sources": [], "success": False}


def format_sources_markdown(sources: List[Dict[str, str]]) -> str:
    """Format sources as a markdown citation block for display."""
    if not sources:
        return ""
    lines: List[str] = ["\n\n---\n**Sources:**"]
    for i, src in enumerate(sources, 1):
        title: str = src.get("title", "Source")
        url: str = src.get("url", "#")
        lines.append(f"{i}. [{title}]({url})")
    return "\n".join(lines)
