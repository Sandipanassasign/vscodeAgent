# 🚀 Release Readiness Multi-Agent System (VDI Edition)

A fully **offline, multi-agent AI system** designed to run inside restricted Virtual Desktop Infrastructure (VDI) environments without requiring any external LLM API keys (like OpenAI or Anthropic) or internet access.

This system uses **LangGraph** for agent orchestration, **DuckDuckGo** (optional) for web searches, and a **Local SQLite Knowledge Base** for offline document retrieval. 

---

## 🌟 Features

- 🏗️ **Expanded Multi-Agent Architecture**: 
  - **Orchestrator Agent**: Routes queries based on intent.
  - **Research Agent**: Gathers info from local KB or Web.
  - **Summarizer Agent**: Condenses findings using extractive NLP.
  - **Bug Analysis Agent**: Analyzes logs and incident history.
  - **Code Review Agent**: Checks code against standards.
  - **Compliance Agent**: Audits projects for GDPR/SOC2.
  - **Report Agent (NEW)**: Generates a rich, dynamic HTML readiness report with strict multi-factor scoring and an interactive Risk Indicator Dashboard.
- 📴 **100% Offline Mode (`USE_LOCAL_KB=true`)**: Reads your internal company `.txt`, `.md`, or `.pdf` files securely.
- 🌐 **Web Search Mode (`USE_LOCAL_KB=false`)**: Uses DuckDuckGo for live internet research (if permitted).
- 🧠 **No API Keys Needed**: Uses rule-based NLP and extractive summarization.
- 💬 **Interactive CLI**: Menu-driven interface allowing standalone agent execution or sequential runs (e.g., executing all agents `2-8` in one go).

---

## 🛠️ Folder Structure

```
Release Readiness MultiAgent/
├── 📂 agents/
│   ├── orchestrator.py      ← 🧠 LangGraph StateGraph router
│   ├── research_agent.py    ← 🔍 Information gatherer
│   ├── summarizer_agent.py  ← 📝 Extractive summarizer
│   └── report_agent.py      ← 📊 HTML report generator with strict bounds
├── 📂 tools/
│   ├── search_tool.py          ← DDGS web search wrapper
│   └── local_knowledge_tool.py ← SQLite/Chroma local file search (VDI mode)
├── 📂 knowledge_base/       ← 📁 Drop your docs here!
│   ├── incident_history.md  
│   ├── coding_standards.md  
│   └── compliance_reqs.md   
├── 📂 reports/              ← 📄 Generated HTML Reports go here
├── main.py                  ← 🚀 Main entry with expanded multi-run menu
├── config.py                ← ⚙️ Core settings & Intent Keywords
├── .env                     ← 🎛️ Toggle Offline vs Online mode
└── requirements.txt         ← 📦 Python dependencies
```

---

## ⚙️ 1. Setup Instructions (Do this once)

### Step 1: Create a Virtual Environment
Open your Terminal and run:
```bash
python -m venv .venv
```

### Step 2: Activate the Virtual Environment
```bash
# Mac/Linux
source .venv/bin/activate

# Windows / VDI
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🎛️ 2. Configuration (VDI Mode)

Since you are running in a restricted VDI environment, ensure your `.env` file is set to use the local Knowledge Base.

Open the `.env` file and set:
```env
# Set to true to use your local files in /knowledge_base/ (VDI Mode)
# Set to false to use DuckDuckGo Web Search
USE_LOCAL_KB=true
```

### 🗂️ Adding Internal Documents
1. Open the `knowledge_base/` folder.
2. Drop any company-specific guidelines, checklists, or runbooks into this folder as `.md` or `.txt` files.
3. The agents will automatically index and search them the next time you run `main.py`!

---

## 🚀 3. How to Run the Agents

Make sure your virtual environment is activated (`source .venv/bin/activate`).

### Interactive Menu (Recommended)
Simply run the main script to open the interactive chat menu:
```bash
python main.py
```

**Executing Sequences (NEW)**:
You can now pass comma-separated strings (e.g., `2,5,7`) or ranges (e.g., `2-8`) to run multiple agents sequentially without interruption. 
- Use option `8` to automatically generate the strict-bound Readiness HTML report wrapping all findings from the recent run.

---

## 📊 4. Strict Readiness HTML Reports

The newly integrated **Report Agent** generates a final standalone HTML status report stored in the `reports/` folder.
- **Strict Bounding**: Multi-Factor readiness scores now utilize extremely rigid logic. 100% test passing ratios and 0.0 defect densities are required to receive a Go decision.
- **Risk Indicators**: Displays categories mapped to specific executed intents (Compliance, Bug Analysis, etc.)
- **Actionable Summaries**: Condenses findings from the non-LLM pipelines into readable, executive-scoped bullet points grouped by intent.

---

*Maintained by the Release Readiness Team | Built in VS Code*
