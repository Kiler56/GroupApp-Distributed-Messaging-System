import os
import grpc
import Roles.protos.roles_pb2 as roles_pb2
import Roles.protos.roles_pb2_grpc as roles_pb2_grpc

from Grupos.config import ROLES_SERVICE_HOST, ROLES_SERVICE_PORT

class RolesClient:
    def __init__(self):
        host = ROLES_SERVICE_HOST
        port = ROLES_SERVICE_PORT
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = roles_pb2_grpc.RoleServiceStub(self.channel)

    def get_roles_by_grupo(self, id_grupo: str):
        request = roles_pb2.GetRolesByGrupoRequest(id_grupo=id_grupo)
        return self.stub.GetRolesByGrupo(request).roles

    def get_role_by_id(self, id_rol_grupo: str):
        request = roles_pb2.GetRoleByIdRequest(id_rol_grupo=id_rol_grupo)
        try:
            return self.stub.GetRoleById(request)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise e

    def create_role(self, id_grupo: str, nombre: str, descripcion: str = ""):
        request = roles_pb2.CreateRoleRequest(id_grupo=id_grupo, nombre=nombre, descripcion=descripcion)
        return self.stub.CreateRole(request)

    def update_role(self, id_rol_grupo: str, nombre: str, descripcion: str = ""):
        request = roles_pb2.UpdateRoleRequest(id_rol_grupo=id_rol_grupo, nombre=nombre, descripcion=descripcion)
        return self.stub.UpdateRole(request)

    def delete_role(self, id_rol_grupo: str):
        request = roles_pb2.DeleteRoleRequest(id_rol_grupo=id_rol_grupo)
        return self.stub.DeleteRole(request).success

    def assign_resource_to_role(self, id_rol_grupo: str, id_recurso: str):
        request = roles_pb2.AssignResourceRequest(id_rol_grupo=id_rol_grupo, id_recurso=id_recurso)
        return self.stub.AssignResourceToRole(request)

    def remove_resource_from_role(self, id_rol_grupo: str, id_recurso: str):
        request = roles_pb2.RemoveResourceRequest(id_rol_grupo=id_rol_grupo, id_recurso=id_recurso)
        return self.stub.RemoveResourceFromRole(request).success

    def get_resources_by_role(self, id_rol_grupo: str):
        request = roles_pb2.GetResourcesByRoleRequest(id_rol_grupo=id_rol_grupo)
        return self.stub.GetResourcesByRole(request).resources

    def get_all_resources(self):
        request = roles_pb2.Empty()
        return self.stub.GetAllResources(request).resources
