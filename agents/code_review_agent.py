import logging
from config import USE_LOCAL_KB

if USE_LOCAL_KB:
    from tools.local_knowledge_tool import LocalKnowledgeTool as SearchBackend
    _MODE = "🗂️  LOCAL KB (offline)"
else:
    from tools.search_tool import SearchTool as SearchBackend
    _MODE = "🌐 WEB SEARCH (online)"

logger = logging.getLogger(__name__)

class CodeReviewAgent:
    """
    Agent specialized in evaluating code standards and review guidelines
    to ensure adherence to release criteria.
    """

    def __init__(self):
        self.search_tool = SearchBackend()
        self.name = "CodeReviewAgent"
        self.mode = _MODE

    def run(self, query: str) -> dict:
        """
        Execute code review evaluation for the given query.

        Args:
            query: The domain or question to review.

        Returns:
            A dict with 'agent', 'query', 'raw_results', and 'formatted_output'.
        """
        logger.info(f"[{self.name}] Analyzing code standards for: '{query}'")

        # Enrich query with coding standards context
        enriched_query = f"coding standards review guidelines {query}"
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
