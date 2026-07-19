from typing import Literal

from pydantic import BaseModel, Field

from backend.app.schemas.scoring import SessionScore
from backend.app.schemas.timeline import SimulationSession


CoachLanguage = Literal["en", "es"]


class AdaptiveDebriefContent(BaseModel):
    performance_summary: str = Field(min_length=1)
    strengths: list[str] = Field(min_length=1, max_length=3)
    improvement_priorities: list[str] = Field(min_length=1, max_length=3)
    clinical_reasoning_explanation: str = Field(min_length=1)
    replay_objective: str = Field(min_length=1)
    replay_success_criteria: list[str] = Field(
        min_length=1,
        max_length=3,
    )


class CoachDebriefRequest(BaseModel):
    session: SimulationSession
    language: CoachLanguage = "en"


class CoachDebriefResponse(BaseModel):
    session_id: str
    model: str
    language: CoachLanguage
    score: SessionScore
    replay_from_seconds: int = Field(ge=0)
    debrief: AdaptiveDebriefContent
    educational_use_only: bool = True
