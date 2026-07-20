from backend.app.schemas.actions import ClinicalActionType
from backend.app.schemas.comparison import (
    ActionTimingComparison,
    ImprovementOutcome,
    SessionComparison,
)
from backend.app.schemas.timeline import SimulationSession
from backend.app.scoring.evaluator import evaluate_session


TRACKED_ACTIONS = (
    ClinicalActionType.CALL_FOR_HELP,
    ClinicalActionType.START_IV_FLUIDS,
    ClinicalActionType.ACTIVATE_TRANSFUSION,
)


def _first_action_time(
    session: SimulationSession,
    action: ClinicalActionType,
) -> int | None:
    for event in session.timeline:
        if event.action == action:
            return event.elapsed_seconds

    return None


def _compare_action_timing(
    initial_session: SimulationSession,
    replay_session: SimulationSession,
    action: ClinicalActionType,
) -> ActionTimingComparison:
    initial_time = _first_action_time(initial_session, action)
    replay_time = _first_action_time(replay_session, action)

    seconds_faster: int | None = None

    if initial_time is not None and replay_time is not None:
        seconds_faster = initial_time - replay_time

    return ActionTimingComparison(
        action=action,
        initial_time_seconds=initial_time,
        replay_time_seconds=replay_time,
        seconds_faster=seconds_faster,
        omission_corrected=initial_time is None and replay_time is not None,
    )


def compare_sessions(
    initial_session: SimulationSession,
    replay_session: SimulationSession,
) -> SessionComparison:
    if (
        initial_session.current_state.scenario_id
        != replay_session.current_state.scenario_id
    ):
        raise ValueError(
            "Sessions from different scenarios cannot be compared."
        )

    initial_score = evaluate_session(initial_session)
    replay_score = evaluate_session(replay_session)

    score_delta = replay_score.total_score - initial_score.total_score
    harm_reduction = initial_score.final_harm - replay_score.final_harm

    initial_omissions = set(initial_score.critical_omissions)
    replay_omissions = set(replay_score.critical_omissions)

    corrected_omissions = [
        action
        for action in TRACKED_ACTIONS
        if action in initial_omissions and action not in replay_omissions
    ]

    new_omissions = [
        action
        for action in TRACKED_ACTIONS
        if action not in initial_omissions and action in replay_omissions
    ]

    action_timings = [
        _compare_action_timing(
            initial_session=initial_session,
            replay_session=replay_session,
            action=action,
        )
        for action in TRACKED_ACTIONS
    ]

    if score_delta > 0:
        outcome = ImprovementOutcome.IMPROVED
    elif score_delta < 0:
        outcome = ImprovementOutcome.WORSENED
    elif harm_reduction > 0:
        outcome = ImprovementOutcome.IMPROVED
    elif harm_reduction < 0:
        outcome = ImprovementOutcome.WORSENED
    else:
        outcome = ImprovementOutcome.UNCHANGED

    return SessionComparison(
        initial_score=initial_score,
        replay_score=replay_score,
        score_delta=score_delta,
        harm_reduction=harm_reduction,
        corrected_omissions=corrected_omissions,
        new_omissions=new_omissions,
        action_timings=action_timings,
        outcome=outcome,
    )
