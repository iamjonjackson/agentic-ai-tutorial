# steps/sq1-gmail.md — Side quest 1: Gmail connector

## Goal
Gmail as three agent tools (search, read, send) with send gated behind the ASK policy — the MCP pattern in miniature.

## Do
1. Google Cloud Console: create project, enable Gmail API, create OAuth desktop credential, download `credentials.json` into the repo root (gitignored).
2. Add google-api-python-client google-auth-httplib2 google-auth-oauthlib to requirements/devcontainer.
3. One-time `InstalledAppFlow` exchange to produce `token.json` (codespace port forwarding handles the localhost redirect).
4. Create `agent/tools_gmail.py`: `gmail_service()` from token.json; `search_mail(query, max_results=10)` returning `id | From | Subject` lines; `read_mail(id)`; `send_mail(to, subject, body)`. Register in TOOLS/TOOL_IMPLS; add `send_mail` to the ASK policy set.

## Production parallels
Real MCP connectors run as separate processes with a discovery handshake; security-conscious setups sandbox the connector and scope OAuth narrowly. Treat email content as untrusted input (injection risk) — and note Presidio from Stage 5 matters double here: email is the highest-PII source the agent touches.

## Test
Ask "search my inbox for anything from X" (should list results), then "draft a reply" — sending must trigger the y/N prompt. Never commit token.json or credentials.json.
