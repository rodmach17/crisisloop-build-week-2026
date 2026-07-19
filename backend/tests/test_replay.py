import pytest

from backend.app.engine.session import (
    advance_session,
    create_replay_session,
    create_simulation_session,
)


def _build_source_session_at_120_seconds():
    session = create_simulation_session()

    for _ in range(4):
        session = advance_session(session, 30)

    return session


def test_replay_creates_new_session_at_requested_checkpoint() -> None:
    source = _build_source_session_at_120_seconds()

    replay = create_replay_session(
        source_session=source,
        replay_from_seconds=90,
    )

    assert replay.session_id != source.session_id
    assert replay.current_state.elapsed_seconds == 90
    assert replay.current_state.estimated_blood_loss_ml == 1155
    assert replay.current_state.vital_signs.heart_rate == 117
    assert replay.current_state.vital_signs.systolic_bp == 96
    assert replay.current_state.cumulative_harm == 17


def test_replay_has_clean_timeline_with_checkpoint_only() -> None:
    source = _build_source_session_at_120_seconds()

    replay = create_replay_session(
        source_session=source,
        replay_from_seconds=90,
    )

    assert len(replay.timeline) == 1
    assert replay.timeline[0].event_type == "replay_checkpoint"
    assert replay.timeline[0].elapsed_seconds == 90
    assert replay.timeline[0].action is None


def test_replay_checkpoint_matches_original_deterministic_state() -> None:
    source = create_simulation_session()
    source = advance_session(source, 30)
    source = advance_session(source, 30)
    source_at_90 = advance_session(source, 30)

    replay = create_replay_session(
        source_session=advance_session(source_at_90, 30),
        replay_from_seconds=90,
    )

    assert replay.current_state == source_at_90.current_state


def test_replay_rejects_future_checkpoint() -> None:
    source = _build_source_session_at_120_seconds()

    with pytest.raises(ValueError):
        create_replay_session(
            source_session=source,
            replay_from_seconds=150,
        )


def test_replay_from_zero_returns_fresh_session() -> None:
    source = _build_source_session_at_120_seconds()

    replay = create_replay_session(
        source_session=source,
        replay_from_seconds=0,
    )

    assert replay.current_state.elapsed_seconds == 0
    assert replay.timeline == []
