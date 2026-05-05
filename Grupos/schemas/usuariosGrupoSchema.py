from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UsuariosGrupoModel(BaseModel):
    id_usuario: str
    id_grupo: str
    id_estado: str

class UsuariosGrupoCreate(BaseModel):
    id_usuario: str
    id_rol_grupo: str
    id_estado: str

class UsuariosGrupoUpdate(BaseModel):
    id_rol_grupo: Optional[str] = None
    id_estado: Optional[str] = None

class UsuariosGrupoResponse(BaseModel):
    id_usuario_grupo: str
    id_grupo: str
    id_usuario: str
    id_rol_grupo: str
    id_estado: Optional[str]
    fecha_union: datetime

    class Config:
        from_attributes = True
