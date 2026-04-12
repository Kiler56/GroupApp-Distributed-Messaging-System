from sqlalchemy.orm import Session
from models.rolRecursoModel import RolRecurso

class RolRecursoRepository:

    def get_by_rol(self, db: Session, id_rol_grupo: str):
        return db.query(RolRecurso).filter(
            RolRecurso.id_rol_grupo == id_rol_grupo
        ).all()

    def create(self, db: Session, data: dict):
        db_rr = RolRecurso(**data)
        db.add(db_rr)
        return db_rr

    def delete(self, db: Session, db_rr: RolRecurso):
        db.delete(db_rr)