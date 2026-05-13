"""User registration and login service."""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.security import hash_password, normalize_email, normalize_username, validate_email, validate_username, verify_password
from app.config import ENABLE_SIGNUP
from app.db.models import User


class AuthError(Exception):
    """Authentication or registration failed."""


def user_to_dto(user: User) -> dict[str, object]:
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": _iso(user.created_at),
        "last_login_at": _iso(user.last_login_at),
    }


def register_user(db: Session, *, email: str, username: str = "", password: str) -> User:
    if not ENABLE_SIGNUP:
        raise AuthError("当前服务未开放注册")
    normalized_email = normalize_email(email)
    normalized_username = normalize_username(username, normalized_email)
    if not validate_email(normalized_email):
        raise AuthError("邮箱格式不正确")
    if not validate_username(normalized_username):
        raise AuthError("用户名需为 2-40 位中文、字母、数字、下划线或短横线")
    if len(password or "") < 8:
        raise AuthError("密码长度至少 8 位")
    exists = db.scalar(select(User).where((User.email == normalized_email) | (User.username == normalized_username)))
    if exists:
        raise AuthError("邮箱或用户名已被注册")
    user_count = int(db.scalar(select(func.count(User.id))) or 0)
    user = User(
        email=normalized_email,
        username=normalized_username,
        password_hash=hash_password(password),
        role="admin" if user_count == 0 else "user",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, *, email_or_username: str, password: str) -> User:
    identity = str(email_or_username or "").strip()
    normalized_email = normalize_email(identity)
    user = db.scalar(select(User).where((User.email == normalized_email) | (User.username == identity)))
    if user is None or not user.is_active or not verify_password(password, user.password_hash):
        raise AuthError("邮箱/用户名或密码不正确")
    user.last_login_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: str) -> User | None:
    return db.get(User, user_id)


def _iso(value: object) -> str:
    return value.isoformat() if hasattr(value, "isoformat") else ""
