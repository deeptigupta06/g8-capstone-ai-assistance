import json
from pathlib import Path

from src.agent_graph import analyse_ticket
from src.hybrid_retriever import build_index, hybrid_search


BASE_DIR = Path(__file__).resolve().parents[1]
evaluation_path = BASE_DIR / "data" / "evaluation.jsonl"

build_index()

records = []

with open(evaluation_path, "r", encoding="utf-8") as file:
    for line in file:
        records.append(json.loads(line))

successful_retrieval = 0
correct_escalation = 0

for record in records:
    results = hybrid_search(
        record["ticket"],
        category=record["category"],
        limit=5
    )

    retrieved_ids = [item["id"] for item in results]

    expected_ids = (
        record["expected_ticket_ids"]
        + record["expected_document_ids"]
    )

    if any(source_id in retrieved_ids for source_id in expected_ids):
        successful_retrieval += 1

    answer = analyse_ticket(
        record["ticket"],
        record["category"]
    )

    if answer["should_escalate"] == record["expected_escalation"]:
        correct_escalation += 1

total = len(records)

print(f"Total evaluation cases: {total}")
print(
    f"Retrieval success: "
    f"{successful_retrieval / total:.2%}"
)
print(
    f"Escalation accuracy: "
    f"{correct_escalation / total:.2%}"
)