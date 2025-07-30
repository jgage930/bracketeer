import pytest
from jose import JWTError

from api.auth.encrypt import hash_password, encode_token, decode_token


def test_hash_password_is_consistent():
    password = "secure123"
    hashed1 = hash_password(password)
    hashed2 = hash_password(password)
    assert hashed1 == hashed2
    assert hashed1 != hash_password("different")


def test_hash_password_format():
    password = "test"
    hashed = hash_password(password)
    assert isinstance(hashed, str)
    assert len(hashed) == 64  # SHA256 hex digest length


def test_encode_token(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "mysecret")
    token = encode_token("alice")
    assert isinstance(token, str)


def test_decode_token(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "mysecret")
    token = encode_token("alice")
    payload = decode_token(token)
    assert payload["username"] == "alice"


def test_invalid_token_raises_error(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "mysecret")
    with pytest.raises(JWTError):
        decode_token("this.is.an.invalid.token")
