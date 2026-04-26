from sqlalchemy.orm import Session
from fastapi import HTTPException

from backend.grupos.repositories.usuariosGrupoRepository import UsuariosGrupoRepository
from backend.grupos.repositories.rolGrupoRepository import RolGrupoRepository
from backend.grupos.schemas.usuariosGrupoSchema import UsuariosGrupoCreate
from backend.grupos.services.grupoService import GrupoService

class UsuariosGrupoService:

    def __init__(self):
        self.grupo_service = GrupoService()
        self.usuarios_repo = UsuariosGrupoRepository()
        self.rol_repo = RolGrupoRepository()

    def add_usuario_a_grupo(
        self,
        db: Session,
        id_grupo: str,
        data: UsuariosGrupoCreate,
        user_id: int
    ):
        # 1. Validar grupo
        grupo = self.grupo_service.get_grupo(db, id_grupo)

        # 2. Validar pertenencia
        user_rel = self.usuarios_repo.get_by_user_and_group(db, user_id, id_grupo)

        if not user_rel:
            raise HTTPException(
                status_code=403,
                detail="No perteneces al grupo"
            )

        # 3. Validar admin
        rol = self.rol_repo.get_by_id(db, user_rel.id_rol_grupo)

        if rol.nombre != "Administrador":
            raise HTTPException(
                status_code=403,
                detail="No eres administrador"
            )

        # 4. Evitar duplicados
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

        # 5. Validar rol
        rol_asignar = self.rol_repo.get_by_id(db, data.id_rol_grupo)

        if not rol_asignar:
            raise HTTPException(
                status_code=404,
                detail="Rol no encontrado"
            )

        # 6. Crear relación
        usuario_grupo = self.usuarios_repo.create(db, {
            "id_grupo": id_grupo,
            "id_usuario": data.id_usuario,
            "id_rol_grupo": data.id_rol_grupo,
            "id_estado": data.id_estado
        })

        db.commit()
        db.refresh(usuario_grupo)

        return usuario_grupo
    
    def remove_usuario_from_grupo(
    self,
    db: Session,
    id_grupo: str,
    target_user_id: int,
    user_id: int
):
    # 1. Validar grupo
        self.grupo_service.get_grupo(db, id_grupo)

    # 2. Validar que quien ejecuta pertenece
        user_rel = self.usuarios_repo.get_by_user_and_group(db, user_id, id_grupo)

        if not user_rel:
           raise HTTPException(403, "No perteneces al grupo")

    # 3. Validar que es admin
        rol = self.rol_repo.get_by_id(db, user_rel.id_rol_grupo)

        if rol.nombre != "Administrador":
          raise HTTPException(403, "No eres administrador")

    # 4. Buscar usuario a eliminar
        target_rel = self.usuarios_repo.get_by_user_and_group(db, target_user_id, id_grupo)

        if not target_rel:
         raise HTTPException(404, "Usuario no pertenece al grupo")

    # 5. (opcional) evitar que se elimine a sí mismo como admin
        if target_user_id == user_id:
         raise HTTPException(400, "Usa la opción de salir del grupo")
 
    # 6. Eliminar
        self.usuarios_repo.delete(db, target_rel)

        db.commit()

        return {"message": "Usuario eliminado del grupo"}

    def leave_grupo(
    self,
    db: Session,
    id_grupo: str,
    user_id: int
):
    # 1. Validar grupo
        self.grupo_service.get_grupo(db, id_grupo)

    # 2. Buscar relación
        user_rel = self.usuarios_repo.get_by_user_and_group(db, user_id, id_grupo)

        if not user_rel:
           raise HTTPException(404, "No perteneces al grupo")

    # 3. Eliminar
        self.usuarios_repo.delete(db, user_rel)

        db.commit()

        return {"message": "Saliste del grupo"}
    
    def get_usuarios_grupo(self, db: Session, id_grupo: str):
        self.grupo_service.get_grupo(db, id_grupo)
        return self.usuarios_repo.get_by_grupo(db, id_grupo)