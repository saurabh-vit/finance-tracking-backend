"""
FastAPI dependencies:
  - get_db          → yields a SQLAlchemy Session
  - get_current_user → validates JWT and returns the User ORM object
  - require_role    → dependency factory that enforces role-based access
  - rate_limit_login → prevents brute-force attacks on login endpoint
"""

from collections import defaultdict
from time import time
from typing import Callable

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from finance_system.database import SessionLocal
from finance_system.models.user import User
from finance_system.services.auth_service import decode_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


# ---------------------------------------------------------------------------
# Rate Limiting for Login Protection
# ---------------------------------------------------------------------------

# In-memory storage for rate limiting (resets on server restart)
# In production, use Redis or similar persistent store
_login_attempts = defaultdict(list)

MAX_LOGIN_ATTEMPTS = 5  # Max attempts per minute
RATE_LIMIT_WINDOW = 60  # 1 minute window


def rate_limit_login(request: Request):
    """
    Rate limiting dependency for login endpoint to prevent brute-force attacks.

    Tracks attempts by client IP address. Allows max 5 attempts per minute.
    This is a simple in-memory implementation; in production, use Redis.

    Raises:
        429 – too many requests
    """
    client_ip = request.client.host
    current_time = time()

    # Clean old attempts outside the window
    _login_attempts[client_ip] = [
        timestamp for timestamp in _login_attempts[client_ip]
        if current_time - timestamp < RATE_LIMIT_WINDOW
    ]

    # Check if limit exceeded
    if len(_login_attempts[client_ip]) >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts, please try again later",
        )

    # Record this attempt
    _login_attempts[client_ip].append(current_time)


# ---------------------------------------------------------------------------
# DB session
# ---------------------------------------------------------------------------

def get_db():
    """Yield a database session and guarantee it is closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# DB session
# ---------------------------------------------------------------------------

def get_db():
    """Yield a database session and guarantee it is closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Current user
# ---------------------------------------------------------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """
    Decode the JWT bearer token and return the corresponding User.

    Raises:
        401 – token missing, invalid, or expired
        401 – user referenced in token no longer exists
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials. Please log in again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# ---------------------------------------------------------------------------
# Role guard
# ---------------------------------------------------------------------------

def require_role(*roles: str) -> Callable:
    """
    Dependency factory.  Use as:

        Depends(require_role("admin", "analyst"))

    Raises:
        403 – if the current user's role is not in *roles*
    """

    def _checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Access denied. Required role(s): {', '.join(roles)}. "
                    f"Your role: {current_user.role}. "
                    f"Only admin can perform this action."
                ),
            )
        return current_user

    return _checker
