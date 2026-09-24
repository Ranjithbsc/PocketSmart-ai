
from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..auth import authenticate_user, create_access_token, get_user_by_username, hash_password
from ..database import get_db
from ..models import User
from ..schemas import RegisterRequest, TokenResponse

router = APIRouter()


@router.post("/register")
async def register_api(payload: RegisterRequest, db: Annotated[Session, Depends(get_db)]):
    if payload.password != payload.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    if get_user_by_username(db, payload.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")

    user = User(
        username=payload.username,
        email=str(payload.email).lower(),
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "Account created", "username": user.username}


@router.post("/register/form")
async def register_form(
    request: Request,
    username: Annotated[str, Form(...)],
    email: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    confirm_password: Annotated[str, Form(...)],
    db: Annotated[Session, Depends(get_db)],
):
    if password != confirm_password:
        request.session["flash"] = "Passwords do not match."
        return RedirectResponse("/register", status_code=303)
    if get_user_by_username(db, username) or db.query(User).filter(User.email == email.lower()).first():
        request.session["flash"] = "Username or email already exists."
        return RedirectResponse("/register", status_code=303)
    if len(password) < 8:
        request.session["flash"] = "Password must be at least 8 characters."
        return RedirectResponse("/register", status_code=303)

    user = User(username=username, email=email.lower(), password_hash=hash_password(password))
    db.add(user)
    db.commit()
    request.session["username"] = username
    return RedirectResponse("/dashboard", status_code=303)


@router.post("/login/form")
async def login_form(
    request: Request,
    username: Annotated[str, Form(...)],
    password: Annotated[str, Form(...)],
    db: Annotated[Session, Depends(get_db)],
):
    user = authenticate_user(db, username, password)
    if not user:
        request.session["flash"] = "Invalid username or password."
        return RedirectResponse("/login", status_code=303)
    request.session["username"] = user.username
    return RedirectResponse("/dashboard", status_code=303)


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


@router.post("/token", response_model=TokenResponse)
async def token(form: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = authenticate_user(db, form.username, form.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return TokenResponse(access_token=create_access_token(user.username))
