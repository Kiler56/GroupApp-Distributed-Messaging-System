from sqlalchemy.orm import Session
from fastapi import HTTPException

from Grupos.repositories.usuariosGrupoRepository import UsuariosGrupoRepository
from Grupos.repositories.grupoRepository import GrupoRepository
from Grupos.roles_client import RolesClient
from Grupos.auth_client import AuthClient

from Grupos.schemas.grupoSchema import (
    GrupoCreate,
    GrupoUpdate,
)


class GrupoService:

    def __init__(self):
        self.grupo_repo = GrupoRepository()
        self.roles_client = RolesClient()
        self.auth_client = AuthClient()
        self.usuarios_repo = UsuariosGrupoRepository()

    # Get all grupos
    def get_grupos(self, db: Session):
        return self.grupo_repo.get_all(db)

    # Get subgroups
    def get_subgroups(self, db: Session, id_padre: str):
        return self.grupo_repo.get_subgroups(db, id_padre)

    # Get my grupos
    def get_my_grupos(self, db: Session, user_id: int):
        relaciones = self.usuarios_repo.get_by_usuario(db, str(user_id))
        ids_grupos = [rel.id_grupo for rel in relaciones]
        return db.query(self.grupo_repo.model).filter(self.grupo_repo.model.id_grupo.in_(ids_grupos)).all()

    # Get grupo por id
    def get_grupo(self, db: Session, id_grupo: str):
        grupo = self.grupo_repo.get_by_id(db, id_grupo)
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo no encontrado")
        return grupo

    # Validar admin
    def validate_admin(self, db: Session, id_grupo: str, user_id: int):
        print(f"DEBUG: Validating admin for user {user_id} in group {id_grupo}")
        
        grupo = self.grupo_repo.get_by_id(db, id_grupo)
        if not grupo:
            raise HTTPException(status_code=404, detail="Grupo no encontrado")

        usuario_grupo = self.usuarios_repo.get_one(
            db,
            id_grupo,
            str(user_id)
        )

        is_admin = False
        if usuario_grupo:
            rol = self.roles_client.get_role_by_id(usuario_grupo.id_rol_grupo)
            if rol and (rol.nombre == "Administrador" or rol.nombre == "Admin discusión"):
                is_admin = True

        # Si no es admin directo y es una discusión, validar si es admin del padre
        if not is_admin and grupo.id_grupo_padre:
            print(f"DEBUG: Checking parent group {grupo.id_grupo_padre} for admin rights")
            try:
                # Recursión para validar admin en el padre
                return self.validate_admin(db, grupo.id_grupo_padre, user_id)
            except HTTPException:
                pass

        if not is_admin:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos administrativos para realizar esta acción"
            )

        return True

    # Crear grupo
    def create_grupo(self, db: Session, data: GrupoCreate, user_id: int):
        try:
            # 1. Crear grupo
            grupo_data = data.model_dump()
            grupo_data["id_usuario_crea"] = user_id

            grupo = self.grupo_repo.create(db, grupo_data)

            db.flush()

            # 2. Manejo de Roles según jerarquía
            if grupo.id_grupo_padre:
                # Es una discusión: Solo crear "Admin discusión"
                admin_role = self.roles_client.create_role(
                    id_grupo=grupo.id_grupo,
                    nombre="Admin discusión",
                    descripcion=f"Administrador de la discusión: {grupo.nombre}"
                )
            else:
                # Es grupo principal: Crear Admin y Miembro estándar
                admin_role = self.roles_client.create_role(
                    id_grupo=grupo.id_grupo,
                    nombre="Administrador",
                    descripcion="Administrador del grupo"
                )
                
                self.roles_client.create_role(
                    id_grupo=grupo.id_grupo,
                    nombre="Miembro",
                    descripcion="Miembro del grupo"
                )

            # Asignar todos los recursos al admin (de grupo o discusión) automáticamente
            all_resources = self.roles_client.get_all_resources()
            for res in all_resources:
                self.roles_client.assign_resource_to_role(admin_role.id_rol_grupo, res.id_recurso)

            # 3. Agregar creador como admin (del grupo o de la discusión)
            self.usuarios_repo.create(db, {
                "id_grupo": grupo.id_grupo,
                "id_usuario": str(user_id),
                "id_rol_grupo": admin_role.id_rol_grupo,
                "id_estado": "ACTIVO"
            })

            db.commit()
            db.refresh(grupo)

            return grupo

        except Exception as e:
            db.rollback()
            raise e

    #  Update grupo
    def update_grupo(self, db: Session, id_grupo: str, data: GrupoUpdate, user_id: int):
        grupo = self.get_grupo(db, id_grupo)

        # validar admin
        self.validate_admin(db, id_grupo, user_id)

        update_data = data.model_dump(exclude_unset=True)

        self.grupo_repo.update(db, grupo, update_data)

        db.commit()
        db.refresh(grupo)

        return grupo

    # Delete grupo
    def delete_grupo(self, db: Session, id_grupo: str, user_id: int):
        grupo = self.get_grupo(db, id_grupo)

        # validar admin
        self.validate_admin(db, id_grupo, user_id)

        self.grupo_repo.delete(db, grupo)

        db.commit()

        return True

    def get_group_roles(self, id_grupo: str):
        # 1. Obtener grupo actual
        from Grupos.database import SessionLocal
        db = SessionLocal()
        grupo = self.grupo_repo.get_by_id(db, id_grupo)
        db.close()
        
        if not grupo:
            return []

        # 2. Roles locales
        roles = self.roles_client.get_roles_by_grupo(id_grupo)
        
        # 3. Si es una discusión, añadir roles del padre
        if grupo.id_grupo_padre:
            parent_roles = self.roles_client.get_roles_by_grupo(grupo.id_grupo_padre)
            # Evitar duplicados por nombre
            existing_names = {r.nombre for r in roles}
            for pr in parent_roles:
                if pr.nombre not in existing_names:
                    roles.append(pr)

        result = []
        for r in roles:
            permissions = self.roles_client.get_resources_by_role(r.id_rol_grupo)
            result.append({
                "id_rol_grupo": r.id_rol_grupo,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "permisos": [p.id_recurso for p in permissions]
            })
        return result

    # Get subgroups
    def get_subgroups(self, db: Session, id_padre: str, user_id: int = None):
        # 1. Obtener todos los subgrupos
        all_subgroups = self.grupo_repo.get_subgroups(db, id_padre)
        
        # 2. Si no hay user_id (petición anónima), solo públicos
        if not user_id:
            return [g for g in all_subgroups if not g.privado]

        # 3. Verificar si el usuario es Admin del padre
        is_parent_admin = False
        try:
            # Validamos contra el padre
            is_parent_admin = self.validate_admin(db, id_padre, user_id)
        except HTTPException:
            pass

        # 4. Si es admin del padre, ve todo. Si no, solo públicos o donde sea miembro.
        if is_parent_admin:
            return all_subgroups

        # Filtrar para usuarios normales
        user_memberships = self.usuarios_repo.get_by_usuario(db, str(user_id))
        member_group_ids = {rel.id_grupo for rel in user_memberships}

        return [g for g in all_subgroups if not g.privado or g.id_grupo in member_group_ids]

    def create_role(self, id_grupo: str, data: dict, user_id: int):
        from Grupos.database import SessionLocal
        db = SessionLocal()
        try:
            self.validate_admin(db, id_grupo, user_id)
            r = self.roles_client.create_role(id_grupo, data.get("nombre"), data.get("descripcion", ""))
            return {
                "id_rol_grupo": r.id_rol_grupo,
                "id_grupo": r.id_grupo,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "activo": r.activo
            }
        finally:
            db.close()

    def update_role(self, id_grupo: str, id_rol_grupo: str, data: dict, user_id: int):
        from Grupos.database import SessionLocal
        db = SessionLocal()
        try:
            self.validate_admin(db, id_grupo, user_id)
            r = self.roles_client.update_role(id_rol_grupo, data.get("nombre"), data.get("descripcion", ""))
            return {
                "id_rol_grupo": r.id_rol_grupo,
                "id_grupo": r.id_grupo,
                "nombre": r.nombre,
                "descripcion": r.descripcion,
                "activo": r.activo
            }
        finally:
            db.close()

    def delete_role(self, id_grupo: str, id_rol_grupo: str, user_id: int):
        from Grupos.database import SessionLocal
        db = SessionLocal()
        try:
            self.validate_admin(db, id_grupo, user_id)
            return self.roles_client.delete_role(id_rol_grupo)
        finally:
            db.close()

    def get_all_resources(self):
        resources = self.roles_client.get_all_resources()
        return [{"id_recurso": r.id_recurso, "nombre_recurso": r.nombre_recurso, "codigo_interno": r.codigo_interno} for r in resources]

    def invite_by_email(self, id_grupo: str, email: str, user_id: int):
        from Grupos.database import SessionLocal
        db = SessionLocal()
        try:
            # 1. Validar permisos del invitador
            self.validate_admin(db, id_grupo, user_id)
            
            # 2. Buscar usuario en Auth vía gRPC
            user = self.auth_client.get_user_by_email(email)
            if not user:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # 3. Verificar si ya es miembro
            existing = self.usuarios_repo.get_by_user_and_group(db, str(user.id_usuario), id_grupo)
            if existing:
                raise HTTPException(status_code=400, detail="El usuario ya es miembro del grupo")

            # 4. Obtener rol miembro
            roles = self.roles_client.get_roles_by_grupo(id_grupo)
            rol_miembro = next((r for r in roles if r.nombre == "Miembro"), roles[-1] if roles else None)
            
            if not rol_miembro:
                raise HTTPException(status_code=500, detail="No se pudo determinar un rol para el nuevo miembro")

            # 5. Agregar
            rel = self.usuarios_repo.create(db, {
                "id_grupo": id_grupo,
                "id_usuario": str(user.id_usuario),
                "id_rol_grupo": rol_miembro.id_rol_grupo,
                "id_estado": "ACTIVO"
            })
            db.commit()
            return {"id_usuario": user.id_usuario, "username": user.username}
        finally:
            db.close()

    def assign_permission(self, id_grupo: str, id_rol_grupo: str, id_recurso: str, user_id: int):
        from Grupos.database import SessionLocal
        db = SessionLocal()
        try:
            self.validate_admin(db, id_grupo, user_id)
            res = self.roles_client.assign_resource_to_role(id_rol_grupo, id_recurso)
            return {
                "id_rol_recurso": res.id_rol_recurso,
                "id_rol_grupo": res.id_rol_grupo,
                "id_recurso": res.id_recurso
            }
        finally:
            db.close()

    def remove_permission(self, id_grupo: str, id_rol_grupo: str, id_recurso: str, user_id: int):
        from Grupos.database import SessionLocal
        db = SessionLocal()
        try:
            self.validate_admin(db, id_grupo, user_id)
            success = self.roles_client.remove_resource_from_role(id_rol_grupo, id_recurso)
            return {"success": success}
        finally:
            db.close()
