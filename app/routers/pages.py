
import json
from pathlib import Path

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..auth import get_optional_user
from ..database import get_db
from ..models import Recommendation

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parents[2] / "templates"))



@router.get("/")
async def index(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    return templates.TemplateResponse(request=request, name="index.html", context={"user": user})


@router.get("/login")
async def login_page(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if user:
        return RedirectResponse("/dashboard", status_code=303)
    return templates.TemplateResponse(
        request=request, name="login.html", context={"user": None, "flash": request.session.pop("flash", None)}
    )


@router.get("/register")
async def register_page(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if user:
        return RedirectResponse("/dashboard", status_code=303)
    return templates.TemplateResponse(
        request=request, name="register.html", context={"user": None, "flash": request.session.pop("flash", None)}
    )


def require_user(request: Request, db: Session):
    user = get_optional_user(request, db)
    if not user:
        raise PermissionError
    return user


@router.get("/dashboard")
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    recent = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user.id)
        .order_by(Recommendation.created_at.desc())
        .limit(5)
        .all()
    )
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"user": user, "recent": recent})


@router.get("/planner/home")
async def home_planner(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request=request, name="home_planner.html", context={"user": user})


@router.get("/planner/party")
async def party_planner(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request=request, name="party_planner.html", context={"user": user})


@router.get("/planner/jewelry")
async def jewelry_planner(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse(request=request, name="jewelry_planner.html", context={"user": user})


@router.get("/history")
async def history(request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    items = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user.id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(request=request, name="history.html", context={"user": user, "items": items})


@router.get("/recommendations/{recommendation_id}")
async def recommendation_detail(recommendation_id: int, request: Request, db: Session = Depends(get_db)):
    user = get_optional_user(request, db)
    if not user:
        return RedirectResponse("/login", status_code=303)
    item = (
        db.query(Recommendation)
        .filter(Recommendation.id == recommendation_id, Recommendation.user_id == user.id)
        .first()
    )
    if not item:
        return RedirectResponse("/history", status_code=303)
    return templates.TemplateResponse(
        request=request,
        name="recommendations.html",
        context={"user": user, "item": item, "result": json.loads(item.result_json)},
    )
