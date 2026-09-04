import pytest
from app.security.auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)


def test_password_hashing():
    password = "testpassword123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_access_token():
    token = create_access_token("user123")
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["type"] == "access"


def test_refresh_token():
    token = create_refresh_token("user123")
    payload = decode_token(token)
    assert payload is not None
    assert payload["sub"] == "user123"
    assert payload["type"] == "refresh"


def test_invalid_token():
    payload = decode_token("invalidtoken")
    assert payload is None
