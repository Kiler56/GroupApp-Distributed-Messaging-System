from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import uuid
import os

router = APIRouter()

MEDIA_DB = {}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/media/upload")
async def upload_image(file: UploadFile = File(...)):
    media_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{media_id}.jpg"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    MEDIA_DB[media_id] = {
        "path": file_path,
        "viewed": False
    }

    return {
        "media_id": media_id
    }


@router.get("/media/{media_id}")
def get_image(media_id: str):
    media = MEDIA_DB.get(media_id)

    if not media:
        raise HTTPException(status_code=404, detail="No existe")

    if media["viewed"]:
        raise HTTPException(status_code=403, detail="Imagen ya fue vista")

    media["viewed"] = True

    return FileResponse(media["path"], media_type="image/jpeg")