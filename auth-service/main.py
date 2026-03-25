from fastapi import FastAPI
from database import engine
from models import User
from fastapi.middleware.cors import CORSMiddleware
import auth

User.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Users service running"}

app.include_router(auth.router, prefix="/auth")