from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth_service.database import engine, Base, SessionLocal
from auth_service import auth
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield 

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def root():
    return {"message": "Auth service running"}