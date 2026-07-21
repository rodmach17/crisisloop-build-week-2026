from backend.app.main import app
from backend.tests.client import ASGITestClient


client = ASGITestClient(app)


def _create_session():
    response = client.post("/session")
    assert response.status_code == 200
    return response.json()


def _advance_session(session, seconds):
    response = client.post(
        "/session/advance",
        json={
            "session": session,
            "seconds": seconds,
        },
    )
    assert response.status_code == 200
    return response.json()


def _apply_action(session, action):
    response = client.post(
        "/session/action",
        json={
            "session": session,
            "action": action,
        },
    )
    assert response.status_code == 200
    return response.json()


def test_compare_endpoint_detects_improvement() -> None:
    initial = _create_session()
    initial = _advance_session(initial, 180)

    replay_response = client.post(
        "/session/replay",
        json={
            "session": initial,
            "replay_from_seconds": 90,
        },
    )
    assert replay_response.status_code == 200
    replay = replay_response.json()

    replay = _apply_action(replay, "call_for_help")
    replay = _apply_action(replay, "start_iv_fluids")
    replay = _apply_action(replay, "activate_transfusion")

    compare_response = client.post(
        "/session/compare",
        json={
            "initial_session": initial,
            "replay_session": replay,
        },
    )

    assert compare_response.status_code == 200

    comparison = compare_response.json()

    assert comparison["outcome"] == "improved"
    assert comparison["score_delta"] > 0
    assert comparison["harm_reduction"] > 0
    assert len(comparison["corrected_omissions"]) == 3


def test_compare_endpoint_rejects_different_scenarios() -> None:
    initial = _create_session()
    replay = _create_session()

    replay["current_state"]["scenario_id"] = "different_scenario"

    compare_response = client.post(
        "/session/compare",
        json={
            "initial_session": initial,
            "replay_session": replay,
        },
    )

    assert compare_response.status_code == 400
    assert compare_response.json()["detail"] == (
        "Sessions from different scenarios cannot be compared."
    )
