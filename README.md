# 🚀 Release Readiness Multi-Agent System (VDI Edition)

A fully **offline, multi-agent AI system** designed to run inside restricted Virtual Desktop Infrastructure (VDI) environments without requiring any external LLM API keys (like OpenAI or Anthropic) or internet access.

This system uses **LangGraph** for agent orchestration, **DuckDuckGo** (optional) for web searches, and a **Local SQLite Knowledge Base** for offline document retrieval. 

---

## 🌟 Features

- 🏗️ **Multi-Agent Architecture**: Orchestrator Agent, Research Agent, and Summarizer Agent.
- 📴 **100% Offline Mode (`USE_LOCAL_KB=true`)**: Reads your internal company `.txt`, `.md`, or `.pdf` files securely.
- 🌐 **Web Search Mode (`USE_LOCAL_KB=false`)**: Uses DuckDuckGo for live internet research (if permitted).
- 🧠 **No API Keys Needed**: Uses rule-based NLP and extractive summarization.
- 💬 **Interactive CLI**: Menu-driven interface for easy querying.

---

## 🛠️ Folder Structure

```
Release Readiness MultiAgent/
├── 📂 agents/
│   ├── orchestrator.py      ← 🧠 LangGraph StateGraph router
│   ├── research_agent.py    ← 🔍 Information gatherer
│   └── summarizer_agent.py  ← 📝 Extractive summarizer
├── 📂 tools/
│   ├── search_tool.py          ← DDGS web search wrapper
│   └── local_knowledge_tool.py ← SQLite/Chroma local file search (VDI mode)
├── 📂 knowledge_base/       ← 📁 Drop your internal PDFs, TXTs, MDs here!
├── main.py                  ← 🚀 The main entry point to run the app
├── config.py                ← ⚙️ Core settings & routing keywords
├── .env                     ← 🎛️ Toggle Offline vs Online mode
└── requirements.txt         ← 📦 Python dependencies
```

---

## ⚙️ 1. Setup Instructions (Do this once)

### Step 1: Create a Virtual Environment
Open your VS Code Terminal (`Ctrl + ~`) and run:
```bash
# Mac/Linux
python -m venv .venv

# Windows / VDI
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

## 🎛️ 2. Configuration (Online vs Offline Mode)

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

### Mode A: Interactive Menu (Recommended)
Simply run the main script to open the interactive chat menu:
```bash
python main.py
```
**Output:**
```
┌─────────────────────────────────────────────┐
│  Choose an option:                          │
│  [1] Ask a custom query                     │
│  [2] Run preset: Release Readiness Check    │
│  [3] Run preset: Search Testing Practices   │
│  [4] Run preset: Summarize Deployment Tips  │
│  [q] Quit                                   │
└─────────────────────────────────────────────┘
Your choice: 
```

### Mode B: Single Query (Command Line)
You can directly pass your question to the agent in the terminal:
```bash
python main.py "summarize the security checklist for production"
```
```bash
python main.py "find testing best practices before deployment"
```

---

## 🧠 How the Agents Think

When you run a query like *"summarize security readiness"*:
1. **Orchestrator Agent**: Analyzes your query and detects the "intent" (e.g., `release_check`, `summarize`, `research`).
2. **Research Agent**: 
   - If `USE_LOCAL_KB=true`, it searches your `knowledge_base/` folder instantly using SQLite.
   - If `USE_LOCAL_KB=false`, it searches the internet via DuckDuckGo.
3. **Summarizer Agent**: Condenses the extracted text into a readable summary using Extractive NLP.
4. **Final Output**: The result is formatted with bullet points, summaries, and exact file/URL citations. 

---

*Maintained by the Release Readiness Team | Built in VS Code*
