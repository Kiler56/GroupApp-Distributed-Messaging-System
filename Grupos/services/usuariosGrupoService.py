# -*- coding: utf-8 -*-
from sqlalchemy.orm import Session
from fastapi import HTTPException

from Grupos.repositories.usuariosGrupoRepository import UsuariosGrupoRepository
from Grupos.roles_client import RolesClient
from Grupos.schemas.usuariosGrupoSchema import UsuariosGrupoCreate
from Grupos.services.grupoService import GrupoService

class UsuariosGrupoService:

    def __init__(self):
        self.grupo_service = GrupoService()
        self.usuarios_repo = UsuariosGrupoRepository()
        self.roles_client = RolesClient()

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
        user_rel = self.usuarios_repo.get_by_user_and_group(db, str(user_id), id_grupo)

        if not user_rel:
            raise HTTPException(
                status_code=403,
                detail="No perteneces al grupo"
            )

        # 3. Validar admin
        rol = self.roles_client.get_role_by_id(user_rel.id_rol_grupo)

        if not rol:
            # Si el rol no se encuentra (puede pasar si se borró en el MS Roles)
            # asumimos que no es admin por seguridad
            raise HTTPException(
                status_code=403,
                detail="No tienes un rol válido asignado"
            )

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
        rol_asignar = self.roles_client.get_role_by_id(data.id_rol_grupo)

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
        user_rel = self.usuarios_repo.get_by_user_and_group(db, str(user_id), id_grupo)

        if not user_rel:
           raise HTTPException(403, "No perteneces al grupo")

        # 3. Validar que es admin
        rol = self.roles_client.get_role_by_id(user_rel.id_rol_grupo)

        if not rol or rol.nombre != "Administrador":
          raise HTTPException(403, "No eres administrador")

        # 4. Buscar usuario a eliminar
        target_rel = self.usuarios_repo.get_by_user_and_group(db, str(target_user_id), id_grupo)

        if not target_rel:
          raise HTTPException(404, "Usuario no pertenece al grupo")

        # 5. evitar que se elimine a sí mismo como admin
        if str(target_user_id) == str(user_id):
          raise HTTPException(400, "Usa la opción de salir del grupo")
 
        # 6. Eliminar
        self.usuarios_repo.delete(db, target_rel)

        db.commit()

        return {"message": "Usuario eliminado del grupo"}

    def update_usuario_grupo(
        self,
        db: Session,
        id_grupo: str,
        target_user_id: int,
        data: UsuariosGrupoCreate, # Usamos este schema para id_rol_grupo
        user_id: int
    ):
        # 1. Validar grupo
        self.grupo_service.get_grupo(db, id_grupo)

        # 2. Validar que quien ejecuta pertenece
        user_rel = self.usuarios_repo.get_by_user_and_group(db, str(user_id), id_grupo)

        if not user_rel:
           raise HTTPException(403, "No perteneces al grupo")

        # 3. Validar que es admin
        rol = self.roles_client.get_role_by_id(user_rel.id_rol_grupo)

        if not rol or rol.nombre != "Administrador":
          raise HTTPException(403, "No eres administrador")

        # 4. Buscar relación del usuario objetivo
        target_rel = self.usuarios_repo.get_by_user_and_group(db, str(target_user_id), id_grupo)

        if not target_rel:
          raise HTTPException(404, "Usuario no pertenece al grupo")

        # REGLA SEGURIDAD: Solo uno mismo puede cambiarse su propio rol si es admin
        # O mejor dicho: un admin no puede cambiar el rol de otro admin.
        if str(target_user_id) != str(user_id):
            target_rol = self.roles_client.get_role_by_id(target_rel.id_rol_grupo)
            if target_rol and target_rol.nombre == "Administrador":
                raise HTTPException(403, "No puedes modificar el rol de otro Administrador")

        # 5. Actualizar
        target_rel.id_rol_grupo = data.id_rol_grupo
        if data.id_estado:
            target_rel.id_estado = data.id_estado

        db.commit()
        db.refresh(target_rel)

        return target_rel


    def join_grupo(
        self,
        db: Session,
        id_grupo: str,
        user_id: int
    ):
        # 1. Validar grupo
        grupo = self.grupo_service.get_grupo(db, id_grupo)

        if grupo.privado:
            raise HTTPException(
                status_code=403,
                detail="No puedes unirte directamente a un grupo privado"
            )

        # 2. Evitar duplicados
        existing = self.usuarios_repo.get_by_user_and_group(db, str(user_id), id_grupo)

        if existing:
            return {"message": "Ya perteneces al grupo", "id_usuario_grupo": existing.id_usuario_grupo}

        # 3. Buscar rol de "Miembro" para este grupo vía gRPC
        roles = self.roles_client.get_roles_by_grupo(id_grupo)
        rol_miembro = next((r for r in roles if r.nombre == "Miembro"), None)

        if not rol_miembro:
            # Si no existe, crearlo
            rol_miembro = self.roles_client.create_role(
                id_grupo=id_grupo,
                nombre="Miembro",
                descripcion="Miembro del grupo"
            )

        # 4. Crear relación
        usuario_grupo = self.usuarios_repo.create(db, {
            "id_grupo": id_grupo,
            "id_usuario": str(user_id),
            "id_rol_grupo": rol_miembro.id_rol_grupo,
            "id_estado": "ACTIVO"
        })

        db.commit()
        db.refresh(usuario_grupo)

        return usuario_grupo

    def leave_grupo(
    self,
    db: Session,
    id_grupo: str,
    user_id: int
):
    # 1. Validar grupo
        self.grupo_service.get_grupo(db, id_grupo)

    # 2. Buscar relación
        user_rel = self.usuarios_repo.get_by_user_and_group(db, str(user_id), id_grupo)

        if not user_rel:
           raise HTTPException(404, "No perteneces al grupo")

    # 3. Eliminar
        self.usuarios_repo.delete(db, user_rel)

        db.commit()

        return {"message": "Saliste del grupo"}
    
    def get_usuarios_grupo(self, db: Session, id_grupo: str):
        self.grupo_service.get_grupo(db, id_grupo)
        return self.usuarios_repo.get_by_grupo(db, id_grupo)
