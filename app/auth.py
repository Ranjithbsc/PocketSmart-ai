
from datetime import datetime, timedelta, timezone
from typing import Annotated

import base64
import hashlib
import hmac
import secrets
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy.orm import Session

from .config import get_settings
from .database import get_db
from .models import User

settings = get_settings()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)
TOKEN_EXPIRE_MINUTES = 60


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(settings.secret_key, salt="pocketsmart-auth")


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 310_000)
    return "pbkdf2_sha256$310000$" + base64.urlsafe_b64encode(salt).decode() + "$" + base64.urlsafe_b64encode(digest).decode()


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, rounds_text, salt_text, digest_text = password_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        rounds = int(rounds_text)
        salt = base64.urlsafe_b64decode(salt_text.encode())
        expected = base64.urlsafe_b64decode(digest_text.encode())
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, rounds)
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False


def create_access_token(username: str) -> str:
    return _serializer().dumps({"sub": username})


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def authenticate_user(db: Session, username: str, password: str) -> User | None:
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def user_from_token(token: str, db: Session) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = _serializer().loads(token, max_age=TOKEN_EXPIRE_MINUTES * 60)
        username = payload.get("sub")
        if not username:
            raise credentials_error
    except (BadSignature, SignatureExpired) as exc:
        raise credentials_error from exc

    user = get_user_by_username(db, username)
    if not user:
        raise credentials_error
    return user


def get_current_user(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    token: Annotated[str | None, Depends(oauth2_scheme)],
) -> User:
    session_username = request.session.get("username")
    if session_username:
        user = get_user_by_username(db, session_username)
        if user:
            return user

    if token:
        return user_from_token(token, db)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
    )


def get_optional_user(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> User | None:
    username = request.session.get("username")
    if not username:
        return None
    return get_user_by_username(db, username)


def require_page_user(request: Request, db: Session) -> User:
    username = request.session.get("username")
    if not username:
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    user = get_user_by_username(db, username)
    if not user:
        request.session.clear()
        raise HTTPException(status_code=303, headers={"Location": "/login"})
    return user
