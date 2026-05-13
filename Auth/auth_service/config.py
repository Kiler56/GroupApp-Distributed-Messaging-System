import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
AUTH_GRPC_PORT = os.getenv("AUTH_GRPC_PORT", "50052")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")
