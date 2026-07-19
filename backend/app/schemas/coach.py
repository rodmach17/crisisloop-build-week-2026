from pydantic import BaseModel, Field

from backend.app.schemas.scoring import SessionScore
from backend.app.schemas.timeline import SimulationSession


class AdaptiveDebriefContent(BaseModel):
    performance_summary: str = Field(
        min_length=1,
        description="Concise educational summary of the learner's performance.",
    )
    strengths: list[str] = Field(
        min_length=1,
        max_length=3,
        description="Specific strengths supported by the verified timeline.",
    )
    improvement_priorities: list[str] = Field(
        min_length=1,
        max_length=3,
        description="Specific priorities supported by the verified timeline.",
    )
    clinical_reasoning_explanation: str = Field(
        min_length=1,
        description="Educational explanation of the crisis recognition and response.",
    )
    replay_objective: str = Field(
        min_length=1,
        description="A focused objective for the next replay attempt.",
    )
    replay_success_criteria: list[str] = Field(
        min_length=1,
        max_length=3,
        description="Observable criteria for improvement during replay.",
    )


class CoachDebriefRequest(BaseModel):
    session: SimulationSession


class CoachDebriefResponse(BaseModel):
    session_id: str
    model: str
    score: SessionScore
    replay_from_seconds: int = Field(ge=0)
    debrief: AdaptiveDebriefContent
    educational_use_only: bool = True
