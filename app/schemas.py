
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[A-Za-z0-9_.-]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    confirm_password: str = Field(min_length=8, max_length=128)


class HomeBudgetRequest(BaseModel):
    total_budget: float = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(default_factory=list)
    num_lights: int = Field(default=0, ge=0, le=100)
    num_fans: int = Field(default=0, ge=0, le=100)
    num_furniture: int = Field(default=0, ge=0, le=100)
    num_dining_tables: int = Field(default=0, ge=0, le=20)
    style: str = Field(default="modern", max_length=100)
    additional_requirements: str = Field(default="", max_length=1000)


class PartyBudgetRequest(BaseModel):
    total_budget: float = Field(gt=0, le=10_000_000)
    num_guests: int = Field(gt=0, le=10000)
    party_type: str = Field(min_length=2, max_length=100)
    venue_type: str = Field(default="hall", max_length=100)
    needs: list[str] = Field(default_factory=list)
    additional_requirements: str = Field(default="", max_length=1000)


class JewelryBudgetRequest(BaseModel):
    total_budget: float = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = Field(default="classic", max_length=100)
    preferences: str = Field(default="", max_length=1000)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RecommendationOut(BaseModel):
    id: int
    planner_type: str
    result: dict
    created_at: str
