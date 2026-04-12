from sqlalchemy import Column, Index, String, ForeignKey
from uuid6 import uuid7
from app.core.database import database

class RolRecurso(database):
    __tablename__ = "rol_recurso"

    __table_args__ = (
        Index('idx_rol_recurso_rol', 'id_rol_grupo'),
        Index('idx_rol_recurso_recurso', 'id_recurso'),
    )

    id_rol_recurso = Column(String, primary_key=True, default=lambda: str(uuid7()))
    id_rol_grupo = Column(String, ForeignKey("rol_grupo.id_rol_grupo", ondelete="CASCADE"), nullable=False)
    id_recurso = Column(String, ForeignKey("recurso_grupo.id_recurso"), nullable=False)