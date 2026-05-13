import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
METADATA_FILE = os.getenv("METADATA_FILE", "media_metadata.json")

os.makedirs(UPLOAD_DIR, exist_ok=True)

import uuid
import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

def load_metadata():
    if os.path.exists(METADATA_FILE):
        try:
            with open(METADATA_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_metadata(data):
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f)

MEDIA_DB = load_metadata()

@router.post("/media/upload")
async def upload_image(file: UploadFile = File(...), expected_views: int = 1):
    media_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, media_id)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    MEDIA_DB[media_id] = {
        "path": file_path,
        "viewed_by": [],
        "expected_views": int(expected_views),
        "mime_type": file.content_type or "image/jpeg"
    }
    save_metadata(MEDIA_DB)

    return {"media_id": media_id}


@router.get("/media/{media_id}")
async def get_image(media_id: str, user_id: str):
    global MEDIA_DB
    media = MEDIA_DB.get(media_id)

    if not media:
        raise HTTPException(status_code=404, detail="El archivo no existe o ya fue eliminado")

    u_id = str(user_id)

    if u_id in media["viewed_by"]:
        raise HTTPException(status_code=403, detail="Ya viste esta imagen una vez")

    if not os.path.exists(media["path"]):
        del MEDIA_DB[media_id]
        save_metadata(MEDIA_DB)
        raise HTTPException(status_code=404, detail="Archivo físico no encontrado")

    media["viewed_by"].append(u_id)
    
    response = FileResponse(media["path"], media_type=media["mime_type"])

    if len(media["viewed_by"]) >= media["expected_views"]:
        save_metadata(MEDIA_DB)
    else:
        save_metadata(MEDIA_DB)

    return response

