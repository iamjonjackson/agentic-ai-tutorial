# steps/00-setup.md — Repo scaffold

## Goal
A codespace that boots with everything the core tutorial needs installed.

## Do
1. Create `.devcontainer/devcontainer.json`:

```json
{
  "name": "agentic-tutorial",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "features": {
    "ghcr.io/devcontainers/features/common-utils:2": {}
  },
  "postCreateCommand": "pip install openai presidio-analyzer presidio-anonymizer pypdf chromadb"
}
```

2. Create `.gitignore` containing: `.rag/`, `token.json`, `credentials.json`, `.env`, `__pycache__/`.
3. Put `AGENTS.md` (repo conventions) in the repo root.
4. Create `requirements.txt` listing the same packages as postCreateCommand.

## Test
`python -c "import openai, presidio_analyzer, pypdf, chromadb; print('deps ok')"`
