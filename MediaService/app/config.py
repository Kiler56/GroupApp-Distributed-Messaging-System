import os
from dotenv import load_dotenv

load_dotenv()

MEDIA_PORT = int(os.getenv("MEDIA_PORT", "8003"))
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,http://localhost:5500").split(",")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
METADATA_FILE = os.getenv("METADATA_FILE", "media_metadata.json")
