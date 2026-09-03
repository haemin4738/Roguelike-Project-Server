from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.auth import get_current_user
from app.schemas import AbilityLevelResponse, AbilityLevelUpdate, PlayerDataResponse, PlayerDataUpdate

router = APIRouter(prefix="/player", tags=["player"])


@router.get("/data", response_model=PlayerDataResponse)
def get_player_data(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return current_user.player_data


@router.put("/data", response_model=PlayerDataResponse)
def update_player_data(
    body: PlayerDataUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pd = current_user.player_data
    for field, value in body.model_dump(exclude_none=True).items():
        setattr(pd, field, value)
    db.commit()
    db.refresh(pd)
    return pd


@router.get("/abilities", response_model=list[AbilityLevelResponse])
def get_abilities(
    current_user: models.User = Depends(get_current_user),
):
    return current_user.ability_levels


@router.put("/abilities", response_model=list[AbilityLevelResponse])
def update_abilities(
    body: list[AbilityLevelUpdate],
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    existing = {a.ability_id: a for a in current_user.ability_levels}
    for item in body:
        if item.ability_id in existing:
            existing[item.ability_id].level = item.level
        else:
            db.add(models.AbilityLevel(user_id=current_user.id, ability_id=item.ability_id, level=item.level))
    db.commit()
    db.refresh(current_user)
    return current_user.ability_levels
