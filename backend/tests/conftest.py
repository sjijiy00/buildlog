import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def test_environment(tmp_path, monkeypatch):
    database_path = (tmp_path / "buildlog-test.sqlite3").as_posix()
    database_url = f"sqlite:///{database_path}"
    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.setenv("SECRET_KEY", "test-only-secret-key")
    monkeypatch.setenv("ENVIRONMENT", "test")

    from app.core.config import get_settings

    get_settings.cache_clear()
    yield database_url
    get_settings.cache_clear()


@pytest.fixture
def client(test_environment):
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def database_session(test_environment):
    from app import models  # noqa: F401
    from app.core.database import Base, create_database_engine

    test_engine = create_database_engine(test_environment)
    Base.metadata.create_all(test_engine)

    with Session(test_engine) as session:
        yield session

    Base.metadata.drop_all(test_engine)
    test_engine.dispose()
