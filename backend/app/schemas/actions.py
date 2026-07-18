from enum import StrEnum

from pydantic import BaseModel

from backend.app.schemas.patient import PatientState


class ClinicalActionType(StrEnum):
    CALL_FOR_HELP = "call_for_help"
    START_IV_FLUIDS = "start_iv_fluids"
    ACTIVATE_TRANSFUSION = "activate_transfusion"


class ApplyActionRequest(BaseModel):
    state: PatientState
    action: ClinicalActionType


class ActionResult(BaseModel):
    action: ClinicalActionType
    description: str
    state_before: PatientState
    state_after: PatientState
