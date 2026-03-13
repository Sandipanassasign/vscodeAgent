"""
Summarizer Agent — condenses research results into concise summaries.
Uses rule-based NLP (no LLM API key needed).
"""
import logging
import re
from config import MAX_SUMMARY_LENGTH

logger = logging.getLogger(__name__)


class SummarizerAgent:
    """
    Summarizes and condenses research output into actionable insights.
    Works without any external LLM API — uses extractive summarization.
    """

    def __init__(self):
        self.name = "SummarizerAgent"
        self.max_length = MAX_SUMMARY_LENGTH

    def run(self, research_output: dict) -> dict:
        """
        Summarize the output from ResearchAgent.

        Args:
            research_output: Dict returned by ResearchAgent.run()

        Returns:
            A dict with 'agent', 'summary', and 'key_points'.
        """
        logger.info(f"[{self.name}] Summarizing research results...")

        raw_results = research_output.get("raw_results", [])
        query = research_output.get("query", "")

        summary = self._extractive_summary(raw_results)
        key_points = self._extract_key_points(raw_results)

        return {
            "agent": self.name,
            "original_query": query,
            "summary": summary,
            "key_points": key_points,
            "sources": [r.get("href", "") for r in raw_results if r.get("href")],
        }

    def _extractive_summary(self, results: list[dict]) -> str:
        """Extract and combine the most relevant sentences from results."""
        if not results:
            return "No content available to summarize."

        # Collect all body text
        all_text = " ".join(
            r.get("body", "") for r in results if r.get("body")
        )

        # Split into sentences and pick top ones by length (proxy for info density)
        sentences = re.split(r'(?<=[.!?])\s+', all_text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 40]

        # Pick top sentences up to max_length characters
        summary_parts = []
        total_len = 0
        for sentence in sentences[:10]:
            if total_len + len(sentence) <= self.max_length:
                summary_parts.append(sentence)
                total_len += len(sentence)
            else:
                break

        return " ".join(summary_parts) if summary_parts else all_text[:self.max_length]

    def _extract_key_points(self, results: list[dict]) -> list[str]:
        """Extract key bullet points from search result titles."""
        key_points = []
        for r in results:
            title = r.get("title", "").strip()
            if title and len(title) > 10:
                key_points.append(f"• {title}")
        return key_points[:5]  # Return top 5 key points

    def summarize_text(self, text: str, label: str = "Input") -> dict:
        """
        Directly summarize any raw text (helper method).

        Args:
            text: Raw text to summarize.
            label: Label for the content being summarized.

        Returns:
            Summary dict.
        """
        logger.info(f"[{self.name}] Summarizing raw text: '{label}'")
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 40]
        summary = " ".join(sentences[:5])
        return {
            "agent": self.name,
            "label": label,
            "summary": summary[:self.max_length],
            "key_points": [f"• {s[:100]}" for s in sentences[:5]],
            "sources": [],
        }
