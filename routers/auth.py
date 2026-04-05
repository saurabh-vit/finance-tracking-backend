"""
Auth router: user registration and login.

Security Features:
- Rate limiting on login to prevent brute-force attacks (via dependency)
- Environment-based configuration for sensitive values
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from finance_system.dependencies import get_db, rate_limit_login
from finance_system.models.user import User
from finance_system.schemas.user import Token, UserCreate, UserResponse
from finance_system.services.auth_service import (
    create_access_token,
    hash_password,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
def register(user_in: UserCreate, db: Session = Depends(get_db)) -> User:
    """
    Create a new user account with role **viewer**.

    - **username**: 3+ chars, alphanumeric + underscore only
    - **email**: valid email format
    - **password**: minimum 6 characters
    """
    # Check uniqueness
    if db.query(User).filter(User.username == user_in.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{user_in.username}' is already taken.",
        )
    if db.query(User).filter(User.email == user_in.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{user_in.email}' is already registered.",
        )

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role="viewer",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post(
    "/login",
    response_model=Token,
    summary="Login and obtain a JWT access token",
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    rate_limited: None = Depends(rate_limit_login),  # Rate limiting dependency
) -> Token:
    """
    Authenticate with **username** and **password** (form-encoded).

    Returns a JWT bearer token valid for 30 minutes (configurable via .env).

    Rate limited: Max 5 attempts per minute per IP to prevent brute-force attacks.
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")
