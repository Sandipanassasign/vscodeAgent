"""
Local Knowledge Tool — replaces web search for VDI environments with no internet.

Strategy (in order of preference):
  1. ChromaDB vector search (semantic — best quality)
  2. SQLite full-text search (keyword — fast, zero extra deps)
  3. Plain file scan (fallback — always works)

Documents are loaded from the /knowledge_base/ folder.
Supported formats: .txt, .md, .pdf (if pdfplumber installed)
"""
import os
import re
import logging
import sqlite3
from pathlib import Path
from config import KNOWLEDGE_BASE_DIR, MAX_SEARCH_RESULTS

logger = logging.getLogger(__name__)


class LocalKnowledgeTool:
    """
    Offline knowledge retrieval tool for VDI environments with no internet access.
    Searches local documents using SQLite full-text search OR ChromaDB vector search.
    """

    def __init__(self):
        self.kb_dir = Path(KNOWLEDGE_BASE_DIR)
        self.kb_dir.mkdir(parents=True, exist_ok=True)
        self.max_results = MAX_SEARCH_RESULTS
        self.db_path = self.kb_dir / "knowledge.db"
        self._use_chroma = self._try_init_chroma()
        if not self._use_chroma:
            self._init_sqlite()

    # ─── ChromaDB Setup (Semantic Search) ────────────────────────────────────

    def _try_init_chroma(self) -> bool:
        """Try to initialise ChromaDB with local embeddings. Returns True if successful."""
        try:
            import chromadb
            from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

            self._chroma_client = chromadb.PersistentClient(
                path=str(self.kb_dir / "chroma_store")
            )
            self._embed_fn = SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
            self._collection = self._chroma_client.get_or_create_collection(
                name="release_knowledge",
                embedding_function=self._embed_fn,
            )
            logger.info("[LocalKnowledgeTool] ✅ ChromaDB (semantic search) ready.")
            self._index_documents_chroma()
            return True
        except ImportError:
            logger.info("[LocalKnowledgeTool] ChromaDB not available — falling back to SQLite.")
            return False
        except Exception as e:
            logger.warning(f"[LocalKnowledgeTool] ChromaDB init failed: {e} — using SQLite.")
            return False

    def _index_documents_chroma(self):
        """Load all knowledge base docs into ChromaDB (only new ones)."""
        docs = self._load_all_documents()
        if not docs:
            return
        existing_ids = set(self._collection.get()["ids"])
        new_docs = [(doc_id, text) for doc_id, text in docs if doc_id not in existing_ids]
        if new_docs:
            ids, texts = zip(*new_docs)
            self._collection.add(ids=list(ids), documents=list(texts))
            logger.info(f"[LocalKnowledgeTool] Indexed {len(new_docs)} new docs into ChromaDB.")

    # ─── SQLite Setup (Keyword Search) ───────────────────────────────────────

    def _init_sqlite(self):
        """Create SQLite FTS5 table and index all knowledge base documents."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS knowledge
            USING fts5(doc_id, content, filename)
        """)
        conn.commit()

        docs = self._load_all_documents()
        if docs:
            existing = {row[0] for row in cursor.execute("SELECT doc_id FROM knowledge")}
            new_docs = [(doc_id, text, doc_id.split("::")[0]) for doc_id, text in docs if doc_id not in existing]
            if new_docs:
                cursor.executemany("INSERT INTO knowledge VALUES (?, ?, ?)", new_docs)
                conn.commit()
                logger.info(f"[LocalKnowledgeTool] Indexed {len(new_docs)} docs into SQLite FTS.")
        conn.close()
        logger.info("[LocalKnowledgeTool] ✅ SQLite full-text search ready.")

    # ─── Document Loader ──────────────────────────────────────────────────────

    def _load_all_documents(self) -> list[tuple[str, str]]:
        """
        Load all .txt and .md files from knowledge_base/ folder.
        Returns list of (doc_id, content) tuples.
        """
        docs = []
        for file_path in sorted(self.kb_dir.glob("**/*")):
            if file_path.suffix in (".txt", ".md"):
                try:
                    text = file_path.read_text(encoding="utf-8").strip()
                    if text:
                        # Split large files into chunks of ~500 words
                        chunks = self._chunk_text(text, chunk_size=500)
                        for i, chunk in enumerate(chunks):
                            doc_id = f"{file_path.name}::{i}"
                            docs.append((doc_id, chunk))
                except Exception as e:
                    logger.warning(f"[LocalKnowledgeTool] Could not read {file_path}: {e}")
            elif file_path.suffix == ".pdf":
                docs.extend(self._load_pdf(file_path))
        return docs

    def _load_pdf(self, file_path: Path) -> list[tuple[str, str]]:
        """Load PDF using pdfplumber if available."""
        try:
            import pdfplumber
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join(p.extract_text() or "" for p in pdf.pages)
            chunks = self._chunk_text(text, chunk_size=500)
            return [(f"{file_path.name}::{i}", chunk) for i, chunk in enumerate(chunks)]
        except ImportError:
            logger.info(f"[LocalKnowledgeTool] pdfplumber not installed — skipping {file_path.name}")
            return []

    def _chunk_text(self, text: str, chunk_size: int = 500) -> list[str]:
        """Split text into overlapping word chunks."""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - 50):  # 50-word overlap
            chunk = " ".join(words[i: i + chunk_size])
            if chunk:
                chunks.append(chunk)
        return chunks

    # ─── Search Methods ───────────────────────────────────────────────────────

    def search(self, query: str) -> list[dict]:
        """
        Search local knowledge base. Uses ChromaDB if available, else SQLite FTS.

        Args:
            query: Natural language search query.

        Returns:
            List of result dicts with 'title', 'href', 'body' keys.
        """
        logger.info(f"[LocalKnowledgeTool] Searching locally for: '{query}'")
        if self._use_chroma:
            return self._search_chroma(query)
        return self._search_sqlite(query)

    def _search_chroma(self, query: str) -> list[dict]:
        """Semantic search via ChromaDB."""
        try:
            results = self._collection.query(
                query_texts=[query],
                n_results=min(self.max_results, self._collection.count() or 1)
            )
            docs = results.get("documents", [[]])[0]
            ids = results.get("ids", [[]])[0]
            return [
                {
                    "title": f"[KB] {doc_id.split('::')[0]}",
                    "href": f"local://knowledge_base/{doc_id.split('::')[0]}",
                    "body": doc[:500],
                }
                for doc_id, doc in zip(ids, docs)
            ]
        except Exception as e:
            logger.error(f"[LocalKnowledgeTool] ChromaDB search error: {e}")
            return []

    def _search_sqlite(self, query: str) -> list[dict]:
        """Full-text keyword search via SQLite FTS5."""
        try:
            # Sanitize query for FTS5
            safe_query = re.sub(r'[^a-zA-Z0-9 ]', ' ', query).strip()
            # Convert normal query "software deployment checklist" to "software OR deployment OR checklist"
            # so FTS5 doesn't fail if a single word is missing
            fts_query = " OR ".join(word for word in safe_query.split() if len(word) > 3)
            
            if not fts_query:
                return []

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Using rank (bm25 algorithm) built into FTS5 for better sorting
            rows = cursor.execute(
                "SELECT doc_id, content, filename FROM knowledge WHERE knowledge MATCH ? ORDER BY rank LIMIT ?",
                (fts_query, self.max_results)
            ).fetchall()
            conn.close()
            return [
                {
                    "title": f"[KB] {row[2]}",
                    "href": f"local://knowledge_base/{row[2]}",
                    "body": row[1][:500],
                }
                for row in rows
            ]
        except Exception as e:
            logger.error(f"[LocalKnowledgeTool] SQLite search error: {e}")
            return self._fallback_file_scan(query)

    def _fallback_file_scan(self, query: str) -> list[dict]:
        """Plain keyword scan — always works, even with no database."""
        results = []
        keywords = set(query.lower().split())
        for file_path in self.kb_dir.glob("**/*.{txt,md}"):
            try:
                content = file_path.read_text(encoding="utf-8")
                score = sum(1 for kw in keywords if kw in content.lower())
                if score > 0:
                    results.append({
                        "title": f"[KB] {file_path.name}",
                        "href": f"local://{file_path}",
                        "body": content[:500],
                        "_score": score,
                    })
            except Exception:
                pass
        results.sort(key=lambda x: x.get("_score", 0), reverse=True)
        return results[:self.max_results]

    def format_results(self, results: list[dict]) -> str:
        """Format search results into readable text."""
        if not results:
            return (
                "⚠️  No results found in local knowledge base.\n"
                "   → Add .txt or .md files to the 'knowledge_base/' folder."
            )
        formatted = []
        for i, r in enumerate(results, 1):
            formatted.append(
                f"[{i}] {r.get('title', 'No Title')}\n"
                f"    Source: {r.get('href', 'N/A')}\n"
                f"    {r.get('body', '')[:300]}..."
            )
        return "\n\n".join(formatted)

    def get_stats(self) -> dict:
        """Return stats about the knowledge base."""
        files = list(self.kb_dir.glob("**/*.txt")) + list(self.kb_dir.glob("**/*.md"))
        return {
            "mode": "ChromaDB (semantic)" if self._use_chroma else "SQLite (keyword)",
            "kb_directory": str(self.kb_dir),
            "document_files": len(files),
            "file_list": [f.name for f in files],
        }
