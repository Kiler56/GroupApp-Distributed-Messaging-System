
from pydantic import BaseModel
from typing import Optional

class RolGrupoModel(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    activo: bool = True

class RolGrupoCreate(RolGrupoModel):
    pass  # id_grupo viene del path (/groups/{id}/roles)

class RolGrupoUpdate(RolGrupoModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class RolGrupoResponse(RolGrupoModel):
    id_rol_grupo: str
    id_grupo: str

    class Config:
        from_attributes = True