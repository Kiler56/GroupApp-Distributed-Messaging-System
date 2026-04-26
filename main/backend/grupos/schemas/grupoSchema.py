from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class GrupoModel(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    privado: bool = False
    requiere_invitacion: bool = False

class GrupoCreate(GrupoModel):
    pass  # id_usuario_crea viene del backend (auth)

class GrupoUpdate(GrupoModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    privado: Optional[bool] = None
    requiere_invitacion: Optional[bool] = None

class GrupoDelete(GrupoModel):
    id_grupo: str

class GrupoResponse(GrupoModel):
    id_grupo: str
    fecha_creacion: datetime
    id_usuario_crea: str

    class Config:
        from_attributes = True