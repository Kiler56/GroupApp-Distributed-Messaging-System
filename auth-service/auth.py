from fastapi import APIRouter, HTTPException
from database import SessionLocal
from models import User
from schemas import UserCreate
from schemas import UserLogin
from security import hash_password
from security import verify_password
from jwt_handler import create_access_token
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.post("/register")
def register(user: UserCreate):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(user)
    db.commit()

    return {"message": "User created"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == form_data.username).first()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(form_data.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    access_token = create_access_token(
        data={"sub": existing_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    } 

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@router.get("/profile")
def profile(user: str = Depends(get_current_user)):
    return {"user": user}    