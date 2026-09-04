from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.database import Base, engine
from app.routers import auth, player

Base.metadata.create_all(bind=engine)

# 기존 DB에 새 컬럼 추가 (IF NOT EXISTS — 재시작해도 안전)
with engine.connect() as conn:
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS email_verified BOOLEAN NOT NULL DEFAULT TRUE"))
    conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS verification_token VARCHAR"))
    conn.execute(text("ALTER TABLE users ALTER COLUMN username DROP NOT NULL"))
    conn.execute(text("ALTER TABLE users ALTER COLUMN email DROP NOT NULL"))
    conn.commit()

app = FastAPI(title="Roguelike API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(auth.router)
app.include_router(player.router)


@app.get("/health")
def health():
    return {"status": "ok"}
