import uuid
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas import MessageResponse, Token, UserCreate
from app.auth import hash_password, verify_password, create_access_token
from app.email_utils import send_verification_email

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=MessageResponse)
def register(body: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == body.email).first():
        raise HTTPException(status_code=400, detail="이미 가입된 이메일입니다.")

    token = str(uuid.uuid4())
    user = models.User(
        email=body.email,
        hashed_password=hash_password(body.password),
        email_verified=False,
        verification_token=token,
    )
    db.add(user)
    db.flush()
    db.add(models.PlayerData(user_id=user.id))
    db.commit()

    background_tasks.add_task(send_verification_email, body.email, token)
    return MessageResponse(message="가입 완료! 이메일을 확인해 인증을 완료해주세요.")


@router.get("/verify/{token}", response_class=HTMLResponse)
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.verification_token == token).first()
    if not user:
        return HTMLResponse("<h2>유효하지 않은 인증 링크입니다.</h2>", status_code=400)
    if user.email_verified:
        return HTMLResponse("<h2>이미 인증된 계정입니다.</h2>")
    user.email_verified = True
    user.verification_token = None
    db.commit()
    return HTMLResponse("<h2>이메일 인증 완료! 게임으로 돌아가서 로그인해주세요.</h2>")


@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    if not user.email_verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="이메일 인증이 필요합니다.")
    return Token(access_token=create_access_token({"sub": user.email}))
