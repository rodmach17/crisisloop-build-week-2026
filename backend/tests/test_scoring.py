from backend.app.engine.session import (
    advance_session,
    apply_action_to_session,
    create_simulation_session,
)
from backend.app.schemas.actions import ClinicalActionType
from backend.app.scoring.evaluator import evaluate_session


def test_delayed_session_receives_low_score_and_critical_decision() -> None:
    session = create_simulation_session()
    session = advance_session(session, 180)

    result = evaluate_session(session)

    assert result.total_score < 40
    assert ClinicalActionType.CALL_FOR_HELP in result.critical_omissions
    assert result.critical_decision is not None
    assert result.critical_decision.elapsed_seconds == 120


def test_early_actions_receive_higher_score() -> None:
    session = create_simulation_session()
    session = advance_session(session, 30)
    session = apply_action_to_session(
        session,
        ClinicalActionType.CALL_FOR_HELP,
    )
    session = advance_session(session, 20)
    session = apply_action_to_session(
        session,
        ClinicalActionType.START_IV_FLUIDS,
    )
    session = advance_session(session, 20)
    session = apply_action_to_session(
        session,
        ClinicalActionType.ACTIVATE_TRANSFUSION,
    )

    result = evaluate_session(session)

    assert result.total_score >= 80
    assert result.critical_omissions == []
    assert result.critical_decision is None


def test_early_actions_outscore_delayed_management() -> None:
    delayed = create_simulation_session()
    delayed = advance_session(delayed, 180)

    early = create_simulation_session()
    early = advance_session(early, 30)
    early = apply_action_to_session(
        early,
        ClinicalActionType.CALL_FOR_HELP,
    )
    early = advance_session(early, 20)
    early = apply_action_to_session(
        early,
        ClinicalActionType.START_IV_FLUIDS,
    )
    early = advance_session(early, 20)
    early = apply_action_to_session(
        early,
        ClinicalActionType.ACTIVATE_TRANSFUSION,
    )

    delayed_score = evaluate_session(delayed)
    early_score = evaluate_session(early)

    assert early_score.total_score > delayed_score.total_score
    assert early_score.final_harm < delayed_score.final_harm
