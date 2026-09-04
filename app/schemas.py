from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str


class PlayerDataResponse(BaseModel):
    ap: int
    gold: int
    total_runs: int
    best_floor: int
    total_kills: int
    total_deaths: int

    model_config = {"from_attributes": True}


class PlayerDataUpdate(BaseModel):
    ap: Optional[int] = None
    gold: Optional[int] = None
    total_runs: Optional[int] = None
    best_floor: Optional[int] = None
    total_kills: Optional[int] = None
    total_deaths: Optional[int] = None


class AbilityLevelResponse(BaseModel):
    ability_id: str
    level: int

    model_config = {"from_attributes": True}


class AbilityLevelUpdate(BaseModel):
    ability_id: str
    level: int
