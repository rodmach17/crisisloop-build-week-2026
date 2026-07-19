import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from backend.app.schemas.coach import (
    AdaptiveDebriefContent,
    CoachDebriefResponse,
)
from backend.app.schemas.scoring import SessionScore
from backend.app.schemas.timeline import SimulationSession


DEFAULT_COACH_MODEL = "gpt-5.6-sol"


def determine_replay_from_seconds(score: SessionScore) -> int:
    """Start replay before the deterministic critical decision."""
    if score.critical_decision is None:
        return 0

    return max(0, score.critical_decision.elapsed_seconds - 30)


def _load_environment() -> None:
    project_root = Path(__file__).resolve().parents[3]
    load_dotenv(dotenv_path=project_root / ".env")


def generate_adaptive_debrief(
    session: SimulationSession,
    score: SessionScore,
    language: str = "English",
    client: OpenAI | None = None,
) -> CoachDebriefResponse:
    """Generate educational feedback without changing simulation state."""
    _load_environment()

    selected_model = os.getenv(
        "CRISISLOOP_COACH_MODEL",
        DEFAULT_COACH_MODEL,
    )
    openai_client = client or OpenAI()

    replay_from_seconds = determine_replay_from_seconds(score)
    language_name = language.strip()

    verified_payload = {
        "scenario": "Occult postoperative hemorrhage with hypovolemic shock",
        "session": session.model_dump(mode="json"),
        "deterministic_score": score.model_dump(mode="json"),
        "replay_from_seconds": replay_from_seconds,
        "output_language": language,
    }

    response = openai_client.responses.parse(
        model=selected_model,
        store=False,
        input=[
            {
                "role": "system",
                "content": (
                    "You are the adaptive educational coach for CrisisLoop. "
                    "Use only the verified timeline and deterministic score. "
                    "Do not invent actions, times, vital signs, outcomes, or "
                    "scores. Do not modify the simulation. "
                    f"Write every field in {language_name}. "
                    "Strengths must describe learner actions that are explicitly "
                    "documented in the timeline and were clinically appropriate. "
                    "Never describe residual score points, missing data, absence "
                    "of unverified actions, system behavior, or completion of the "
                    "simulation as learner strengths. If no genuine learner "
                    "strength is documented, state honestly that no demonstrated "
                    "clinical strength was recorded in this attempt. "
                    "Improvement priorities must be specific and supported by the "
                    "verified evidence. The replay time is fixed by the application "
                    "and must not be changed. This is educational simulation "
                    "feedback, not patient-specific medical advice."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    verified_payload,
                    ensure_ascii=False,
                ),
            },
        ],
        text_format=AdaptiveDebriefContent,
    )

    debrief = response.output_parsed
    if debrief is None:
        raise RuntimeError(
            "GPT-5.6 did not return a valid structured debrief."
        )

    return CoachDebriefResponse(
        session_id=session.session_id,
        model=selected_model,
        language=language,
        score=score,
        replay_from_seconds=replay_from_seconds,
        debrief=debrief,
        educational_use_only=True,
    )
