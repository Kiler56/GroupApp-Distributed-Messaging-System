from sqlalchemy import Column, DateTime, Index, String, ForeignKey, Boolean, UniqueConstraint
from uuid6 import uuid7
from datetime import datetime
from auth_service.database import Base

class RolGrupo(Base):
    __tablename__ = "rol_grupo"

    __table_args__ = (
        UniqueConstraint('id_grupo', 'nombre', name='uq_rol_nombre_grupo'),
        Index('idx_rol_grupo_grupo', 'id_grupo'),
    )

    id_rol_grupo = Column(String, primary_key=True, default=lambda: str(uuid7()))
    id_grupo = Column(String, ForeignKey("grupo.id_grupo", ondelete="CASCADE"), nullable=False)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    activo = Column(Boolean, nullable=False, default=True)