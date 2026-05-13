from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from fastapi import HTTPException, Request
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.server import app
from app.auth.dependencies import require_current_user
from app.db.base import Base
from app.db.models import User
from app.db.session import get_db


def _in_memory_session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, future=True, expire_on_commit=False)


@contextmanager
def database_client() -> Iterator[tuple[TestClient, sessionmaker]]:
    Session = _in_memory_session_factory()

    def override_db():
        session = Session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_db
    try:
        yield TestClient(app), Session
    finally:
        app.dependency_overrides.clear()


@contextmanager
def authenticated_client(*, role: str = "admin", username: str = "alice", user_id: str = "user-test") -> Iterator[tuple[TestClient, User]]:
    Session = _in_memory_session_factory()
    with Session() as db:
        user = User(id=user_id, email=f"{username}@example.com", username=username, password_hash="x", role=role)
        db.add(user)
        db.commit()

    def override_db():
        session = Session()
        try:
            yield session
        finally:
            session.close()

    def override_user() -> User:
        with Session() as db:
            return db.get(User, user_id) or user

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[require_current_user] = override_user
    try:
        yield TestClient(app), user
    finally:
        app.dependency_overrides.clear()


@contextmanager
def multi_user_client() -> Iterator[tuple[TestClient, dict[str, User], sessionmaker]]:
    Session = _in_memory_session_factory()
    seed_users = [
        User(id="user-alice", email="alice@example.com", username="alice", password_hash="x", role="user"),
        User(id="user-bob", email="bob@example.com", username="bob", password_hash="x", role="user"),
        User(id="user-admin", email="admin@example.com", username="admin", password_hash="x", role="admin"),
    ]
    with Session() as db:
        db.add_all(seed_users)
        db.commit()

    def override_db():
        session = Session()
        try:
            yield session
        finally:
            session.close()

    def override_user(request: Request) -> User:
        username = request.headers.get("X-Test-User", "alice")
        with Session() as db:
            user = db.scalar(select(User).where(User.username == username))
            if user is None:
                raise HTTPException(status_code=401, detail="请先登录")
            return user

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[require_current_user] = override_user
    try:
        users = {user.username: user for user in seed_users}
        yield TestClient(app), users, Session
    finally:
        app.dependency_overrides.clear()
