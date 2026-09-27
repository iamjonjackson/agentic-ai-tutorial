import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

_SERVICE = {}


def gmail_service():
    if "service" in _SERVICE:
        return _SERVICE["service"]
    token_path = "token.json"
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())
    service = build("gmail", "v1", credentials=creds)
    _SERVICE["service"] = service
    return service


def search_mail(query, max_results=10):
    service = gmail_service()
    result = service.users().messages().list(
        userId="me", q=query, maxResults=max_results
    ).execute()
    ids = [m["id"] for m in result.get("messages", [])]
    if not ids:
        return f"(no messages matching '{query}')"
    lines = []
    for mid in ids:
        msg = service.users().messages().get(
            userId="me", id=mid, format="metadata"
        ).execute()
        headers = {
            h["name"]: h["value"] for h in msg["payload"]["headers"]
        }
        lines.append(
            f"{mid} | {headers.get('From', '?')} | {headers.get('Subject', '?')}"
        )
    return "\n".join(lines)


def read_mail(id):
    service = gmail_service()
    msg = service.users().messages().get(userId="me", id=id, format="full").execute()
    import base64

    body = ""
    parts = msg["payload"].get("parts", [msg["payload"]])
    for part in parts:
        data = part.get("body", {}).get("data")
        if data:
            body += base64.urlsafe_b64decode(data).decode(errors="replace")
    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    return f"From: {headers.get('From', '?')}\nSubject: {headers.get('Subject', '?')}\n\n{body}"


def send_mail(to, subject, body):
    import base64
    from email.message import EmailMessage

    message = EmailMessage()
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    service = gmail_service()
    service.users().messages().send(
        userId="me", body={"raw": raw}
    ).execute()
    return f"sent mail to {to}"


GMAIL_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_mail",
            "description": "Search the user's Gmail inbox with a Gmail search query. Returns id | From | Subject lines.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Gmail search query, e.g. 'from:alice@example.com'."},
                    "max_results": {"type": "integer", "description": "Maximum messages to return. Default 10."},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_mail",
            "description": "Read a single Gmail message by its id (from search_mail results).",
            "parameters": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "description": "Message id from search_mail."},
                },
                "required": ["id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_mail",
            "description": "Send an email. Requires explicit user approval.",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address."},
                    "subject": {"type": "string"},
                    "body": {"type": "string"},
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
]

GMAIL_TOOL_IMPLS = {
    "search_mail": search_mail,
    "read_mail": read_mail,
    "send_mail": send_mail,
}
