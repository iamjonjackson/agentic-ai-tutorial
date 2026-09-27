# steps/70-stage6-rag.md — Stage 6

## Goal
RAG in its smallest working form: ingest a PDF (chunk by size/delimiter), embed, store in ChromaDB, and expose retrieval to the agent as just another tool.

## Do
1. Create `agent/rag.py`:
   - ChromaDB `PersistentClient(path=".rag")`, collection "docs".
   - `ingest(pdf_path, chunk_size=1000, delimiter="\n\n")`: extract text with pypdf, chunk by walking forward in chunk_size windows but preferring the last delimiter occurrence inside each window, embed all chunks with `mistral-embed` via the same OpenAI-compatible client, store with ids `f"{pdf_path}-{i}"`.
   - `search(query, k=3)`: embed the query (same model — mismatched embedding models give garbage), `col.query`, join the top-k documents with `"\n---\n"`.
2. Register one tool `search_docs(query)` in TOOLS/TOOL_IMPLS with a description like "Search the ingested PDF documents for relevant passages."
3. Add a tiny CLI entry (`python -m agent.rag path/to/file.pdf`) or an `ingest_pdf` path so a PDF can be indexed without editing code.

## Production parallels
Retrieval as a tool the model chooses to call — identical to how production agents answer document questions without stuffing files into context. Real simplifications: no chunk overlap, no metadata filters, no hybrid keyword+vector search, no re-ranking, no provenance.

## Test
Drag any PDF into the codespace, ingest it, then ask the agent "what does the paper say about X?" — it must call search_docs and answer from retrieved chunks, not from memory. Then vary chunk_size (100 / 500 / 2000) and note retrieval quality differences; ask a question whose answer spans a chunk boundary and watch it fail (this motivates overlap windows).
