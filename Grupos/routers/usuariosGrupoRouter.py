from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from Grupos.utils.dependencies import get_current_user
from Grupos.config.database import get_db

from Grupos.schemas.usuariosGrupoSchema import (
    UsuariosGrupoCreate,
    UsuariosGrupoResponse
)

from Grupos.services.usuariosGrupoService import UsuariosGrupoService


router = APIRouter(tags=["Grupos"])
service = UsuariosGrupoService()


@router.post("/users-groups/{id_grupo}/usuarios", response_model=UsuariosGrupoResponse, status_code=status.HTTP_201_CREATED)
def add_usuario_a_grupo(
    id_grupo: str,
    data: UsuariosGrupoCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return service.add_usuario_a_grupo(db, id_grupo, data, user_id)


@router.get("/users-groups/{id_grupo}/usuarios", response_model=List[UsuariosGrupoResponse])
def get_usuarios_grupo(
    id_grupo: str,
    db: Session = Depends(get_db)
):
    return service.get_usuarios_grupo(db, id_grupo)


@router.delete("/users-groups/{id_grupo}/usuarios/{id_usuario}")
def remove_usuario(
    id_grupo: str,
    id_usuario: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return service.remove_usuario_from_grupo(
        db,
        id_grupo,
        id_usuario,
        user_id
    )

@router.put("/users-groups/{id_grupo}/usuarios/{id_usuario}")
def update_usuario_rol(
    id_grupo: str,
    id_usuario: int,
    data: UsuariosGrupoCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return service.update_usuario_grupo(db, id_grupo, id_usuario, data, user_id)


@router.post("/users-groups/{id_grupo}/join", status_code=status.HTTP_201_CREATED)
def join_grupo(
    id_grupo: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return service.join_grupo(db, id_grupo, user_id)


@router.delete("/users-groups/{id_grupo}/leave")
def leave_grupo(
    id_grupo: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return service.leave_grupo(db, id_grupo, user_id)
