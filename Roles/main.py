import os
import grpc
from concurrent import futures
import Roles.protos.roles_pb2 as roles_pb2
import Roles.protos.roles_pb2_grpc as roles_pb2_grpc
from Roles.repositories.rolGrupoRepository import RolGrupoRepository
from Roles.repositories.rolRecursoRepository import RolRecursoRepository
from Roles.models.recursoGrupoModel import RecursoGrupo
from Roles.database import SessionLocal, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

def seed_recursos():
    db = SessionLocal()
    recursos = [
        ("GRP_MOD", "Modificar información del grupo", "Permite cambiar nombre, descripción, privacidad e invitación"),
        ("MEM_INV", "Invitar y eliminar miembros", "Permite gestionar la membresía del grupo"),
        ("ROL_MNG", "Crear y modificar roles", "Permite gestionar los roles y permisos del grupo"),
        ("DSC_MNG", "Gestionar discusiones", "Permite crear, modificar y eliminar subgrupos"),
        ("GRP_DEL", "Eliminar grupo", "Permite la eliminación total de la comunidad (Solo Admin recomendado)"),
        ("MSG_DIR", "Enviar solicitudes de DM", "Permite contactar directamente a otros miembros")
    ]
    
    for id_rec, nombre, desc in recursos:
        if not db.query(RecursoGrupo).filter_by(id_recurso=id_rec).first():
            db.add(RecursoGrupo(id_recurso=id_rec, nombre_recurso=nombre, codigo_interno=id_rec))
    
    db.commit()
    db.close()

seed_recursos()

class RoleService(roles_pb2_grpc.RoleServiceServicer):
    # ... (rest of the class remains the same)
    def __init__(self):
        self.rol_repo = RolGrupoRepository()
        self.rol_recurso_repo = RolRecursoRepository()

    def GetRolesByGrupo(self, request, context):
        db = SessionLocal()
        roles = self.rol_repo.get_by_grupo(db, request.id_grupo)
        db.close()
        return roles_pb2.GetRolesByGrupoResponse(
            roles=[roles_pb2.RoleResponse(
                id_rol_grupo=r.id_rol_grupo,
                id_grupo=r.id_grupo,
                nombre=r.nombre,
                descripcion=r.descripcion or "",
                activo=r.activo
            ) for r in roles]
        )

    def GetRoleById(self, request, context):
        db = SessionLocal()
        role = self.rol_repo.get_by_id(db, request.id_rol_grupo)
        db.close()
        if not role:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Role not found')
            return roles_pb2.RoleResponse()
        return roles_pb2.RoleResponse(
            id_rol_grupo=role.id_rol_grupo,
            id_grupo=role.id_grupo,
            nombre=role.nombre,
            descripcion=role.descripcion or "",
            activo=role.activo
        )

    def CreateRole(self, request, context):
        db = SessionLocal()
        role_data = {
            "id_grupo": request.id_grupo,
            "nombre": request.nombre,
            "descripcion": request.descripcion
        }
        role = self.rol_repo.create(db, role_data)
        db.close()
        return roles_pb2.RoleResponse(
            id_rol_grupo=role.id_rol_grupo,
            id_grupo=role.id_grupo,
            nombre=role.nombre,
            descripcion=role.descripcion or "",
            activo=role.activo
        )

    def UpdateRole(self, request, context):
        db = SessionLocal()
        role = self.rol_repo.get_by_id(db, request.id_rol_grupo)
        if not role:
            db.close()
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return roles_pb2.RoleResponse()
        
        self.rol_repo.update(db, role, {
            "nombre": request.nombre,
            "descripcion": request.descripcion
        })
        db.commit()
        db.refresh(role)
        db.close()
        return roles_pb2.RoleResponse(
            id_rol_grupo=role.id_rol_grupo,
            id_grupo=role.id_grupo,
            nombre=role.nombre,
            descripcion=role.descripcion or "",
            activo=role.activo
        )

    def DeleteRole(self, request, context):
        db = SessionLocal()
        role = self.rol_repo.get_by_id(db, request.id_rol_grupo)
        if role:
            self.rol_repo.delete(db, role)
            db.commit()
            db.close()
            return roles_pb2.DeleteRoleResponse(success=True)
        db.close()
        return roles_pb2.DeleteRoleResponse(success=False)

    def AssignResourceToRole(self, request, context):
        print(f"DEBUG: AssignResourceToRole called with role: {request.id_rol_grupo}, resource: {request.id_recurso}")
        db = SessionLocal()
        try:
            # Verificar si ya existe
            existing = db.query(self.rol_recurso_repo.model).filter_by(
                id_rol_grupo=request.id_rol_grupo, 
                id_recurso=request.id_recurso
            ).first()
            
            if existing:
                print(f"DEBUG: Relationship already exists with ID: {existing.id_rol_recurso}")
                return roles_pb2.RoleResourceResponse(
                    id_rol_recurso=str(existing.id_rol_recurso),
                    id_rol_grupo=str(existing.id_rol_grupo),
                    id_recurso=str(existing.id_recurso)
                )

            data = {
                "id_rol_grupo": request.id_rol_grupo,
                "id_recurso": request.id_recurso
            }
            
            # Crear instancia manual
            from Roles.models.rolRecursoModel import RolRecurso
            from uuid6 import uuid7
            
            new_id = str(uuid7())
            rr = RolRecurso(
                id_rol_recurso=new_id,
                id_rol_grupo=request.id_rol_grupo,
                id_recurso=request.id_recurso
            )
            
            print(f"DEBUG: Attempting to insert new relationship ID: {new_id}")
            db.add(rr)
            db.commit()
            db.refresh(rr)
            
            print("DEBUG: Successfully inserted")
            return roles_pb2.RoleResourceResponse(
                id_rol_recurso=str(rr.id_rol_recurso),
                id_rol_grupo=str(rr.id_rol_grupo),
                id_recurso=str(rr.id_recurso)
            )
        except Exception as e:
            print(f"DEBUG ERROR: {str(e)}")
            db.rollback()
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return roles_pb2.RoleResourceResponse()
        finally:
            db.close()

    def RemoveResourceFromRole(self, request, context):
        db = SessionLocal()
        rr = db.query(self.rol_recurso_repo.model).filter_by(
            id_rol_grupo=request.id_rol_grupo,
            id_recurso=request.id_recurso
        ).first()
        if rr:
            db.delete(rr)
            db.commit()
            db.close()
            return roles_pb2.DeleteRoleResponse(success=True)
        db.close()
        return roles_pb2.DeleteRoleResponse(success=False)

    def GetResourcesByRole(self, request, context):
        db = SessionLocal()
        resources = self.rol_recurso_repo.get_by_rol(db, request.id_rol_grupo)
        db.close()
        return roles_pb2.GetResourcesByRoleResponse(
            resources=[roles_pb2.RoleResourceResponse(
                id_rol_recurso=r.id_rol_recurso,
                id_rol_grupo=r.id_rol_grupo,
                id_recurso=r.id_recurso
            ) for r in resources]
        )

    def GetAllResources(self, request, context):
        db = SessionLocal()
        recursos = db.query(RecursoGrupo).all()
        db.close()
        return roles_pb2.GetAllResourcesResponse(
            resources=[roles_pb2.ResourceResponse(
                id_recurso=r.id_recurso,
                nombre_recurso=r.nombre_recurso,
                codigo_interno=r.codigo_interno
            ) for r in recursos]
        )

def serve():
    port = os.getenv("ROLES_GRPC_PORT", "50051")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    roles_pb2_grpc.add_RoleServiceServicer_to_server(RoleService(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Roles gRPC server started on port {port}")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
