from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.grupos.repositories.usuariosGrupoRepository import UsuariosGrupoRepository
from backend.grupos.repositories.grupoRepository import GrupoRepository
from backend.grupos.repositories.rolGrupoRepository import RolGrupoRepository

from backend.grupos.schemas.grupoSchema import (
    GrupoCreate,
    GrupoUpdate,
)


class GrupoService:

    def __init__(self):
        self.grupo_repo = GrupoRepository()
        self.rol_repo = RolGrupoRepository()
        self.usuarios_repo = UsuariosGrupoRepository()

    # Get all grupos
    def get_grupos(self, db: Session):
        return self.grupo_repo.get_all(db)

    # Get grupo por id
    def get_grupo(self, db: Session, id_grupo: str):
        grupo = self.grupo_repo.get_by_id(db, id_grupo)
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo no encontrado")
        return grupo

    # 🔐 Validar admin (REUTILIZABLE)
    def validate_admin(self, db: Session, id_grupo: str, user_id: int):
        usuario_grupo = self.usuarios_repo.get_one(
            db,
            id_grupo,
            user_id
        )

        if not usuario_grupo:
            raise HTTPException(
                status_code=403,
                detail="No perteneces al grupo"
            )

        rol = self.rol_repo.get_by_id(db, usuario_grupo.id_rol_grupo)

        if rol.nombre != "Administrador":
            raise HTTPException(
                status_code=403,
                detail="No eres administrador"
            )

        return True

    # ✅ Crear grupo
    def create_grupo(self, db: Session, data: GrupoCreate, user_id: int):
        try:
            # 1. Crear grupo
            grupo_data = data.model_dump()
            grupo_data["id_usuario_crea"] = user_id

            grupo = self.grupo_repo.create(db, grupo_data)

            db.flush()

            # 2. Crear roles
            admin_role = self.rol_repo.create(db, {
                "id_grupo": grupo.id_grupo,
                "nombre": "Administrador",
                "descripcion": "Administrador del grupo"
            })

            miembro_role = self.rol_repo.create(db, {
                "id_grupo": grupo.id_grupo,
                "nombre": "Miembro",
                "descripcion": "Miembro del grupo"
            })

            db.flush()

            # 3. Agregar creador como admin
            self.usuarios_repo.create(db, {
                "id_grupo": grupo.id_grupo,
                "id_usuario": user_id,
                "id_rol_grupo": admin_role.id_rol_grupo,
                "id_estado": "ACTIVO"
            })

            db.commit()
            db.refresh(grupo)

            return grupo

        except Exception as e:
            db.rollback()
            raise e

    # ✏️ Update grupo
    def update_grupo(self, db: Session, id_grupo: str, data: GrupoUpdate, user_id: int):
        grupo = self.get_grupo(db, id_grupo)

        # 🔐 validar admin
        self.validate_admin(db, id_grupo, user_id)

        update_data = data.model_dump(exclude_unset=True)

        self.grupo_repo.update(db, grupo, update_data)

        db.commit()
        db.refresh(grupo)

        return grupo

    # 🗑️ Delete grupo
    def delete_grupo(self, db: Session, id_grupo: str, user_id: int):
        grupo = self.get_grupo(db, id_grupo)

        # 🔐 validar admin
        self.validate_admin(db, id_grupo, user_id)

        self.grupo_repo.delete(db, grupo)

        db.commit()

        return True