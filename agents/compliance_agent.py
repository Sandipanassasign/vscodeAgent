import logging
from config import USE_LOCAL_KB

if USE_LOCAL_KB:
    from tools.local_knowledge_tool import LocalKnowledgeTool as SearchBackend
    _MODE = "🗂️  LOCAL KB (offline)"
else:
    from tools.search_tool import SearchTool as SearchBackend
    _MODE = "🌐 WEB SEARCH (online)"

logger = logging.getLogger(__name__)

class ComplianceAgent:
    """
    Agent specialized in compliance analysis, checking security guidelines
    and regulatory requirements to ensure zero violations.
    """

    def __init__(self):
        self.search_tool = SearchBackend()
        self.name = "ComplianceAgent"
        self.mode = _MODE

    def run(self, query: str) -> dict:
        """
        Execute compliance evaluation for the given query.

        Args:
            query: The topic or check to analyze.

        Returns:
            A dict with 'agent', 'query', 'raw_results', and 'formatted_output'.
        """
        logger.info(f"[{self.name}] Analyzing compliance requirements for: '{query}'")

        # Enrich query with compliance and security context
        enriched_query = f"compliance requirements security checklist {query}"
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
