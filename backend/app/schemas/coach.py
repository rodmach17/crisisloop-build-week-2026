from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    StringConstraints,
    field_validator,
)

from backend.app.schemas.scoring import SessionScore
from backend.app.schemas.timeline import SimulationSession


StrengthText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=220,
    ),
]

PriorityText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=300,
    ),
]

SuccessCriterionText = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        max_length=220,
    ),
]


class AdaptiveDebriefContent(BaseModel):
    performance_summary: str = Field(
        min_length=1,
        max_length=600,
    )
    strengths: list[StrengthText] = Field(
        min_length=1,
        max_length=3,
    )
    improvement_priorities: list[PriorityText] = Field(
        min_length=1,
        max_length=3,
    )
    clinical_reasoning_explanation: str = Field(
        min_length=1,
        max_length=900,
    )
    replay_objective: str = Field(
        min_length=1,
        max_length=350,
    )
    replay_success_criteria: list[SuccessCriterionText] = Field(
        min_length=1,
        max_length=3,
    )


class CoachDebriefRequest(BaseModel):
    session: SimulationSession
    language: str = Field(
        default="English",
        min_length=2,
        max_length=40,
    )

    @field_validator("language")
    @classmethod
    def validate_language(cls, value: str) -> str:
        normalized = value.strip()

        if not normalized:
            raise ValueError("Language cannot be empty.")

        allowed_characters = all(
            character.isalpha()
            or character in {" ", "-", "(", ")"}
            for character in normalized
        )

        if not allowed_characters:
            raise ValueError(
                "Language may contain only letters, spaces, hyphens, "
                "and parentheses."
            )

        return normalized


class CoachDebriefResponse(BaseModel):
    session_id: str
    model: str
    language: str = Field(min_length=2, max_length=40)
    score: SessionScore
    replay_from_seconds: int = Field(ge=0)
    debrief: AdaptiveDebriefContent
    educational_use_only: bool = True
