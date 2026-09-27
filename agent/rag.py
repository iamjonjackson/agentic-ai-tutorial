import json
import os
import sys

import chromadb
from openai import OpenAI
from pypdf import PdfReader

client = OpenAI(
    api_key=os.environ["MISTRAL_API_KEY"],
    base_url="https://api.mistral.ai/v1",
)

EMBED_MODEL = "mistral-embed"

chroma = chromadb.PersistentClient(path=".rag")
col = chroma.get_or_create_collection("docs")


def _embed(texts):
    reply = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in reply.data]


def _chunk(text, chunk_size=1000, delimiter="\n\n"):
    chunks = []
    start = 0
    while start < len(text):
        window = text[start : start + chunk_size]
        cut = window.rfind(delimiter)
        if cut > 0 and cut < len(window):
            end = start + cut + len(delimiter)
        else:
            end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end
    return chunks


def ingest(pdf_path, chunk_size=1000, delimiter="\n\n"):
    reader = PdfReader(pdf_path)
    text = "\n\n".join(page.extract_text() or "" for page in reader.pages)
    chunks = _chunk(text, chunk_size, delimiter)
    embeddings = _embed(chunks)
    ids = [f"{pdf_path}-{i}" for i in range(len(chunks))]
    col.add(documents=chunks, embeddings=embeddings, ids=ids)
    return f"ingested {len(chunks)} chunks from {pdf_path}"


def search(query, k=3):
    query_embedding = _embed([query])[0]
    result = col.query(query_embeddings=[query_embedding], n_results=k)
    docs = result["documents"][0]
    if not docs:
        return "(no documents ingested)"
    return "\n---\n".join(docs)


def search_docs(query):
    return search(query)


RAG_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": "Search the ingested PDF documents for relevant passages.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "What to look for in the documents.",
                    },
                },
                "required": ["query"],
            },
        },
    },
]

RAG_TOOL_IMPLS = {
    "search_docs": search_docs,
}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python -m agent.rag <pdf> [chunk_size]")
        sys.exit(1)
    pdf = sys.argv[1]
    size = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    print(ingest(pdf, chunk_size=size))
