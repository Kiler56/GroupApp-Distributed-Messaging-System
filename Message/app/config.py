import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "messages_db")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8000")
GRUPOS_SERVICE_URL = os.getenv("GRUPOS_SERVICE_URL", "http://localhost:8002")
RABBITMQ_URL = os.getenv("RABBITMQ_URL", "localhost")
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5500").split(",")
