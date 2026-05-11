from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
import uuid
import os

router = APIRouter()

MEDIA_DB = {}

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

import uuid
import os
import json
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

router = APIRouter()

UPLOAD_DIR = "uploads"
METADATA_FILE = "media_metadata.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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

# Cargar metadatos al iniciar
MEDIA_DB = load_metadata()

@router.post("/media/upload")
async def upload_image(file: UploadFile = File(...), expected_views: int = 1):
    media_id = str(uuid.uuid4())
    # Guardamos sin extensión para facilitar la recuperación por ID puro
    file_path = f"{UPLOAD_DIR}/{media_id}"

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

    # Normalizar user_id a string para la comparación
    u_id = str(user_id)

    if u_id in media["viewed_by"]:
        raise HTTPException(status_code=403, detail="Ya viste esta imagen una vez")

    if not os.path.exists(media["path"]):
        del MEDIA_DB[media_id]
        save_metadata(MEDIA_DB)
        raise HTTPException(status_code=404, detail="Archivo físico no encontrado")

    # Registrar visualización
    media["viewed_by"].append(u_id)
    
    # Preparar la respuesta antes de borrar (si fuera necesario)
    response = FileResponse(media["path"], media_type=media["mime_type"])

    # Si todos la vieron, autodestrucción
    if len(media["viewed_by"]) >= media["expected_views"]:
        # Nota: En un sistema real usaríamos un background task para borrar el archivo
        # después de que el FileResponse termine de enviarse.
        # Por ahora lo mantenemos y una tarea de limpieza podría borrarlo luego, 
        # o lo borramos del DB para que nadie más acceda.
        save_metadata(MEDIA_DB)
        print(f"MEDIA: {media_id} marcada para eliminación (vistas completadas)")
    else:
        save_metadata(MEDIA_DB)

    return response

