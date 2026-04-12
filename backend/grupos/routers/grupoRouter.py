from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from backend.core.database import get_db

from schemas.grupoSchema import (
    GrupoCreate,
    GrupoUpdate,
    GrupoResponse
)
from services.grupoService import GrupoService

router = APIRouter(prefix="/grupos", tags=["Grupos"])
service = GrupoService()

# MOCK (reemplazar luego con JWT real)
def get_current_user():
    return "user-123"

# Get all grupos
@router.get("/", response_model=List[GrupoResponse])
def get_grupos(db: Session = Depends(get_db)):
    return service.get_grupos(db)

# Get grupo por id
@router.get("/{id_grupo}", response_model=GrupoResponse)
def get_grupo(id_grupo: str, db: Session = Depends(get_db)):
    return service.get_grupo(db, id_grupo)

# Crear grupo
@router.post("/", response_model=GrupoResponse, status_code=status.HTTP_201_CREATED)
def create_grupo(
    grupo: GrupoCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return service.create_grupo(db, grupo, user_id)

# Update grupo
@router.put("/{id_grupo}", response_model=GrupoResponse)
def update_grupo(
    id_grupo: str,
    grupo: GrupoUpdate,
    db: Session = Depends(get_db)
):
    return service.update_grupo(db, id_grupo, grupo)

# Delete grupo
@router.delete("/{id_grupo}", status_code=status.HTTP_204_NO_CONTENT)
def delete_grupo(
    id_grupo: str,
    db: Session = Depends(get_db)
):
    service.delete_grupo(db, id_grupo)
    return None