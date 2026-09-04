from datetime import datetime, timezone
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=True, index=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    email_verified = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    player_data = relationship("PlayerData", back_populates="user", uselist=False)
    ability_levels = relationship("AbilityLevel", back_populates="user")


class PlayerData(Base):
    __tablename__ = "player_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    ap = Column(Integer, default=0)
    gold = Column(Integer, default=0)
    total_runs = Column(Integer, default=0)
    best_floor = Column(Integer, default=0)
    total_kills = Column(Integer, default=0)
    total_deaths = Column(Integer, default=0)

    user = relationship("User", back_populates="player_data")


class AbilityLevel(Base):
    __tablename__ = "ability_levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    ability_id = Column(String, nullable=False)
    level = Column(Integer, default=0)

    __table_args__ = (UniqueConstraint("user_id", "ability_id"),)

    user = relationship("User", back_populates="ability_levels")
