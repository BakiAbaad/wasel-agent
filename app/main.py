import os
import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from dotenv import load_dotenv
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

META_FILE = DATA_DIR / "metadata.json"
INDEX_FILE = DATA_DIR / "faiss_index.bin"

embedder = SentenceTransformer("all-MiniLM-L6-v2")
metadata = []
index = None

app = FastAPI(title="Wasel Agent (PoC)")
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")


class IndexRequest(BaseModel):
    path: str


class QueryRequest(BaseModel):
    query: str
    k: int = 5


def chunk_text(text: str, chunk_size: int = 1200, overlap: int = 250):
    chunks = []
    start = 0
    L = len(text)
    while start < L:
        end = min(start + chunk_size, L)
        chunks.append(text[start:end])
        start = end - overlap
        if start < 0:
            start = 0
    return chunks


def save_metadata():
    with open(META_FILE, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def save_index(idx):
    faiss.write_index(idx, str(INDEX_FILE))


def load_metadata():
    global metadata
    if META_FILE.exists():
        with open(META_FILE, "r", encoding="utf-8") as f:
            metadata = json.load(f)
    else:
        metadata = []


def load_index():
    global index
    if INDEX_FILE.exists():
        index = faiss.read_index(str(INDEX_FILE))
    else:
        index = None


@app.on_event("startup")
def startup():
    load_metadata()
    load_index()


@app.post("/api/index")
def do_index(req: IndexRequest):
    p = Path(req.path).expanduser()
    if not p.exists():
        return {"error": "path not found", "path": str(p)}

    supported = {".py", ".md", ".txt", ".json", ".js", ".ts", ".yaml", ".yml", ".java", ".go", ".rs", ".cs", ".html"}
    new_items = []

    for fp in p.rglob("*"):
        if fp.is_file() and fp.suffix.lower() in supported:
            try:
                text = fp.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            for chunk in chunk_text(text):
                new_items.append({"path": str(fp), "text": chunk})

    if not new_items:
        return {"error": "no supported files found"}

    metadata.extend(new_items)
    texts = [m["text"] for m in metadata]
    vectors = embedder.encode(texts, convert_to_numpy=True, show_progress_bar=False).astype("float32")

    idx = faiss.IndexFlatL2(vectors.shape[1])
    idx.add(vectors)
    save_index(idx)
    save_metadata()
    load_index()

    return {"status": "ok", "documents_indexed": len(metadata)}


@app.post("/api/search")
def search(req: QueryRequest):
    if index is None:
        return {"error": "index not built yet"}

    qvec = embedder.encode([req.query], convert_to_numpy=True).astype("float32")
    D, I = index.search(qvec, req.k)

    results = []
    for dist, idx_pos in zip(D[0], I[0]):
        if idx_pos < 0 or idx_pos >= len(metadata):
            continue
        results.append({
            "path": metadata[idx_pos]["path"],
            "text": metadata[idx_pos]["text"],
            "score": float(dist)
        })

    return {"query": req.query, "results": results}


@app.post("/api/chat")
def chat(req: QueryRequest):
    resp = search(req)
    results = resp.get("results", [])
    snippets = "\n\n---\n\n".join(r["text"] for r in results)

    if OPENAI_API_KEY:
        try:
            completion = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "أنت مساعد برمجي عربي. استخدم السياق التالي من الكود والملفات لإعطاء إجابة دقيقة."},
                    {"role": "user", "content": f"السؤال: {req.query}\n\nالسياق:\n{snippets}"}
                ],
                max_tokens=700
            )
            answer = completion["choices"][0]["message"]["content"]
        except Exception as e:
            answer = f"OpenAI error: {e}\n\nFallback from retrieved context:\n{snippets[:4000]}"
    else:
        answer = "لم يتم توفير مفتاح OpenAI. هذا هو السياق المسترجع من المشروع:\n\n" + snippets[:4000]

    return {"query": req.query, "answer": answer, "snippets": results}
