from enum import StrEnum

from pydantic import BaseModel

from backend.app.schemas.actions import ClinicalActionType
from backend.app.schemas.scoring import SessionScore


class ImprovementOutcome(StrEnum):
    IMPROVED = "improved"
    UNCHANGED = "unchanged"
    WORSENED = "worsened"


class ActionTimingComparison(BaseModel):
    action: ClinicalActionType
    initial_time_seconds: int | None
    replay_time_seconds: int | None
    seconds_faster: int | None
    omission_corrected: bool


class SessionComparison(BaseModel):
    initial_score: SessionScore
    replay_score: SessionScore
    score_delta: int
    harm_reduction: int
    corrected_omissions: list[ClinicalActionType]
    new_omissions: list[ClinicalActionType]
    action_timings: list[ActionTimingComparison]
    outcome: ImprovementOutcome
