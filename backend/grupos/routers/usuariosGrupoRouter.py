from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db

from schemas.usuariosGrupoSchema import (
    UsuariosGrupoCreate,
    UsuariosGrupoResponse
)
from services.usuariosGrupoService import UsuariosGrupoService

router = APIRouter(prefix="/grupos", tags=["Grupos"])
service = UsuariosGrupoService()

# (reemplazar luego con JWT real)
def get_current_user():
    return "user-123"

# Agregar usuario grupo
@router.post("/{id_grupo}/usuarios", 
             response_model=UsuariosGrupoResponse, 
             status_code=status.HTTP_201_CREATED)
def add_usuario_a_grupo(
    id_grupo: str,
    data: UsuariosGrupoCreate,
    db: Session = Depends(get_db)
):
    return service.add_usuario_a_grupo(db, id_grupo, data)

# Get all usuarios grupo por id_grupo
@router.get("/{id_grupo}/usuarios",
            response_model=List[UsuariosGrupoResponse])
def get_usuarios_grupo(
    id_grupo: str,
    db: Session = Depends(get_db)
):
    return service.get_usuarios_grupo(db, id_grupo)