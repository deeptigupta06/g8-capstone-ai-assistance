import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

tickets = [
    {
        "id": "INC-1001",
        "title": "Unable to access Finance application",
        "description": "User receives an authentication error after changing their password.",
        "category": "authentication",
        "resolution": "The account session was synchronised and the user signed out from all active sessions before logging in again.",
        "resolved_date": "2025-06-15"
    },
    {
        "id": "INC-1002",
        "title": "VPN authentication failure",
        "description": "User cannot connect to VPN after a password reset.",
        "category": "authentication",
        "resolution": "The user re-authenticated using the updated password and the VPN profile was refreshed.",
        "resolved_date": "2025-03-20"
    },
    {
        "id": "INC-1003",
        "title": "Application configuration error",
        "description": "Application opens but displays an invalid configuration message.",
        "category": "configuration",
        "resolution": "The local configuration file was recreated using the approved configuration template.",
        "resolved_date": "2025-01-10"
    },
    {
        "id": "INC-1004",
        "title": "Access request not completed",
        "description": "A new employee cannot access the reporting application.",
        "category": "software-access",
        "resolution": "The manager approval was confirmed and the user was added to the approved access group.",
        "resolved_date": "2024-11-05"
    },
    {
        "id": "INC-1005",
        "title": "Authentication error after browser change",
        "description": "User receives repeated login prompts in a new browser.",
        "category": "authentication",
        "resolution": "Browser cache and cookies were cleared, then the user signed in again.",
        "resolved_date": "2024-08-12"
    }
]

documents = [
    {
        "id": "DOC-001",
        "title": "Finance Application Authentication Guide",
        "content": "After a password reset, sign out from all active sessions, clear the browser session if necessary, and sign in again using the new password.",
        "category": "authentication",
        "last_updated": "2025-02-15",
        "validity_period_days": 730
    },
    {
        "id": "DOC-002",
        "title": "VPN Authentication Troubleshooting",
        "content": "For VPN authentication failures, verify the updated password, refresh the VPN profile, and confirm that multi-factor authentication is completed.",
        "category": "authentication",
        "last_updated": "2024-01-15",
        "validity_period_days": 365
    },
    {
        "id": "DOC-003",
        "title": "Application Configuration Standard",
        "content": "Configuration errors should be investigated by comparing the local configuration with the approved configuration template.",
        "category": "configuration",
        "last_updated": "2025-05-01",
        "validity_period_days": 730
    },
    {
        "id": "DOC-004",
        "title": "Software Access Request Procedure",
        "content": "Software access requires a valid request, manager approval, and membership in the relevant access group.",
        "category": "software-access",
        "last_updated": "2023-01-10",
        "validity_period_days": 365
    }
]

evaluation = [
    {
        "id": "EVAL-001",
        "ticket": "The user cannot access the Finance application after resetting their password and receives an authentication error.",
        "category": "authentication",
        "expected_ticket_ids": ["INC-1001", "INC-1002"],
        "expected_document_ids": ["DOC-001"],
        "expected_escalation": False
    },
    {
        "id": "EVAL-002",
        "ticket": "A user cannot connect to VPN after changing their password.",
        "category": "authentication",
        "expected_ticket_ids": ["INC-1002"],
        "expected_document_ids": ["DOC-002"],
        "expected_escalation": False
    },
    {
        "id": "EVAL-003",
        "ticket": "The application shows an invalid configuration message when it starts.",
        "category": "configuration",
        "expected_ticket_ids": ["INC-1003"],
        "expected_document_ids": ["DOC-003"],
        "expected_escalation": False
    },
    {
        "id": "EVAL-004",
        "ticket": "The employee still has no access to the reporting application.",
        "category": "software-access",
        "expected_ticket_ids": ["INC-1004"],
        "expected_document_ids": ["DOC-004"],
        "expected_escalation": False
    },
    {
        "id": "EVAL-005",
        "ticket": "The payroll system is failing with an unknown error code that is not found in the knowledge base.",
        "category": "unknown",
        "expected_ticket_ids": [],
        "expected_document_ids": [],
        "expected_escalation": True
    }
]

def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as file:
        for record in records:
            file.write(json.dumps(record) + "\n")

write_jsonl(DATA_DIR / "tickets.jsonl", tickets)
write_jsonl(DATA_DIR / "documents.jsonl", documents)
write_jsonl(DATA_DIR / "evaluation.jsonl", evaluation)

print("Sample data created in the data folder.")