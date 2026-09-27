import base64
import unittest
from unittest.mock import MagicMock, patch

from agent import tools_gmail


class FakeMsg:
    def __init__(self, mid, frm, subj, body="hello"):
        self._d = {
            "id": mid,
            "payload": {
                "headers": [
                    {"name": "From", "value": frm},
                    {"name": "Subject", "value": subj},
                ],
                "parts": [
                    {"body": {"data": base64.urlsafe_b64encode(body.encode()).decode()}}
                ],
            }
        }

    def execute(self):
        return self._d


def make_service():
    svc = MagicMock()
    svc.users.return_value.messages.return_value.list.return_value = MagicMock(
        **{"execute.return_value": {"messages": [{"id": "abc123"}]}}
    )
    svc.users.return_value.messages.return_value.get.return_value = FakeMsg(
        "abc123", "alice@example.com", "Hello there", "body text"
    )
    svc.users.return_value.messages.return_value.send.return_value.execute.return_value = {}
    return svc


class GmailMockTests(unittest.TestCase):
    def test_search_mail(self):
        with patch.object(tools_gmail, "gmail_service", return_value=make_service()):
            out = tools_gmail.search_mail("from:alice")
        self.assertIn("abc123", out)
        self.assertIn("alice@example.com", out)
        self.assertIn("Hello there", out)

    def test_read_mail(self):
        with patch.object(tools_gmail, "gmail_service", return_value=make_service()):
            out = tools_gmail.read_mail("abc123")
        self.assertIn("alice@example.com", out)
        self.assertIn("body text", out)

    def test_send_mail(self):
        with patch.object(tools_gmail, "gmail_service", return_value=make_service()):
            out = tools_gmail.send_mail("bob@example.com", "hi", "body")
        self.assertIn("sent mail to bob@example.com", out)

    def test_registration(self):
        self.assertIn("send_mail", tools_gmail.GMAIL_TOOL_IMPLS)
        names = [t["function"]["name"] for t in tools_gmail.GMAIL_TOOLS]
        self.assertEqual(names, ["search_mail", "read_mail", "send_mail"])


if __name__ == "__main__":
    unittest.main()
