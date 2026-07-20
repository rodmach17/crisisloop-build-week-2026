import pytest

from backend.app.engine.session import (
    advance_session,
    apply_action_to_session,
    create_replay_session,
    create_simulation_session,
)
from backend.app.schemas.actions import ClinicalActionType
from backend.app.schemas.comparison import ImprovementOutcome
from backend.app.scoring.comparison import compare_sessions


def _build_failed_initial_attempt():
    session = create_simulation_session()
    return advance_session(session, 180)


def _build_successful_replay(initial_session):
    replay = create_replay_session(
        source_session=initial_session,
        replay_from_seconds=90,
    )
    replay = apply_action_to_session(
        replay,
        ClinicalActionType.CALL_FOR_HELP,
    )
    replay = apply_action_to_session(
        replay,
        ClinicalActionType.START_IV_FLUIDS,
    )
    replay = apply_action_to_session(
        replay,
        ClinicalActionType.ACTIVATE_TRANSFUSION,
    )
    return replay


def test_comparison_detects_improvement() -> None:
    initial = _build_failed_initial_attempt()
    replay = _build_successful_replay(initial)

    result = compare_sessions(initial, replay)

    assert result.outcome == ImprovementOutcome.IMPROVED
    assert result.score_delta > 0
    assert result.harm_reduction > 0
    assert result.replay_score.total_score > result.initial_score.total_score


def test_comparison_detects_corrected_omissions() -> None:
    initial = _build_failed_initial_attempt()
    replay = _build_successful_replay(initial)

    result = compare_sessions(initial, replay)

    assert result.corrected_omissions == [
        ClinicalActionType.CALL_FOR_HELP,
        ClinicalActionType.START_IV_FLUIDS,
        ClinicalActionType.ACTIVATE_TRANSFUSION,
    ]
    assert result.new_omissions == []


def test_comparison_reports_action_times() -> None:
    initial = _build_failed_initial_attempt()
    replay = _build_successful_replay(initial)

    result = compare_sessions(initial, replay)

    help_timing = result.action_timings[0]

    assert help_timing.action == ClinicalActionType.CALL_FOR_HELP
    assert help_timing.initial_time_seconds is None
    assert help_timing.replay_time_seconds == 90
    assert help_timing.seconds_faster is None
    assert help_timing.omission_corrected is True


def test_identical_attempts_are_unchanged() -> None:
    initial = create_simulation_session()
    initial = advance_session(initial, 60)

    result = compare_sessions(initial, initial.model_copy(deep=True))

    assert result.outcome == ImprovementOutcome.UNCHANGED
    assert result.score_delta == 0
    assert result.harm_reduction == 0


def test_comparison_rejects_different_scenarios() -> None:
    initial = create_simulation_session()
    replay = create_simulation_session()
    replay.current_state.scenario_id = "different_scenario"

    with pytest.raises(
        ValueError,
        match="Sessions from different scenarios cannot be compared",
    ):
        compare_sessions(initial, replay)
