"""FastAPI authentication dependencies."""
from __future__ import annotations

from typing import Annotated

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.security import decode_access_token
from app.auth.service import get_user_by_id
from app.config import AUTH_COOKIE_NAME, AUTH_REQUIRED
from app.db.models import User
from app.db.session import get_db


def get_optional_current_user(
    db: Annotated[Session, Depends(get_db)],
    session_cookie: Annotated[str | None, Cookie(alias=AUTH_COOKIE_NAME)] = None,
) -> User | None:
    if not session_cookie:
        return None
    payload = decode_access_token(session_cookie)
    if not payload:
        return None
    user_id = str(payload.get("sub") or "")
    if not user_id:
        return None
    user = get_user_by_id(db, user_id)
    if user is None or not user.is_active:
        return None
    return user


def require_current_user(user: Annotated[User | None, Depends(get_optional_current_user)]) -> User:
    if user is None:
        raise HTTPException(status_code=401, detail="请先登录")
    return user


def current_user_or_legacy(user: Annotated[User | None, Depends(get_optional_current_user)]) -> User | None:
    if user is None and AUTH_REQUIRED:
        raise HTTPException(status_code=401, detail="请先登录")
    return user
