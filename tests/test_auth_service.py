"""
Unit tests for auth_service.
"""

import pytest
from finance_system.services.auth_service import hash_password, verify_password, create_access_token, decode_token


def test_hash_password():
    """Test password hashing."""
    password = "test123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)


def test_verify_password():
    """Test password verification."""
    password = "test123"
    hashed = hash_password(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrong", hashed)


def test_create_and_decode_token():
    """Test JWT token creation and decoding."""
    data = {"sub": "testuser"}
    token = create_access_token(data)
    decoded = decode_token(token)
    assert decoded["sub"] == "testuser"


def test_decode_invalid_token():
    """Test decoding invalid token raises error."""
    with pytest.raises(Exception):
        decode_token("invalid.token.here")