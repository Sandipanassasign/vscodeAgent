"""
Configuration for the Release Readiness Multi-Agent System
No API keys required — uses DuckDuckGo for search and rule-based routing.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ─── App Settings ────────────────────────────────────────────────────────────
APP_NAME = "Release Readiness Multi-Agent"
APP_VERSION = "1.0.0"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ─── Agent Settings ──────────────────────────────────────────────────────────
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "5"))
MAX_SUMMARY_LENGTH = int(os.getenv("MAX_SUMMARY_LENGTH", "500"))

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
