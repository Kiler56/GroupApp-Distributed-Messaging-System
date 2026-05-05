from sqlalchemy.orm import Session
from Grupos.models.usuariosGrupoModel import UsuariosGrupo

class UsuariosGrupoRepository:

    def get_by_grupo(self, db: Session, id_grupo: str):
        return db.query(UsuariosGrupo).filter(
            UsuariosGrupo.id_grupo == id_grupo
        ).all()

    def get_by_usuario(self, db: Session, id_usuario: str):
        return db.query(UsuariosGrupo).filter(
            UsuariosGrupo.id_usuario == id_usuario
        ).all()

    def get_one(self, db: Session, id_grupo: str, id_usuario: str):
        return db.query(UsuariosGrupo).filter(
            UsuariosGrupo.id_grupo == id_grupo,
            UsuariosGrupo.id_usuario == id_usuario
        ).first()

    def get_by_user_and_group(self, db: Session, user_id: str, id_grupo: str):
        return db.query(UsuariosGrupo).filter(
            UsuariosGrupo.id_usuario == user_id,
            UsuariosGrupo.id_grupo == id_grupo
        ).first()

    def create(self, db: Session, data: dict):
        db_ug = UsuariosGrupo(**data)
        db.add(db_ug)
        return db_ug

    def update(self, db: Session, db_ug: UsuariosGrupo, data: dict):
        for key, value in data.items():
            setattr(db_ug, key, value)
        return db_ug

    def delete(self, db: Session, db_ug: UsuariosGrupo):
        db.delete(db_ug)
