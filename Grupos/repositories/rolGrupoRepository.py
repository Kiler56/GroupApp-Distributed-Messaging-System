from sqlalchemy.orm import Session
from Grupos.models.rolGrupoModel import RolGrupo

class RolGrupoRepository:

    def get_by_grupo(self, db: Session, id_grupo: str):
        return db.query(RolGrupo).filter(
            RolGrupo.id_grupo == id_grupo
        ).all()

    def get_by_id(self, db: Session, id_rol_grupo: str):
        return db.query(RolGrupo).filter(
            RolGrupo.id_rol_grupo == id_rol_grupo
        ).first()

    def get_by_nombre(self, db: Session, id_grupo: str, nombre: str):
        return db.query(RolGrupo).filter(
            RolGrupo.id_grupo == id_grupo,
            RolGrupo.nombre == nombre
        ).first()

    def create(self, db: Session, data: dict):
        db_rol = RolGrupo(**data)
        db.add(db_rol)
        return db_rol

    def delete(self, db: Session, db_rol: RolGrupo):
        db.delete(db_rol)
