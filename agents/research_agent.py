"""
Research Agent — searches for information related to a given query.
Specialized for Release Readiness topics (testing, deployment, security, etc.)

Mode selection (set in .env or environment):
  USE_LOCAL_KB=false  → DuckDuckGo web search (requires internet)
  USE_LOCAL_KB=true   → Local knowledge base (VDI offline mode ✅)
"""
import logging
from config import USE_LOCAL_KB, RELEASE_DOMAINS

if USE_LOCAL_KB:
    from tools.local_knowledge_tool import LocalKnowledgeTool as SearchBackend
    _MODE = "🗂️  LOCAL KB (offline)"
else:
    from tools.search_tool import SearchTool as SearchBackend
    _MODE = "🌐 WEB SEARCH (online)"

logger = logging.getLogger(__name__)
logger.info(f"[ResearchAgent] Search mode: {_MODE}")


class ResearchAgent:
    """
    A research agent that queries either DuckDuckGo (online) or a
    local knowledge base (offline/VDI mode) based on USE_LOCAL_KB config.
    """

    def __init__(self):
        self.search_tool = SearchBackend()
        self.name = "ResearchAgent"
        self.mode = _MODE

    def run(self, query: str) -> dict:
        """
        Execute a research task for the given query.

        Args:
            query: The topic or question to research.

        Returns:
            A dict with 'agent', 'query', 'raw_results', and 'formatted_output'.
        """
        logger.info(f"[{self.name}] Running research for: '{query}'")

        # Enrich query with release readiness context
        enriched_query = f"software release readiness {query}"
        raw_results = self.search_tool.search(enriched_query)
        formatted = self.search_tool.format_results(raw_results)

        return {
            "agent": self.name,
            "query": query,
            "enriched_query": enriched_query,
            "raw_results": raw_results,
            "formatted_output": formatted,
            "result_count": len(raw_results),
        }

    def get_release_checklist_info(self, domain: str) -> dict:
        """
        Research a specific release readiness domain (e.g., 'testing', 'security').

        Args:
            domain: One of the release readiness domains (testing, deployment, etc.)

        Returns:
            Research result dict.
        """
        query = f"release readiness {domain} checklist best practices"
        return self.run(query)
