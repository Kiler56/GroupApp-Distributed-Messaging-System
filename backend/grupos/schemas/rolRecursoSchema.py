from pydantic import BaseModel

class RolRecursoModel(BaseModel):
    id_recurso: int
    id_rol_grupo: str

class RolRecursoResponse(BaseModel):
    id_rol_recurso: str
    id_rol_grupo: str
    id_recurso: int

    class Config:
        from_attributes = True