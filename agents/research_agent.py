"""
Research Agent — searches for information related to a given query.
Specialized for Release Readiness topics (testing, deployment, security, etc.)
No LLM API key required — uses DuckDuckGo search.
"""
import logging
from tools.search_tool import SearchTool

logger = logging.getLogger(__name__)


class ResearchAgent:
    """
    A research agent that uses DuckDuckGo to gather web information
    about release readiness topics.
    """

    def __init__(self):
        self.search_tool = SearchTool()
        self.name = "ResearchAgent"

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
