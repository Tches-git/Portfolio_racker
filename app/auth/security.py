"""Password hashing and signed session tokens.

The project lists passlib/python-jose as deployment dependencies, but this
module intentionally uses stdlib primitives so local tests keep working before
new dependencies are installed.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import time
from secrets import token_urlsafe

from app.config import AUTH_SECRET, AUTH_TOKEN_TTL_SECONDS

PASSWORD_ITERATIONS = 260_000
TOKEN_ALGORITHM = "HS256"
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_\-\u4e00-\u9fff]{2,40}$")


def normalize_email(email: str) -> str:
    return str(email or "").strip().lower()


def normalize_username(username: str, email: str = "") -> str:
    raw = str(username or "").strip()
    if raw:
        return raw
    return normalize_email(email).split("@", 1)[0][:40] or "user"


def validate_email(email: str) -> bool:
    return bool(EMAIL_RE.match(normalize_email(email)))


def validate_username(username: str) -> bool:
    return bool(USERNAME_RE.match(str(username or "").strip()))


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PASSWORD_ITERATIONS)
    return "pbkdf2_sha256${}${}${}".format(
        PASSWORD_ITERATIONS,
        base64.urlsafe_b64encode(salt).decode("ascii"),
        base64.urlsafe_b64encode(digest).decode("ascii"),
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations, salt_b64, digest_b64 = password_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        salt = base64.urlsafe_b64decode(salt_b64.encode("ascii"))
        expected = base64.urlsafe_b64decode(digest_b64.encode("ascii"))
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations))
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def create_access_token(*, user_id: str, email: str, ttl_seconds: int = AUTH_TOKEN_TTL_SECONDS) -> str:
    now = int(time.time())
    header = {"alg": TOKEN_ALGORITHM, "typ": "JWT"}
    payload = {"sub": user_id, "email": email, "iat": now, "exp": now + ttl_seconds, "jti": token_urlsafe(8)}
    signing_input = f"{_b64_json(header)}.{_b64_json(payload)}"
    signature = _b64_bytes(hmac.new(_secret(), signing_input.encode("utf-8"), hashlib.sha256).digest())
    return f"{signing_input}.{signature}"


def decode_access_token(token: str) -> dict[str, object] | None:
    try:
        header_b64, payload_b64, signature = token.split(".", 2)
        signing_input = f"{header_b64}.{payload_b64}"
        expected = _b64_bytes(hmac.new(_secret(), signing_input.encode("utf-8"), hashlib.sha256).digest())
        if not hmac.compare_digest(signature, expected):
            return None
        payload = json.loads(_b64_decode(payload_b64))
        if int(payload.get("exp", 0)) < int(time.time()):
            return None
        return payload
    except Exception:
        return None


def _secret() -> bytes:
    return AUTH_SECRET.encode("utf-8")


def _b64_json(payload: dict[str, object]) -> str:
    return _b64_bytes(json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def _b64_bytes(payload: bytes) -> str:
    return base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")


def _b64_decode(payload: str) -> bytes:
    padding = "=" * (-len(payload) % 4)
    return base64.urlsafe_b64decode((payload + padding).encode("ascii"))
