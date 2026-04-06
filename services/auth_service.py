"""
Auth service: password hashing, JWT creation and decoding.

Note: Uses the `bcrypt` library directly instead of passlib because passlib's
bcrypt backend is not compatible with bcrypt >= 4.x / 5.x.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from config import settings

logger = logging.getLogger(__name__)


def hash_password(password: str) -> str:
    """Return the bcrypt hash of *password* as a UTF-8 string."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if *plain_password* matches *hashed_password*."""
    result = bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )
    if not result:
        logger.warning("Password verification failed")
    return result


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None,
) -> str:
    """
    Encode *data* into a signed JWT.

    If *expires_delta* is not supplied the default from config is used.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    to_encode["exp"] = expire
    token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    logger.info(f"Access token created for user: {data.get('sub', 'unknown')}")
    return token


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and verify *token*.

    Returns the payload dict on success.
    Raises ``jose.JWTError`` on failure (invalid / expired token).
    """
    try:
        payload: dict[str, Any] = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError:
        raise
