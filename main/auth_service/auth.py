from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth_service.database import SessionLocal
from auth_service.models import User
from auth_service.schemas import UserCreate
from auth_service.security import hash_password, verify_password
from auth_service.jwt_handler import create_access_token

from auth_service.dependencies import get_current_user

router = APIRouter()


# ========================
# REGISTER
# ========================
@router.post("/register")
def register(user: UserCreate):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}


# ========================
# LOGIN
# ========================
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == form_data.username).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token(
        data={
            "user_id": existing_user.id_usuario, 
            "sub": existing_user.email
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ========================
# PROFILE (protegido con JWT)
# ========================
@router.get("/profile")
def profile(user_id: int = Depends(get_current_user)):
    return {"user_id": user_id}

@router.get("/verify/{user_id}")
def verify_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id_usuario == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id_usuario, "username": user.username}