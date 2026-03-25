from fastapi import FastAPI
from database import engine
from models import User
import auth

User.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Users service running"}

app.include_router(auth.router, prefix="/auth")