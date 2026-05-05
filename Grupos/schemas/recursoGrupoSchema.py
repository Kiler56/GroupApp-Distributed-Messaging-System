from pydantic import BaseModel

class RecursoGrupoModel(BaseModel):
    nombre_recurso: str
    codigo_interno: str

class RecursoGrupoResponse(RecursoGrupoBase):
    id_recurso: int
    codigo_interno: str

    class Config:
        from_attributes = True
