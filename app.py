"""Receive minimal GLPI ticket webhooks and record reviewable Jev decisions."""

import argparse
import hashlib
import json
import os
import re
from wsgiref.simple_server import make_server

from jev import evaluate, normalize
from service import InputError, decide, make_app, open_state

EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
SECRET = re.compile(r"(?i)\b(token|password|secret|api[_-]?key)\s*[:=]\s*[^\s,;]+")


def adapt(payload):
    if not isinstance(payload, dict) or payload.get("event") not in (
        "ticket.created",
        "ticket.updated",
    ):
        raise InputError("invalid_ticket_event")
    ticket = payload.get("ticket")
    if not isinstance(ticket, dict):
        raise InputError("invalid_ticket")
    ticket_id, title, description = (
        ticket.get(k) for k in ("id", "title", "description")
    )
    if (
        isinstance(ticket_id, bool)
        or not str(ticket_id).isdigit()
        or int(ticket_id) <= 0
        or not isinstance(title, str)
        or not title.strip()
        or len(title) > 500
        or not isinstance(description, str)
        or len(description) > 8000
    ):
        raise InputError("invalid_ticket")
    text = "Title: " + title + "\nDescription: " + description
    text = EMAIL.sub("[EMAIL]", text)
    text = SECRET.sub(lambda m: m.group(1) + "=[REDACTED]", text)
    digest = hashlib.sha256(text.encode()).hexdigest()
    return (
        f"ticket:{ticket_id}:{payload['event']}:{digest[:32]}",
        text,
        {"ticket_id": str(ticket_id), "event": payload["event"]},
    )


def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demo", action="store_true")
    mode.add_argument("--serve", action="store_true")
    parser.add_argument("--state", default=".local/decisions.sqlite")
    args = parser.parse_args()
    with open("examples/policy.json", encoding="utf-8") as source:
        policy = json.load(source)
    if args.demo:
        with open("examples/ticket.json", encoding="utf-8") as source:
            event = json.load(source)
        with open_state(":memory:") as db:
            print(
                json.dumps(
                    decide(
                        event,
                        adapt,
                        policy,
                        lambda _: normalize("incident", 0.97, policy),
                        db,
                    ),
                    indent=2,
                )
            )
        return
    key = os.environ["TYPESAFE_API_KEY"]
    app = make_app(
        adapt,
        policy,
        lambda text: evaluate(text, policy, key),
        args.state,
        os.environ["JEV_INGEST_TOKEN"],
    )
    with make_server("127.0.0.1", int(os.environ.get("PORT", "8097")), app) as server:
        server.serve_forever()


if __name__ == "__main__":
    main()
