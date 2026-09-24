
import json
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..config import get_settings
from ..database import get_db
from ..models import Recommendation, User
from ..schemas import HomeBudgetRequest, JewelryBudgetRequest, PartyBudgetRequest
from ..services.recommendation_service import RecommendationService

router = APIRouter(prefix="/api")
settings = get_settings()
service = RecommendationService()
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}


def save_history(db: Session, user: User, planner_type: str, payload: dict, result: dict) -> Recommendation:
    row = Recommendation(
        user_id=user.id,
        planner_type=planner_type,
        input_json=json.dumps(payload, ensure_ascii=False),
        result_json=json.dumps(result, ensure_ascii=False),
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


@router.post("/generate-home")
async def generate_home(
    payload: HomeBudgetRequest,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    result = service.home(payload.model_dump())
    row = save_history(db, user, "home", payload.model_dump(), result)
    return {"id": row.id, "planner_type": "home", "result": result}


@router.post("/generate-party")
async def generate_party(
    payload: PartyBudgetRequest,
    request: Request,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    result = service.party(payload.model_dump())
    row = save_history(db, user, "party", payload.model_dump(), result)
    return {"id": row.id, "planner_type": "party", "result": result}


@router.post("/generate-jewelry")
async def generate_jewelry(
    total_budget: Annotated[float, Form(gt=0)],
    occasion: Annotated[str, Form(min_length=2)],
    style: Annotated[str, Form()] = "classic",
    preferences: Annotated[str, Form()] = "",
    outfit_image: Annotated[UploadFile | None, File()] = None,
    db: Annotated[Session, Depends(get_db)] = None,
    user: Annotated[User, Depends(get_current_user)] = None,
):
    if outfit_image and outfit_image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Only JPEG, PNG, and WebP images are supported")

    image_bytes = None
    if outfit_image:
        image_bytes = await outfit_image.read()
        if len(image_bytes) > settings.max_upload_mb * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"Image must be {settings.max_upload_mb} MB or smaller")

    payload = {
        "total_budget": total_budget,
        "occasion": occasion,
        "style": style,
        "preferences": preferences,
    }
    result = service.jewelry(
        payload,
        image_bytes=image_bytes,
        mime_type=outfit_image.content_type if outfit_image else None,
    )
    row = save_history(db, user, "jewelry", payload, result)
    return {"id": row.id, "planner_type": "jewelry", "result": result}


@router.get("/history")
async def api_history(
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    rows = (
        db.query(Recommendation)
        .filter(Recommendation.user_id == user.id)
        .order_by(Recommendation.created_at.desc())
        .all()
    )
    return [
        {
            "id": row.id,
            "planner_type": row.planner_type,
            "created_at": row.created_at.isoformat(),
        }
        for row in rows
    ]


@router.get("/session-info")
async def session_info(user: Annotated[User, Depends(get_current_user)]):
    return {"logged_in": True, "username": user.username, "user_id": user.id}


@router.get("/recommendations/{recommendation_id}")
async def recommendation_json(
    recommendation_id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    row = (
        db.query(Recommendation)
        .filter(Recommendation.id == recommendation_id, Recommendation.user_id == user.id)
        .first()
    )
    if not row:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return {
        "id": row.id,
        "planner_type": row.planner_type,
        "input": json.loads(row.input_json),
        "result": json.loads(row.result_json),
    }
