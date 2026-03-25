from sqlalchemy.orm import Session
from fastapi import HTTPException

from repositories.usuariosGrupoRepository import UsuariosGrupoRepository

from repositories.rolGrupoRepository import RolGrupoRepository

from schemas.usuariosGrupoSchema import UsuariosGrupoCreate

from services.grupoService import GrupoService

class UsuariosGrupoService:

    def __init__(self):
        self.grupo_service = GrupoService()
        self.usuarios_repo = UsuariosGrupoRepository()
        self.rol_repo = RolGrupoRepository()

    def add_usuario_a_grupo(self, db: Session, id_grupo: str, data: UsuariosGrupoCreate):
        
        # - validar grupo
        grupo = self.grupo_service.get_grupo(db, id_grupo)

        # - evitar duplicados
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

        # - validar rol
        rol = self.rol_repo.get_by_id(db, data.id_rol_grupo)
        if not rol:
            raise HTTPException(
                status_code=404,
                detail="Rol no encontrado"
            )

        # - crear relación
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
        self.grupo_service.get_grupo(db, id_grupo)  # valida existencia
        return self.usuarios_repo.get_by_grupo(db, id_grupo)