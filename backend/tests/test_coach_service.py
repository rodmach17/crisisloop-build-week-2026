from backend.app.coach.service import determine_replay_from_seconds
from backend.app.schemas.actions import ClinicalActionType
from backend.app.schemas.scoring import CriticalDecision, SessionScore


def _build_score(
    critical_decision: CriticalDecision | None,
) -> SessionScore:
    return SessionScore(
        total_score=60,
        recognition_score=20,
        intervention_score=20,
        safety_score=20,
        final_harm=30,
        critical_omissions=[],
        critical_decision=critical_decision,
    )


def test_replay_starts_at_zero_without_critical_decision() -> None:
    score = _build_score(critical_decision=None)

    assert determine_replay_from_seconds(score) == 0


def test_replay_uses_deterministic_critical_decision_time() -> None:
    score = _build_score(
        critical_decision=CriticalDecision(
            elapsed_seconds=120,
            reason="Delayed recognition and escalation.",
            missed_action=ClinicalActionType.CALL_FOR_HELP,
        )
    )

    assert determine_replay_from_seconds(score) == 120
