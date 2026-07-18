from pydantic import BaseModel, Field

from backend.app.schemas.actions import ClinicalActionType


class CriticalDecision(BaseModel):
    elapsed_seconds: int = Field(ge=0)
    reason: str
    missed_action: ClinicalActionType | None = None


class SessionScore(BaseModel):
    total_score: int = Field(ge=0, le=100)
    recognition_score: int = Field(ge=0, le=30)
    intervention_score: int = Field(ge=0, le=40)
    safety_score: int = Field(ge=0, le=30)
    final_harm: int = Field(ge=0, le=100)
    critical_omissions: list[ClinicalActionType]
    critical_decision: CriticalDecision | None = None
