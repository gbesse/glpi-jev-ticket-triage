import json
from pathlib import Path
import unittest

from app import adapt
from service import InputError


class AdapterTests(unittest.TestCase):
    def test_redacts_common_secrets_and_email(self):
        event = json.loads(Path("examples/ticket.json").read_text())
        event["ticket"]["description"] = (
            "Contact alice@example.org; token=abc123 and password: hidden"
        )
        _, text, metadata = adapt(event)
        self.assertNotIn("alice@example.org", text)
        self.assertNotIn("abc123", text)
        self.assertNotIn("hidden", text)
        self.assertEqual(metadata["ticket_id"], "42")

    def test_ticket_edit_generates_new_decision_id(self):
        event = json.loads(Path("examples/ticket.json").read_text())
        first = adapt(event)[0]
        event["ticket"]["description"] += " A new failure appeared."
        self.assertNotEqual(first, adapt(event)[0])

    def test_malformed_ticket_is_rejected(self):
        with self.assertRaises(InputError):
            adapt(
                {
                    "event": "ticket.created",
                    "ticket": {"id": 0, "title": "x", "description": "y"},
                }
            )
