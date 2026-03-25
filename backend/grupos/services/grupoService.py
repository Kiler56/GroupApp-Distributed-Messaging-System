from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.grupoRepository import GrupoRepository
from repositories.rolGrupoRepository import RolGrupoRepository
from ..usuarios.repositories.usuariosRepository import UsuariosRepository

from schemas.grupoSchema import (
    GrupoCreate,
    GrupoUpdate,
)

class GrupoService:

    def __init__(self):
        self.grupo_repo = GrupoRepository()
        self.rol_repo = RolGrupoRepository()
        self.usuarios_repo = UsuariosRepository()

    # Get all grupos
    def get_grupos(self, db: Session):
        return self.grupo_repo.get_all(db)

    # Get gripo por id
    def get_grupo(self, db: Session, id_grupo: str):
        grupo = self.grupo_repo.get_by_id(db, id_grupo)
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo no encontrado")
        return grupo

    # Crear grupo
    def create_grupo(self, db: Session, data: GrupoCreate, user_id: str):
        try:
            # - Crear grupo
            grupo_data = data.model_dump()
            grupo_data["id_usuario_crea"] = user_id

            grupo = self.grupo_repo.create(db, grupo_data)

            # - Crear roles default
            admin_role = self.rol_repo.create(db, {
                "id_grupo": grupo.id_grupo,
                "nombre": "Administrador",
                "descripcion": "Administrador del grupo"
            })

            member_role = self.rol_repo.create(db, {
                "id_grupo": grupo.id_grupo,
                "nombre": "Miembro",
                "descripcion": "Miembro del grupo"
            })

            # - Agregar creador como admin
            self.usuarios_repo.create(db, {
                "id_grupo": grupo.id_grupo,
                "id_usuario": user_id,
                "id_rol_grupo": admin_role.id_rol_grupo
            })

            # - Commit
            db.commit()
            db.refresh(grupo)

            return grupo

        except Exception as e:
            db.rollback()
            raise e

    # Update grupo
    def update_grupo(self, db: Session, id_grupo: str, data: GrupoUpdate):
        grupo = self.get_grupo(db, id_grupo)

        update_data = data.model_dump(exclude_unset=True)

        self.grupo_repo.update(db, grupo, update_data)

        db.commit()
        db.refresh(grupo)

        return grupo

    # Delete grupo
    def delete_grupo(self, db: Session, id_grupo: str):
        grupo = self.get_grupo(db, id_grupo)

        self.grupo_repo.delete(db, grupo)

        db.commit()

        return True