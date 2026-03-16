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
│  [5] Run preset: Bug & Incident Analysis    │
│  [6] Run preset: Code Review Guidelines     │
│  [7] Run preset: Compliance Audit           │
│  [8] Generate HTML Report (Last execution)  │
│  [q] Quit                                   │
│                                             │
│  Tip: Enter comma-separated lists (2,5,7)   │
│  or ranges (2-8) to run them in sequence.   │
└─────────────────────────────────────────────┘
"""

PRESET_QUERIES = {
    "2": "check release readiness for production deployment",
    "3": "search best practices for software testing before release",
    "4": "summarize deployment checklist and rollback strategy",
    "5": "analyze recent incidents and common bug patterns",
    "6": "review coding standards and performance guidelines",
    "7": "run compliance audit for soc2 and gdpr requirements",
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

        raw_choices = [c.strip() for c in choice.split(",") if c.strip()]
        choices = []

        # Parse potential ranges (e.g. '1-3')
        for rc in raw_choices:
            if "-" in rc:
                parts = rc.split("-")
                if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                    start, end = int(parts[0]), int(parts[1])
                    if start <= end:
                        choices.extend([str(i) for i in range(start, end + 1)])
                    else:
                        choices.extend([str(i) for i in range(start, end - 1, -1)])
                else:
                    choices.append(rc)
            else:
                choices.append(rc)

        if not choices:
            continue

        if "q" in choices:
            print("\n👋 Goodbye! Release Readiness System shutting down.\n")
            break

        for c in choices:
            if c == "1":
                query = input("\n📝 Enter your custom query: ").strip()
                if query:
                    run_query(orchestrator, query)
                else:
                    print("⚠️  Empty query. Skipping.")
            elif c == "8":
                print("\n⏳ Generating Release Readiness HTML report...")
                print(orchestrator.generate_report())
            elif c in PRESET_QUERIES:
                run_query(orchestrator, PRESET_QUERIES[c])
            else:
                print(f"⚠️  Invalid choice '{c}'. Please select 1–8 or q.")


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
