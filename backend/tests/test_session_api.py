from backend.app.main import app
from backend.tests.client import ASGITestClient

client = ASGITestClient(app)


def test_create_session_endpoint() -> None:
    response = client.post("/session")

    assert response.status_code == 200
    data = response.json()

    assert data["current_state"]["elapsed_seconds"] == 0
    assert data["timeline"] == []
    assert data["session_id"]


def test_full_session_flow_and_score() -> None:
    session = client.post("/session").json()

    response = client.post(
        "/session/advance",
        json={
            "session": session,
            "seconds": 30,
        },
    )
    assert response.status_code == 200
    session = response.json()

    response = client.post(
        "/session/action",
        json={
            "session": session,
            "action": "call_for_help",
        },
    )
    assert response.status_code == 200
    session = response.json()

    response = client.post(
        "/session/advance",
        json={
            "session": session,
            "seconds": 20,
        },
    )
    session = response.json()

    response = client.post(
        "/session/action",
        json={
            "session": session,
            "action": "start_iv_fluids",
        },
    )
    session = response.json()

    response = client.post(
        "/session/advance",
        json={
            "session": session,
            "seconds": 20,
        },
    )
    session = response.json()

    response = client.post(
        "/session/action",
        json={
            "session": session,
            "action": "activate_transfusion",
        },
    )
    session = response.json()

    response = client.post(
        "/session/score",
        json=session,
    )

    assert response.status_code == 200
    data = response.json()

    assert data["score"]["total_score"] >= 80
    assert data["score"]["critical_omissions"] == []
    assert data["score"]["critical_decision"] is None
    assert len(data["session"]["timeline"]) == 6
