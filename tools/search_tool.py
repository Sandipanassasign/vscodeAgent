"""
Search Tool — wraps DuckDuckGo search for use by agents.
No API key required.
"""
import logging
from ddgs import DDGS
from config import MAX_SEARCH_RESULTS

logger = logging.getLogger(__name__)


class SearchTool:
    """
    A free web search tool powered by DuckDuckGo.
    Used by ResearchAgent to find information without any API key.
    """

    def __init__(self):
        self.max_results = MAX_SEARCH_RESULTS

    def search(self, query: str) -> list[dict]:
        """
        Run a web search and return structured results.

        Args:
            query: The search query string.

        Returns:
            A list of dicts with 'title', 'href', and 'body' keys.
        """
        logger.info(f"[SearchTool] Searching for: '{query}'")
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=self.max_results))
            logger.info(f"[SearchTool] Found {len(results)} results.")
            return results
        except Exception as e:
            logger.error(f"[SearchTool] Search failed: {e}")
            return [{"title": "Error", "href": "", "body": str(e)}]

    def format_results(self, results: list[dict]) -> str:
        """Format raw search results into readable text."""
        if not results:
            return "No results found."

        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"[{i}] {r.get('title', 'No Title')}\n"
                f"    URL: {r.get('href', 'N/A')}\n"
                f"    {r.get('body', '')[:200]}..."
            )
        return "\n\n".join(formatted)
