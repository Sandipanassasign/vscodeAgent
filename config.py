"""
Configuration for the Release Readiness Multi-Agent System
Supports two modes:
  - ONLINE  : Uses DuckDuckGo web search (requires internet)
  - OFFLINE : Uses local knowledge base files (VDI-friendly, no internet)
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── App Settings ────────────────────────────────────────────────────────────
APP_NAME = "Release Readiness Multi-Agent"
APP_VERSION = "1.0.0"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ─── Mode Selection ─────────────────────────────────────────────────────────
# Set USE_LOCAL_KB=true in .env to switch to offline/local knowledge base mode
# Set USE_LOCAL_KB=false (or leave unset) to use DuckDuckGo web search
USE_LOCAL_KB = os.getenv("USE_LOCAL_KB", "false").lower() == "true"

# ─── Agent Settings ──────────────────────────────────────────────────────────
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
MAX_SUMMARY_LENGTH = int(os.getenv("MAX_SUMMARY_LENGTH", "500"))

# ─── Local Knowledge Base ─────────────────────────────────────────────────────
# Path to the folder containing your local .txt and .md knowledge documents
KNOWLEDGE_BASE_DIR = os.getenv(
    "KNOWLEDGE_BASE_DIR",
    str(Path(__file__).parent / "knowledge_base")
)

# ─── Release Readiness Domains ───────────────────────────────────────────────
RELEASE_DOMAINS = [
    "testing",
    "deployment",
    "security",
    "performance",
    "documentation",
    "rollback",
    "monitoring",
    "approval",
    "compliance",
    "incident",
    "standard",
]

# ─── Intent Keywords for Routing ─────────────────────────────────────────────
RESEARCH_KEYWORDS = [
    "search", "find", "look up", "research", "what is",
    "how to", "best practices", "check", "investigate", "explore"
]

SUMMARIZE_KEYWORDS = [
    "summarize", "summary", "brief", "overview", "tldr",
    "condense", "digest", "wrap up", "highlights"
]

RELEASE_KEYWORDS = [
    "release", "deploy", "readiness", "checklist", "go-live",
    "production", "launch", "ship", "publish", "rollout"
]

BUG_KEYWORDS = [
    "bug", "error", "issue", "incident", "crash", "failure", 
    "broken", "fix", "resolution", "root cause"
]

REVIEW_KEYWORDS = [
    "review", "code", "standards", "best practices", "guidelines",
    "refactor", "lint", "naming", "quality"
]

COMPLIANCE_KEYWORDS = [
    "compliance", "audit", "legal", "gdpr", "soc2", "policy",
    "requirement", "license", "regulation"
]
