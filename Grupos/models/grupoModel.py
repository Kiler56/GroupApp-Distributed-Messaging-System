from sqlalchemy import Column, DateTime, Index, String, ForeignKey, Boolean, UniqueConstraint
from uuid6 import uuid7
from datetime import datetime
from Grupos.config.database import Base

class Grupo(Base):
    __tablename__ = "grupo"

    id_grupo = Column(String, primary_key=True, default=lambda: str(uuid7()))
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    id_usuario_crea = Column(String, nullable=False)
    privado = Column(Boolean, nullable=False)
    requiere_invitacion = Column(Boolean, nullable=False)
    id_grupo_padre = Column(String, ForeignKey("grupo.id_grupo", ondelete="CASCADE"), nullable=True)

