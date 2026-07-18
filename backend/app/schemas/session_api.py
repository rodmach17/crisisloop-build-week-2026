from pydantic import BaseModel, Field

from backend.app.schemas.actions import ClinicalActionType
from backend.app.schemas.scoring import SessionScore
from backend.app.schemas.timeline import SimulationSession


class AdvanceSessionRequest(BaseModel):
    session: SimulationSession
    seconds: int = Field(gt=0, le=600)


class ApplySessionActionRequest(BaseModel):
    session: SimulationSession
    action: ClinicalActionType


class SessionScoreResponse(BaseModel):
    session: SimulationSession
    score: SessionScore
