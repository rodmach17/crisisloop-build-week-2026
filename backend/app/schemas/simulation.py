from pydantic import BaseModel, Field

from backend.app.schemas.patient import PatientState


class AdvanceScenarioRequest(BaseModel):
    state: PatientState
    seconds: int = Field(gt=0, le=600)


class AdvanceScenarioResponse(BaseModel):
    previous_state: PatientState
    current_state: PatientState
