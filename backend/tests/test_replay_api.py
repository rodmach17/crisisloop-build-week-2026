from backend.app.main import app
from backend.tests.client import ASGITestClient


client = ASGITestClient(app)


def test_replay_endpoint_creates_new_session_at_checkpoint() -> None:
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

    source_session = advance_response.json()

    replay_response = client.post(
        "/session/replay",
        json={
            "session": source_session,
            "replay_from_seconds": 90,
        },
    )

    assert replay_response.status_code == 200

    replay = replay_response.json()

    assert replay["session_id"] != source_session["session_id"]
    assert replay["current_state"]["elapsed_seconds"] == 90
    assert len(replay["timeline"]) == 1
    assert replay["timeline"][0]["event_type"] == "replay_checkpoint"


def test_replay_endpoint_rejects_future_checkpoint() -> None:
    session_response = client.post("/session")
    session = session_response.json()

    replay_response = client.post(
        "/session/replay",
        json={
            "session": session,
            "replay_from_seconds": 90,
        },
    )

    assert replay_response.status_code == 400
    assert replay_response.json()["detail"] == (
        "Replay time cannot exceed the source session elapsed time."
    )
