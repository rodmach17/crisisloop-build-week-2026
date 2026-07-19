from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.schemas.coach import (
    AdaptiveDebriefContent,
    CoachDebriefResponse,
)

client = TestClient(app)


def test_coach_debrief_endpoint_returns_structured_response(
    monkeypatch,
) -> None:
    def fake_generate_adaptive_debrief(
        session,
        score,
        language,
    ) -> CoachDebriefResponse:
        return CoachDebriefResponse(
            session_id=session.session_id,
            model="gpt-5.6-sol",
            language=language,
            score=score,
            replay_from_seconds=90,
            debrief=AdaptiveDebriefContent(
                performance_summary="Delayed recognition was identified.",
                strengths=["The simulation was completed."],
                improvement_priorities=[
                    "Recognize deterioration earlier.",
                ],
                clinical_reasoning_explanation=(
                    "Progressive hypotension and tachycardia indicated "
                    "ongoing hemorrhagic shock."
                ),
                replay_objective=(
                    "Escalate and initiate resuscitation earlier."
                ),
                replay_success_criteria=[
                    "Call for help within 60 seconds.",
                    "Activate transfusion within 120 seconds.",
                ],
            ),
            educational_use_only=True,
        )

    monkeypatch.setattr(
        "backend.app.main.generate_adaptive_debrief",
        fake_generate_adaptive_debrief,
    )

    session_response = client.post("/session")
    assert session_response.status_code == 200

    session = session_response.json()

    advance_response = client.post(
        "/session/advance",
        json={
            "session": session,
            "seconds": 120,
        },
    )
    assert advance_response.status_code == 200

    response = client.post(
        "/coach/debrief",
        json={
            "session": advance_response.json(),
            "language": "es",
        },
    )

    assert response.status_code == 200

    result = response.json()

    assert result["model"] == "gpt-5.6-sol"
    assert result["replay_from_seconds"] == 90
    assert result["language"] == "es"
    assert result["educational_use_only"] is True
    assert result["score"]["critical_decision"]["elapsed_seconds"] == 120
