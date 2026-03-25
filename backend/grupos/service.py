from sqlalchemy.orm import Session
from fastapi import HTTPException

from .repository.repository import (
    GrupoRepository,
    UsuariosGrupoRepository,
    RolGrupoRepository
)

from .schemas.schemas import (
    GrupoCreate,
    GrupoUpdate,
    UsuariosGrupoCreate
)


class GrupoService:

    def __init__(self):
        self.grupo_repo = GrupoRepository()
        self.usuarios_repo = UsuariosGrupoRepository()
        self.rol_repo = RolGrupoRepository()

    # =========================
    # --- GRUPOS ---
    # =========================

    def get_grupos(self, db: Session):
        return self.grupo_repo.get_all(db)

    def get_grupo(self, db: Session, id_grupo: str):
        grupo = self.grupo_repo.get_by_id(db, id_grupo)
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo no encontrado")
        return grupo

    def create_grupo(self, db: Session, data: GrupoCreate, user_id: str):
        try:
            # 1. Crear grupo
            grupo_data = data.model_dump()
            grupo_data["id_usuario_crea"] = user_id

            grupo = self.grupo_repo.create(db, grupo_data)

            # 2. Crear roles default
            admin_role = self.rol_repo.create(db, {
                "id_grupo": grupo.id_grupo,
                "nombre": "admin",
                "descripcion": "Administrador del grupo"
            })

            member_role = self.rol_repo.create(db, {
                "id_grupo": grupo.id_grupo,
                "nombre": "member",
                "descripcion": "Miembro del grupo"
            })

            # 3. Agregar creador como admin
            self.usuarios_repo.create(db, {
                "id_grupo": grupo.id_grupo,
                "id_usuario": user_id,
                "id_rol_grupo": admin_role.id_rol_grupo
            })

            # 4. Commit final (TRANSACCIÓN)
            db.commit()
            db.refresh(grupo)

            return grupo

        except Exception as e:
            db.rollback()
            raise e

    def update_grupo(self, db: Session, id_grupo: str, data: GrupoUpdate):
        grupo = self.get_grupo(db, id_grupo)

        update_data = data.model_dump(exclude_unset=True)

        self.grupo_repo.update(db, grupo, update_data)

        db.commit()
        db.refresh(grupo)

        return grupo

    def delete_grupo(self, db: Session, id_grupo: str):
        grupo = self.get_grupo(db, id_grupo)

        self.grupo_repo.delete(db, grupo)

        db.commit()

        return True

    # =========================
    # --- USUARIOS_GRUPO ---
    # =========================

    def add_usuario_a_grupo(self, db: Session, id_grupo: str, data: UsuariosGrupoCreate):
        
        # 1. validar grupo
        grupo = self.get_grupo(db, id_grupo)

        # 2. evitar duplicados
        existing = self.usuarios_repo.get_one(
            db,
            id_grupo,
            data.id_usuario
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="El usuario ya pertenece al grupo"
            )

        # 3. validar rol
        rol = self.rol_repo.get_by_id(db, data.id_rol_grupo)
        if not rol:
            raise HTTPException(
                status_code=404,
                detail="Rol no encontrado"
            )

        # 4. crear relación
        usuario_grupo = self.usuarios_repo.create(db, {
            "id_grupo": id_grupo,
            "id_usuario": data.id_usuario,
            "id_rol_grupo": data.id_rol_grupo,
            "id_estado": data.id_estado
        })

        db.commit()
        db.refresh(usuario_grupo)

        return usuario_grupo

    def get_usuarios_grupo(self, db: Session, id_grupo: str):
        self.get_grupo(db, id_grupo)  # valida existencia
        return self.usuarios_repo.get_by_grupo(db, id_grupo)