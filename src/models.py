from typing import List
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    source_id: str
    source_type: str
    reason: str
    title: str = ""
    url: str = ""


class AssistantResponse(BaseModel):
    summary: str
    category: str
    application: str
    diagnostic_steps: List[str]
    recommended_resolution: List[str]
    agent_instructions: List[str]
    evidence: List[Evidence]
    outdated_warnings: List[str]
    should_escalate: bool
    escalation_reason: str
    escalation_information: List[str]
    confidence: float = Field(ge=0.0, le=1.0)