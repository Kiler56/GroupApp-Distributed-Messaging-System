from sqlalchemy.orm import Session
from Grupos.models.grupoModel import Grupo

class GrupoRepository:
    model = Grupo

    def get_all(self, db: Session):
        return db.query(Grupo).all()

    def get_by_id(self, db: Session, id_grupo: str):
        return db.query(Grupo).filter(
            Grupo.id_grupo == id_grupo
        ).first()

    def create(self, db: Session, data: dict):
        db_grupo = Grupo(**data)
        db.add(db_grupo)
        return db_grupo

    def update(self, db: Session, db_grupo: Grupo, data: dict):
        for key, value in data.items():
            setattr(db_grupo, key, value)
        return db_grupo

    def delete(self, db: Session, db_grupo: Grupo):
        db.delete(db_grupo)
