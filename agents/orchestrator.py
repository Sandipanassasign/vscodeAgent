"""
Orchestrator Agent — the brain of the multi-agent system.
Uses LangGraph StateGraph to route queries to the right sub-agent.

Flow:
  User Query
      │
      ▼
  [route_intent]  ← decides: research / summarize / release_check
      │
      ├──► [research_node]   → ResearchAgent
      │         │
      │         ▼
      │    [summarize_node]  → SummarizerAgent
      │
      └──► [summarize_node]  → SummarizerAgent (direct)
"""
import logging
from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END

from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from config import RESEARCH_KEYWORDS, SUMMARIZE_KEYWORDS, RELEASE_KEYWORDS, RELEASE_DOMAINS

logger = logging.getLogger(__name__)


# ─── State Definition ─────────────────────────────────────────────────────────
class AgentState(TypedDict):
    query: str                    # Original user query
    intent: str                   # Detected intent: research / summarize / release_check
    research_output: dict         # Output from ResearchAgent
    summary_output: dict          # Output from SummarizerAgent
    final_result: str             # Final formatted result for the user
    error: str                    # Error message, if any


# ─── Orchestrator Class ───────────────────────────────────────────────────────
class Orchestrator:
    """
    LangGraph-based orchestrator that routes user queries
    to specialized sub-agents (Research, Summarizer).
    """

    def __init__(self):
        self.research_agent = ResearchAgent()
        self.summarizer_agent = SummarizerAgent()
        self.graph = self._build_graph()
        self.name = "Orchestrator"

    # ── Node Functions ──────────────────────────────────────────────────────

    def route_intent(self, state: AgentState) -> AgentState:
        """Detect the user's intent from the query keywords."""
        query = state["query"].lower()
        logger.info(f"[{self.name}] Routing intent for: '{query}'")

        if any(kw in query for kw in RELEASE_KEYWORDS):
            intent = "release_check"
        elif any(kw in query for kw in RESEARCH_KEYWORDS):
            intent = "research"
        elif any(kw in query for kw in SUMMARIZE_KEYWORDS):
            intent = "summarize"
        else:
            intent = "research"  # Default to research

        logger.info(f"[{self.name}] Detected intent: '{intent}'")
        return {**state, "intent": intent}

    def research_node(self, state: AgentState) -> AgentState:
        """Run the ResearchAgent."""
        logger.info(f"[{self.name}] Invoking ResearchAgent...")
        try:
            result = self.research_agent.run(state["query"])
            return {**state, "research_output": result}
        except Exception as e:
            logger.error(f"[{self.name}] ResearchAgent error: {e}")
            return {**state, "error": str(e), "research_output": {}}

    def release_check_node(self, state: AgentState) -> AgentState:
        """Run release readiness checks across all domains."""
        logger.info(f"[{self.name}] Running Release Readiness Check...")
        try:
            combined_results = []
            for domain in RELEASE_DOMAINS[:3]:  # Check top 3 domains
                result = self.research_agent.get_release_checklist_info(domain)
                combined_results.extend(result.get("raw_results", []))

            merged_output = {
                "agent": "ResearchAgent",
                "query": state["query"],
                "raw_results": combined_results,
                "formatted_output": f"Checked domains: {', '.join(RELEASE_DOMAINS[:3])}",
                "result_count": len(combined_results),
            }
            return {**state, "research_output": merged_output}
        except Exception as e:
            logger.error(f"[{self.name}] Release check error: {e}")
            return {**state, "error": str(e), "research_output": {}}

    def summarize_node(self, state: AgentState) -> AgentState:
        """Run the SummarizerAgent on previous research output."""
        logger.info(f"[{self.name}] Invoking SummarizerAgent...")
        try:
            research_out = state.get("research_output", {})
            if research_out:
                summary = self.summarizer_agent.run(research_out)
            else:
                summary = self.summarizer_agent.summarize_text(
                    state["query"], label="Direct Query"
                )

            # Format the final output
            final = self._format_final_output(state["query"], summary)
            return {**state, "summary_output": summary, "final_result": final}
        except Exception as e:
            logger.error(f"[{self.name}] SummarizerAgent error: {e}")
            return {**state, "error": str(e), "final_result": f"Error: {e}"}

    # ── Conditional Edge ────────────────────────────────────────────────────

    def decide_next(self, state: AgentState) -> Literal["research", "release_check", "summarize"]:
        """Route to the appropriate node based on intent."""
        intent = state.get("intent", "research")
        if intent == "release_check":
            return "release_check"
        elif intent == "summarize":
            return "summarize"
        return "research"

    # ── Graph Builder ────────────────────────────────────────────────────────

    def _build_graph(self) -> any:
        """Build and compile the LangGraph state machine."""
        graph = StateGraph(AgentState)

        # Add nodes
        graph.add_node("route_intent", self.route_intent)
        graph.add_node("research", self.research_node)
        graph.add_node("release_check", self.release_check_node)
        graph.add_node("summarize", self.summarize_node)

        # Set entry point
        graph.set_entry_point("route_intent")

        # Add conditional routing after intent detection
        graph.add_conditional_edges(
            "route_intent",
            self.decide_next,
            {
                "research": "research",
                "release_check": "release_check",
                "summarize": "summarize",
            }
        )

        # After research/release_check → always summarize
        graph.add_edge("research", "summarize")
        graph.add_edge("release_check", "summarize")
        graph.add_edge("summarize", END)

        return graph.compile()

    # ── Public Run Method ─────────────────────────────────────────────────────

    def run(self, query: str) -> dict:
        """
        Run the full multi-agent pipeline for a given user query.

        Args:
            query: The user's input question or task.

        Returns:
            Final state dict with result and all intermediate outputs.
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"[{self.name}] Starting pipeline for: '{query}'")
        logger.info(f"{'='*60}")

        initial_state: AgentState = {
            "query": query,
            "intent": "",
            "research_output": {},
            "summary_output": {},
            "final_result": "",
            "error": "",
        }

        final_state = self.graph.invoke(initial_state)
        logger.info(f"[{self.name}] Pipeline complete.")
        return final_state

    # ── Formatting ─────────────────────────────────────────────────────────────

    def _format_final_output(self, query: str, summary: dict) -> str:
        """Format the final result for display."""
        lines = [
            f"\n{'='*60}",
            f"  🤖 MULTI-AGENT RESULT",
            f"{'='*60}",
            f"  📌 Query   : {query}",
            f"  🎯 Intent  : Research → Summarize",
            f"{'─'*60}",
            f"  📋 SUMMARY:",
            f"  {summary.get('summary', 'No summary available.')}",
            f"{'─'*60}",
            f"  🔑 KEY POINTS:",
        ]
        for point in summary.get("key_points", []):
            lines.append(f"  {point}")
        lines.append(f"{'─'*60}")
        sources = summary.get("sources", [])
        if sources:
            lines.append("  🔗 SOURCES:")
            for src in sources[:3]:
                lines.append(f"  • {src}")
        lines.append(f"{'='*60}\n")
        return "\n".join(lines)
