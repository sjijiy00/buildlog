import secrets

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import Base, create_database_engine
from app.core.security import hash_password, verify_password
from app.models.user import User


def make_user(email: str, nickname: str) -> tuple[User, str]:
    password = secrets.token_urlsafe(16)
    return (
        User(
            email=email,
            nickname=nickname,
            password_hash=hash_password(password),
        ),
        password,
    )


def test_user_is_normalized_and_password_is_hashed(database_session):
    user, password = make_user(" Test@Mail.com ", " Coder_한글 ")
    database_session.add(user)
    database_session.commit()
    database_session.refresh(user)

    assert user.email == "test@mail.com"
    assert user.nickname == "Coder_한글"
    assert user.nickname_normalized == "coder_한글"
    assert user.password_hash != password
    assert password not in user.password_hash
    assert verify_password(password, user.password_hash)
    assert not verify_password(secrets.token_urlsafe(16), user.password_hash)
    assert user.is_admin is False
    assert user.created_at is not None


def test_email_is_unique_without_case_sensitivity(database_session):
    first, _ = make_user("Test@Mail.com", "first_user")
    second, _ = make_user("test@mail.com", "second_user")
    database_session.add(first)
    database_session.commit()

    database_session.add(second)
    with pytest.raises(IntegrityError):
        database_session.commit()


def test_nickname_is_unique_without_case_sensitivity(database_session):
    first, _ = make_user("first@example.com", "Coder")
    second, _ = make_user("second@example.com", "coder")
    database_session.add(first)
    database_session.commit()

    database_session.add(second)
    with pytest.raises(IntegrityError):
        database_session.commit()


@pytest.mark.parametrize(
    "nickname",
    ["", "a", "a" * 21, "has space", "사용자!"],
)
def test_nickname_rejects_invalid_values(nickname):
    with pytest.raises(ValueError):
        User(nickname=nickname)


def test_user_remains_after_database_reconnect(test_environment):
    first_engine = create_database_engine(test_environment)
    Base.metadata.create_all(first_engine)
    user, _ = make_user("saved@example.com", "saved_user")

    with Session(first_engine) as session:
        session.add(user)
        session.commit()
    first_engine.dispose()

    second_engine = create_database_engine(test_environment)
    with Session(second_engine) as session:
        saved_user = session.scalar(
            select(User).where(User.email == "saved@example.com")
        )

    second_engine.dispose()
    assert saved_user is not None
    assert saved_user.nickname == "saved_user"
