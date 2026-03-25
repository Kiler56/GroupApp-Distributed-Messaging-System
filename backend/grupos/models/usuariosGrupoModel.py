from sqlalchemy import Column, DateTime, Index, String, ForeignKey, Boolean, UniqueConstraint
from uuid6 import uuid7
from datetime import datetime
from app.core.database import database

class UsuariosGrupo(database):
    __tablename__ = "usuarios_grupo"

    __table_args__ = (
        UniqueConstraint('id_grupo', 'id_usuario', name='uq_usuario_grupo'),
        Index('idx_usuarios_grupo_usuario', 'id_usuario'),
        Index('idx_usuarios_grupo_grupo', 'id_grupo'),
        Index('idx_usuarios_grupo_rol', 'id_rol_grupo'),
    )

    id_usuario_grupo = Column(String, primary_key=True, default=lambda: str(uuid7()))
    id_grupo = Column(String, ForeignKey("grupo.id_grupo", ondelete="CASCADE"), nullable=False)
    id_usuario = Column(String, ForeignKey("usuario.id_usuario"), nullable=False)
    id_rol_grupo = Column(String, ForeignKey("rol_grupo.id_rol_grupo", ondelete="CASCADE"), nullable=False)
    fecha_union = Column(DateTime, nullable=False, default=datetime.utcnow)
    id_estado = Column(String, ForeignKey("tipo_estado_usr_grp.id_estado"), nullable=False)