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

@router.get("/groups", response_model=List[GrupoResponse])
def get_grupos(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return service.get_grupos(db, user_id)

@router.get("/groups/{id_grupo}/subgroups", response_model=List[GrupoResponse])
def get_subgroups(id_grupo: str, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    return service.get_subgroups(db, id_grupo, user_id)

@router.get("/my-groups", response_model=List[GrupoResponse])
def get_my_grupos(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return service.get_my_grupos(db, user_id)

@router.get("/groups/{id_grupo}", response_model=GrupoResponse)
def get_grupo(id_grupo: str, db: Session = Depends(get_db)):
    return service.get_grupo(db, id_grupo)

@router.post("/", response_model=GrupoResponse, status_code=status.HTTP_201_CREATED)
def create_grupo(
    grupo: GrupoCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    return service.create_grupo(db, grupo, user_id)

@router.put("/{id_grupo}")
def update_grupo(
    id_grupo: str,
    grupo: GrupoUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    return service.update_grupo(db, id_grupo, grupo, user_id)

@router.delete("/{id_grupo}", status_code=204)
def delete_grupo(
    id_grupo: str,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    service.delete_grupo(db, id_grupo, user_id)
    return None

@router.get("/{id_grupo}/roles")
def get_group_roles(id_grupo: str):
    return service.get_group_roles(id_grupo)

@router.post("/{id_grupo}/roles")
def create_role(id_grupo: str, data: dict, user_id: int = Depends(get_current_user)):
    return service.create_role(id_grupo, data, user_id)

@router.put("/{id_grupo}/roles/{id_rol_grupo}")
def update_role(id_grupo: str, id_rol_grupo: str, data: dict, user_id: int = Depends(get_current_user)):
    return service.update_role(id_grupo, id_rol_grupo, data, user_id)

@router.delete("/{id_grupo}/roles/{id_rol_grupo}")
def delete_role(id_grupo: str, id_rol_grupo: str, user_id: int = Depends(get_current_user)):
    return service.delete_role(id_grupo, id_rol_grupo, user_id)

@router.get("/resources/all")
def get_all_resources():
    return service.get_all_resources()

@router.post("/{id_grupo}/roles/{id_rol_grupo}/permissions/{id_recurso}")
def assign_permission(id_grupo: str, id_rol_grupo: str, id_recurso: str, user_id: int = Depends(get_current_user)):
    return service.assign_permission(id_grupo, id_rol_grupo, id_recurso, user_id)

@router.delete("/{id_grupo}/roles/{id_rol_grupo}/permissions/{id_recurso}")
def remove_permission(id_grupo: str, id_rol_grupo: str, id_recurso: str, user_id: int = Depends(get_current_user)):
    return service.remove_permission(id_grupo, id_rol_grupo, id_recurso, user_id)

@router.post("/{id_grupo}/invite")
def invite_user(id_grupo: str, data: dict, user_id: int = Depends(get_current_user)):
    return service.invite_by_email(id_grupo, data.get("email"), user_id)
