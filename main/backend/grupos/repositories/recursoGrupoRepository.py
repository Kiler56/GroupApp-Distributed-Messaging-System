from sqlalchemy.orm import Session
from models.recursoGrupoModel import RecursoGrupo

class RecursoGrupoRepository:

    def get_all(self, db: Session):
        return db.query(RecursoGrupo).all()

    def get_by_id(self, db: Session, id_recurso: str):
        return db.query(RecursoGrupo).filter(
            RecursoGrupo.id_recurso == id_recurso
        ).first()

    def create(self, db: Session, data: dict):
        db_recurso = RecursoGrupo(**data)
        db.add(db_recurso)
        return db_recurso

    def delete(self, db: Session, db_recurso: RecursoGrupo):
        db.delete(db_recurso)