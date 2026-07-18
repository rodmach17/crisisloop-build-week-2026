from pydantic import BaseModel, Field

from backend.app.schemas.actions import ClinicalActionType
from backend.app.schemas.patient import PatientState


class TimelineEvent(BaseModel):
    elapsed_seconds: int = Field(ge=0)
    event_type: str
    action: ClinicalActionType | None = None
    description: str
    state_before: PatientState
    state_after: PatientState


class SimulationSession(BaseModel):
    session_id: str
    initial_state: PatientState
    current_state: PatientState
    timeline: list[TimelineEvent]
