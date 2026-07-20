from backend.app.main import allowed_origins


def test_local_origins_are_allowed_by_default() -> None:
    assert "http://127.0.0.1:5173" in allowed_origins
    assert "http://localhost:5173" in allowed_origins


def test_allowed_origins_are_non_empty() -> None:
    assert allowed_origins
    assert all(origin.strip() for origin in allowed_origins)
