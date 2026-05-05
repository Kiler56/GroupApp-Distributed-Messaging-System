from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from Grupos.dependencies import get_current_user
from Grupos.database import get_db

from Grupos.schemas.grupoSchema import (
    GrupoCreate,
    GrupoUpdate,
    GrupoResponse
)
from Grupos.services.grupoService import GrupoService

router = APIRouter(tags=["Grupos"])
service = GrupoService()

# Get all grupos
@router.get("/groups", response_model=List[GrupoResponse])
def get_grupos(db: Session = Depends(get_db)):
    return service.get_grupos(db)

# Get grupo por id
@router.get("/groups/{id_grupo}", response_model=GrupoResponse)
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
@router.put("/{id_grupo}")
def update_grupo(
    id_grupo: str,
    grupo: GrupoUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return service.update_grupo(db, id_grupo, grupo, user_id)

# Delete grupo
@router.delete("/{id_grupo}", status_code=204)
def delete_grupo(
    id_grupo: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    service.delete_grupo(db, id_grupo, user_id)
    return None
