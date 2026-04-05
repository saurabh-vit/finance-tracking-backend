"""
Pydantic schemas for User requests and responses.
"""

import re
from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict


_USERNAME_RE = re.compile(r"^[a-zA-Z0-9_]{3,}$")


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = v.strip()
        if not _USERNAME_RE.match(v):
            raise ValueError(
                "Username must be at least 3 characters and contain only "
                "letters, digits, or underscores."
            )
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters long.")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "securepass123"
            }
        }
    )


class UserLogin(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "admin_user",
                "password": "admin123"
            }
        }
    )


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "username": "admin_user",
                "email": "admin@finance.io",
                "role": "admin"
            }
        }
    )


class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }
    )


class UserUpdate(BaseModel):
    role: Optional[str] = None

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("viewer", "analyst", "admin"):
            raise ValueError("Role must be 'viewer', 'analyst', or 'admin'.")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role": "analyst"
            }
        }
    )
