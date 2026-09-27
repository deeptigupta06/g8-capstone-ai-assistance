import json
from pathlib import Path


def load_jsonl(path):
    records = []

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            if line.strip():
                records.append(json.loads(line))

    return records


def load_all_data():
    base_dir = Path(__file__).resolve().parents[1]

    tickets = load_jsonl(
        base_dir / "data" / "tickets.jsonl"
    )

    documents = load_jsonl(
        base_dir / "data" / "documents.jsonl"
    )

    knowledge_base = load_jsonl(
        base_dir / "data" / "knowledge_base.jsonl"
    )

    return tickets, documents, knowledge_base