
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import init_db
from .routers import auth, pages, planners


settings = get_settings()
BASE_DIR = Path(__file__).resolve().parents[1]


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    description="AI-powered budget planning and recommendation assistant.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.secret_key,
    https_only=settings.session_https_only,
    same_site="lax",
    max_age=60 * 60 * 24 * 7,
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(planners.router)


@app.get("/health")
async def health():
    return {"status": "ok", "service": settings.app_name}


@app.get("/startup")
async def startup_status():
    return {
        "status": "ready",
        "gemini_configured": bool(settings.gemini_api_key),
        "model": settings.gemini_model,
    }
