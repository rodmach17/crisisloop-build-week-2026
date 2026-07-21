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

    assert determine_replay_from_seconds(score) == 90


def test_coach_prompt_hides_internal_action_identifiers() -> None:
    from pathlib import Path

    service_text = Path(
        "backend/app/coach/service.py"
    ).read_text()

    assert "Never expose internal enum values" in service_text
    assert "Each list item must contain exactly one clear idea" in service_text


def test_coach_prompt_requires_concise_feedback() -> None:
    from pathlib import Path

    service_text = Path(
        "backend/app/coach/service.py"
    ).read_text()

    assert "Be concise and operational" in service_text
    assert "Avoid essays, protocol digressions" in service_text


def test_compact_list_item_keeps_first_sentence() -> None:
    from backend.app.coach.service import _compact_list_item

    result = _compact_list_item(
        (
            "Iniciar líquidos intravenosos de inmediato. "
            "Este texto adicional no debe mostrarse."
        ),
        max_length=180,
    )

    assert result == "Iniciar líquidos intravenosos de inmediato."


def test_compact_list_item_removes_long_disclaimer_tail() -> None:
    from backend.app.coach.service import _compact_list_item

    result = _compact_list_item(
        (
            "Iniciar líquidos intravenosos para apoyar la circulación "
            "durante la hemorragia activa, dentro del escenario simulado "
            "educativo únicamente y sin sustituir protocolos reales."
        ),
        max_length=90,
    )

    assert len(result) <= 91
    assert result.startswith("Iniciar líquidos intravenosos")
    assert "protocolos reales" not in result


def test_generate_debrief_uses_structured_async_response(monkeypatch) -> None:
    import anyio

    from backend.app.coach.service import generate_adaptive_debrief
    from backend.app.engine.session import create_simulation_session
    from backend.app.schemas.coach import AdaptiveDebriefContent
    from backend.app.scoring.evaluator import evaluate_session

    captured = {}
    parsed = AdaptiveDebriefContent(
        performance_summary="No critical failure was detected.",
        strengths=["The learner escalated care."],
        improvement_priorities=["Continue acting promptly."],
        clinical_reasoning_explanation="The verified timeline supports this.",
        replay_objective="Repeat the timely sequence.",
        replay_success_criteria=["Escalate within 60 seconds."],
    )

    class FakeResponse:
        output_parsed = parsed

    class FakeResponses:
        async def parse(self, **kwargs):
            captured.update(kwargs)
            return FakeResponse()

    class FakeClient:
        responses = FakeResponses()

    monkeypatch.setenv("CRISISLOOP_COACH_MODEL", "test-model")
    session = create_simulation_session()
    score = evaluate_session(session)

    result = anyio.run(
        generate_adaptive_debrief,
        session,
        score,
        "English",
        FakeClient(),
    )

    assert result.model == "test-model"
    assert result.score == score
    assert captured["store"] is False
    assert captured["text_format"] is AdaptiveDebriefContent
