from typing import TypedDict, List
import json

from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from openai import OpenAI

from src.hybrid_retriever import hybrid_search
from src.models import AssistantResponse

load_dotenv()

client = OpenAI()


class AgentState(TypedDict):
    ticket: str
    category: str
    evidence: List[dict]
    retry_count: int
    response: dict
    application: str


def retrieve(state: AgentState):
    evidence = hybrid_search(
        state["ticket"],
        category=state.get("category"),
        limit=5
    )

    return {
        "evidence": evidence
    }


def validate_evidence(state: AgentState):
    evidence = state.get("evidence", [])

    if len(evidence) == 0:
        return {
            "retry_count": state.get("retry_count", 0) + 1
        }

    return {}


def route_after_validation(state: AgentState):
    evidence = state.get("evidence", [])
    retry_count = state.get("retry_count", 0)

    if len(evidence) == 0 and retry_count < 2:
        return "retry"

    if len(evidence) == 0:
        return "generate"

    return "generate"


def generate_answer(state: AgentState):
    evidence_text = "\n\n".join(
    [
        f'ID: {item["id"]}\n'
        f'Type: {item["source_type"]}\n'
        f'Application: {item.get("application", "")}\n'
        f'Content: {item["text"]}\n'
        f'URL: {item.get("url", "")}\n'
        f'Agent instruction: {item.get("agent_instruction", "")}\n'
        f'Escalation instruction: {item.get("escalation_instruction", "")}\n'
        f'Possibly outdated: {item.get("possibly_outdated", False)}'
        for item in state.get("evidence", [])
    ]
)

    prompt = f"""
    You are a controlled support-ticket resolution assistant.

    New ticket:
    {state["ticket"]}

    Retrieved evidence:
    {evidence_text}

    Use only the retrieved evidence.
    Do not invent information.
    Do not make system changes.
    Do not close the ticket.
    Recommend escalation if the evidence is weak or missing.

    Return a JSON object with exactly these field names:

    summary
    category
    application
    diagnostic_steps
    recommended_resolution
    agent_instructions
    evidence
    outdated_warnings
    should_escalate
    escalation_reason
    escalation_information
    confidence

    Formatting rules:

    - summary must be a string.
    - category must be a string.
    - application must be a string.
    - diagnostic_steps must be an array of strings.
    - recommended_resolution must be an array of strings.
    - agent_instructions must be an array of strings.
    - evidence must be an array of objects.
    - Each evidence object must contain source_id, source_type, reason, title, and url.
    - outdated_warnings must be an array of strings.
    - should_escalate must be true or false.
    - escalation_reason must be a string.
    - escalation_information must be an array of strings.
    - confidence must be a number between 0 and 1.
    - Do not return confidence as low, medium, or high.
    - Do not invent KB IDs or URLs.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You produce grounded support recommendations."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    raw = json.loads(
        response.choices[0].message.content
    )

    def make_list(value):
        if value is None:
            return []

        if isinstance(value, list):
            return value

        return [value]

    evidence_list = []

    for item in raw.get("evidence", []):
        evidence_list.append({
            "source_id": item.get(
                "source_id",
                item.get(
                    "ID",
                    item.get("id", "UNKNOWN")
                )
            ),

            "source_type": item.get(
                "source_type",
                item.get(
                    "Type",
                    item.get("type", "unknown")
                )
            ),

            "reason": item.get(
                "reason",
                "Retrieved as relevant evidence."
            ),

            "title": item.get(
                "title",
                item.get(
                    "Title",
                    ""
                )
            ),

            "url": item.get(
                "url",
                item.get(
                    "URL",
                    ""
                )
            )
        })

    confidence = raw.get("confidence", 0.0)

    if isinstance(confidence, str):
        confidence_values = {
            "low": 0.3,
            "medium": 0.6,
            "high": 0.9
        }

        confidence = confidence_values.get(
            confidence.lower(),
            0.0
        )

    parsed = AssistantResponse(
        summary=raw.get(
            "summary",
            ""
        ),
        category=raw.get(
            "category",
            state.get("category", "")
        ),
        application=raw.get(
            "application",
            state.get("application", "")
        ),
        diagnostic_steps=make_list(
            raw.get(
                "diagnostic_steps",
                []
            )
        ),
        recommended_resolution=make_list(
            raw.get(
                "recommended_resolution",
                []
            )
        ),
        agent_instructions=make_list(
            raw.get(
                "agent_instructions",
                []
            )
        ),
        evidence=evidence_list,
        outdated_warnings=make_list(
            raw.get(
                "outdated_warnings",
                []
            )
        ),
        should_escalate=bool(
            raw.get(
                "should_escalate",
                False
            )
        ),
        escalation_reason=raw.get(
            "escalation_reason",
            ""
        ),
        escalation_information=make_list(
            raw.get(
                "escalation_information",
                []
            )
        ),
        confidence=float(
            confidence
        )
    )

    return {
        "response": parsed.model_dump()
    }

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("retrieve", retrieve)
    graph.add_node("validate", validate_evidence)
    graph.add_node("generate", generate_answer)

    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "validate")

    graph.add_conditional_edges(
        "validate",
        route_after_validation,
        {
            "retry": "retrieve",
            "generate": "generate"
        }
    )

    graph.add_edge("generate", END)

    return graph.compile()


def analyse_ticket(ticket: str, category: str, application: str):
    graph = build_graph()

    result = graph.invoke({
        "ticket": ticket,
        "category": category,
        "application": application,
        "evidence": [],
        "retry_count": 0,
        "response": {}
    })

    return result["response"]