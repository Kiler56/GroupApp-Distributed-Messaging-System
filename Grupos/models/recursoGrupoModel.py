from sqlalchemy import Column, String
from Grupos.database import Base

class RecursoGrupo(Base):
    __tablename__ = "recurso_grupo"

    id_recurso = Column(int, primary_key=True)
    nombre_recurso = Column(String, nullable=False)
    codigo_interno = Column(String, nullable=False)
