import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "grupos_db")

DATABASE_URL = os.getenv("DATABASE_URL", f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8000")
ROLES_SERVICE_HOST = os.getenv("ROLES_SERVICE_HOST", "localhost")
ROLES_SERVICE_PORT = os.getenv("ROLES_SERVICE_PORT", "50051")
AUTH_SERVICE_HOST = os.getenv("AUTH_SERVICE_HOST", "localhost")
AUTH_GRPC_PORT = os.getenv("AUTH_GRPC_PORT", "50052")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5500").split(",")
