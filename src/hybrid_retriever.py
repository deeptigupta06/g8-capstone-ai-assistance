from datetime import date, datetime
from pathlib import Path

import chromadb
from rank_bm25 import BM25Okapi
from openai import OpenAI
from dotenv import load_dotenv

from src.data_loader import load_all_data

load_dotenv()

client = OpenAI()
tickets, documents = load_all_data()
all_records = []

for ticket in tickets:
    all_records.append({
        "id": ticket["id"],
        "source_type": "ticket",
        "text": (
            f'{ticket["title"]}. '
            f'{ticket["description"]}. '
            f'Category: {ticket["category"]}. '
            f'Resolution: {ticket["resolution"]}'
        ),
        "category": ticket["category"],
        "last_updated": ticket["resolved_date"]
    })

for document in documents:
    all_records.append({
        "id": document["id"],
        "source_type": "document",
        "text": (
            f'{document["title"]}. '
            f'{document["content"]}. '
            f'Category: {document["category"]}.'
        ),
        "category": document["category"],
        "last_updated": document["last_updated"],
        "validity_period_days": document["validity_period_days"]
    })

chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection("support_evidence")

def create_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding


def build_index():
    existing = collection.count()

    if existing > 0:
        return

    embeddings = [create_embedding(record["text"]) for record in all_records]

    collection.add(
        ids=[record["id"] for record in all_records],
        documents=[record["text"] for record in all_records],
        embeddings=embeddings,
        metadatas=[
            {
                "source_type": record["source_type"],
                "category": record["category"],
                "last_updated": record["last_updated"]
            }
            for record in all_records
        ]
    )


def keyword_results(query, category=None, limit=5):
    tokenised_documents = [
        record["text"].lower().split()
        for record in all_records
    ]

    bm25 = BM25Okapi(tokenised_documents)
    scores = bm25.get_scores(query.lower().split())

    ranked = sorted(
        zip(all_records, scores),
        key=lambda item: item[1],
        reverse=True
    )

    results = []

    for record, score in ranked:
        if category and record["category"] != category:
            continue

        results.append({
            **record,
            "keyword_score": float(score)
        })

        if len(results) >= limit:
            break

    return results


def semantic_results(query, category=None, limit=5):
    query_embedding = create_embedding(query)

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=limit
    )

    results = []

    for i, source_id in enumerate(result["ids"][0]):
        metadata = result["metadatas"][0][i]

        if category and metadata["category"] != category:
            continue

        matching = next(
            record for record in all_records
            if record["id"] == source_id
        )

        results.append({
            **matching,
            "semantic_rank": i + 1
        })

    return results


def hybrid_search(query, category=None, limit=5):
    semantic = semantic_results(query, category, limit)
    keyword = keyword_results(query, category, limit)

    combined = {}

    for rank, item in enumerate(semantic, start=1):
        combined.setdefault(item["id"], {**item})
        combined[item["id"]]["hybrid_score"] = combined[item["id"]].get(
            "hybrid_score", 0
        ) + 0.6 * (1 / (60 + rank))

    for rank, item in enumerate(keyword, start=1):
        combined.setdefault(item["id"], {**item})
        combined[item["id"]]["hybrid_score"] = combined[item["id"]].get(
            "hybrid_score", 0
        ) + 0.4 * (1 / (60 + rank))

    results = sorted(
        combined.values(),
        key=lambda item: item.get("hybrid_score", 0),
        reverse=True
    )

    today = date.today()

    for result in results:
        try:
            last_updated = datetime.strptime(
                result["last_updated"], "%Y-%m-%d"
            ).date()

            age_days = (today - last_updated).days
            validity = result.get("validity_period_days", 730)

            result["possibly_outdated"] = age_days > validity
        except Exception:
            result["possibly_outdated"] = False

    return results[:limit]