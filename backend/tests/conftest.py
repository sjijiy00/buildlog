import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_environment(tmp_path, monkeypatch):
    database_path = (tmp_path / "buildlog-test.sqlite3").as_posix()
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{database_path}")
    monkeypatch.setenv("SECRET_KEY", "test-only-secret-key")
    monkeypatch.setenv("ENVIRONMENT", "test")

    from app.core.config import get_settings

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def client(test_environment):
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
