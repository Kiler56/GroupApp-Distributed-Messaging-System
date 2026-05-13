from sqlalchemy import Column, String
from Grupos.database import Base

class TipoEstadoUsrGrp(Base):
    __tablename__ = "tipo_estado_usr_grp"

    id_estado = Column(String, primary_key=True)
    nombre = Column(String, unique=True, index=True)
