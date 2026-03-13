"""
main.py — Entry point for the Release Readiness Multi-Agent System

Usage:
    python main.py                    → Interactive mode (menu-driven)
    python main.py "your query here" → Single query mode

Examples:
    python main.py "check release readiness for deployment"
    python main.py "search best practices for testing before release"
    python main.py "summarize security checklist for go-live"
"""
import sys
import logging
from agents.orchestrator import Orchestrator

# ─── Logging Setup ────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)

BANNER = """
╔══════════════════════════════════════════════════════════╗
║     🚀  Release Readiness Multi-Agent System  v1.0       ║
║     Powered by: LangGraph + DuckDuckGo (No API Key)      ║
╚══════════════════════════════════════════════════════════╝

Available Agents:
  🔍 Research Agent     → Searches the web for information
  📝 Summarizer Agent   → Condenses results into key points
  🔄 Orchestrator       → Routes your query to the right agent

Sample Queries:
  → "check release readiness checklist"
  → "search best practices for deployment"
  → "summarize testing strategy before go-live"
  → "find security checks for production release"
"""

MENU = """
┌─────────────────────────────────────────────┐
│  Choose an option:                          │
│  [1] Ask a custom query                     │
│  [2] Run preset: Release Readiness Check    │
│  [3] Run preset: Search Testing Practices   │
│  [4] Run preset: Summarize Deployment Tips  │
│  [q] Quit                                   │
└─────────────────────────────────────────────┘
"""

PRESET_QUERIES = {
    "2": "check release readiness for production deployment",
    "3": "search best practices for software testing before release",
    "4": "summarize deployment checklist and rollback strategy",
}


def run_query(orchestrator: Orchestrator, query: str):
    """Run a single query through the orchestrator and print results."""
    print(f"\n⏳ Processing: '{query}' ...\n")
    result = orchestrator.run(query)

    if result.get("error"):
        print(f"❌ Error: {result['error']}")
    else:
        print(result.get("final_result", "No result generated."))


def interactive_mode(orchestrator: Orchestrator):
    """Run the agent system in interactive menu mode."""
    print(BANNER)

    while True:
        print(MENU)
        choice = input("Your choice: ").strip().lower()

        if choice == "q":
            print("\n👋 Goodbye! Release Readiness System shutting down.\n")
            break
        elif choice == "1":
            query = input("\n📝 Enter your query: ").strip()
            if query:
                run_query(orchestrator, query)
            else:
                print("⚠️  Empty query. Please try again.")
        elif choice in PRESET_QUERIES:
            run_query(orchestrator, PRESET_QUERIES[choice])
        else:
            print("⚠️  Invalid choice. Please select 1–4 or q.")


def main():
    orchestrator = Orchestrator()

    # Single query mode: python main.py "your query"
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(BANNER)
        run_query(orchestrator, query)
    else:
        # Interactive mode
        interactive_mode(orchestrator)


if __name__ == "__main__":
    main()
