import re
from datetime import UTC, datetime

from sqlalchemy import Boolean, CheckConstraint, DateTime, Integer, String, UniqueConstraint, false, func
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.core.database import Base


NICKNAME_PATTERN = re.compile(r"^[가-힣A-Za-z0-9_]+$")


def utc_now() -> datetime:
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "length(nickname) BETWEEN 2 AND 20",
            name="ck_users_nickname_length",
        ),
        UniqueConstraint("email", name="uq_users_email"),
        UniqueConstraint(
            "nickname_normalized",
            name="uq_users_nickname_normalized",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(320), nullable=False)
    nickname: Mapped[str] = mapped_column(String(20), nullable=False)
    nickname_normalized: Mapped[str] = mapped_column(String(20), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=false(),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=utc_now,
        server_default=func.now(),
        nullable=False,
    )

    @validates("email")
    def normalize_email(self, _key: str, value: str) -> str:
        return value.strip().lower()

    @validates("nickname")
    def validate_nickname(self, _key: str, value: str) -> str:
        nickname = value.strip()
        if not 2 <= len(nickname) <= 20:
            raise ValueError("닉네임은 2~20자여야 합니다.")
        if NICKNAME_PATTERN.fullmatch(nickname) is None:
            raise ValueError("닉네임에는 한글, 영문, 숫자, 밑줄만 사용할 수 있습니다.")

        self.nickname_normalized = nickname.lower()
        return nickname
