from backend.app.engine.session import (
    advance_session,
    apply_action_to_session,
    create_simulation_session,
)
from backend.app.schemas.actions import ClinicalActionType


def test_new_session_starts_with_empty_timeline() -> None:
    session = create_simulation_session()

    assert session.current_state.elapsed_seconds == 0
    assert session.timeline == []
    assert session.session_id


def test_time_advance_is_recorded_in_timeline() -> None:
    session = create_simulation_session()

    updated = advance_session(session, 90)

    assert updated.current_state.elapsed_seconds == 90
    assert len(updated.timeline) == 1
    assert updated.timeline[0].event_type == "time_advance"
    assert updated.timeline[0].elapsed_seconds == 90


def test_clinical_action_is_recorded_at_current_time() -> None:
    session = create_simulation_session()
    session = advance_session(session, 180)

    updated = apply_action_to_session(
        session,
        ClinicalActionType.ACTIVATE_TRANSFUSION,
    )

    assert len(updated.timeline) == 2
    assert updated.timeline[1].event_type == "clinical_action"
    assert updated.timeline[1].action == ClinicalActionType.ACTIVATE_TRANSFUSION
    assert updated.timeline[1].elapsed_seconds == 180
    assert (
        updated.timeline[1].state_after.cumulative_harm
        < updated.timeline[1].state_before.cumulative_harm
    )
