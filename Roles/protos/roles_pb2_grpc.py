
import grpc
import warnings

from Roles.protos import roles_pb2 as Roles_dot_protos_dot_roles__pb2

GRPC_GENERATED_VERSION = '1.80.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + ' but the generated code in Roles/protos/roles_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class RoleServiceStub(object):

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetRolesByGrupo = channel.unary_unary(
                '/roles.RoleService/GetRolesByGrupo',
                request_serializer=Roles_dot_protos_dot_roles__pb2.GetRolesByGrupoRequest.SerializeToString,
                response_deserializer=Roles_dot_protos_dot_roles__pb2.GetRolesByGrupoResponse.FromString,
                _registered_method=True)
        self.GetRoleById = channel.unary_unary(
                '/roles.RoleService/GetRoleById',
                request_serializer=Roles_dot_protos_dot_roles__pb2.GetRoleByIdRequest.SerializeToString,
                response_deserializer=Roles_dot_protos_dot_roles__pb2.RoleResponse.FromString,
                _registered_method=True)
        self.CreateRole = channel.unary_unary(
                '/roles.RoleService/CreateRole',
                request_serializer=Roles_dot_protos_dot_roles__pb2.CreateRoleRequest.SerializeToString,
                response_deserializer=Roles_dot_protos_dot_roles__pb2.RoleResponse.FromString,
                _registered_method=True)
        self.UpdateRole = channel.unary_unary(
                '/roles.RoleService/UpdateRole',
                request_serializer=Roles_dot_protos_dot_roles__pb2.UpdateRoleRequest.SerializeToString,
                response_deserializer=Roles_dot_protos_dot_roles__pb2.RoleResponse.FromString,
                _registered_method=True)
        self.DeleteRole = channel.unary_unary(
                '/roles.RoleService/DeleteRole',
                request_serializer=Roles_dot_protos_dot_roles__pb2.DeleteRoleRequest.SerializeToString,
                response_deserializer=Roles_dot_protos_dot_roles__pb2.DeleteRoleResponse.FromString,
                _registered_method=True)
        self.AssignResourceToRole = channel.unary_unary(
                '/roles.RoleService/AssignResourceToRole',
                request_serializer=Roles_dot_protos_dot_roles__pb2.AssignResourceRequest.SerializeToString,
                response_deserializer=Roles_dot_protos_dot_roles__pb2.RoleResourceResponse.FromString,
                _registered_method=True)
        self.RemoveResourceFromRole = channel.unary_unary(
                '/roles.RoleService/RemoveResourceFromRole',
                request_serializer=Roles_dot_protos_dot_roles__pb2.RemoveResourceRequest.SerializeToString,
                response_deserializer=Roles_dot_protos_dot_roles__pb2.DeleteRoleResponse.FromString,
                _registered_method=True)
        self.GetResourcesByRole = channel.unary_unary(
                '/roles.RoleService/GetResourcesByRole',
                request_serializer=Roles_dot_protos_dot_roles__pb2.GetResourcesByRoleRequest.SerializeToString,
                response_deserializer=Roles_dot_protos_dot_roles__pb2.GetResourcesByRoleResponse.FromString,
                _registered_method=True)
        self.GetAllResources = channel.unary_unary(
                '/roles.RoleService/GetAllResources',
                request_serializer=Roles_dot_protos_dot_roles__pb2.Empty.SerializeToString,
                response_deserializer=Roles_dot_protos_dot_roles__pb2.GetAllResourcesResponse.FromString,
                _registered_method=True)


class RoleServiceServicer(object):

    def GetRolesByGrupo(self, request, context):

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetRoleById(self, request, context):

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateRole(self, request, context):

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateRole(self, request, context):

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteRole(self, request, context):

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AssignResourceToRole(self, request, context):

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RemoveResourceFromRole(self, request, context):

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetResourcesByRole(self, request, context):

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllResources(self, request, context):

        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RoleServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetRolesByGrupo': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRolesByGrupo,
                    request_deserializer=Roles_dot_protos_dot_roles__pb2.GetRolesByGrupoRequest.FromString,
                    response_serializer=Roles_dot_protos_dot_roles__pb2.GetRolesByGrupoResponse.SerializeToString,
            ),
            'GetRoleById': grpc.unary_unary_rpc_method_handler(
                    servicer.GetRoleById,
                    request_deserializer=Roles_dot_protos_dot_roles__pb2.GetRoleByIdRequest.FromString,
                    response_serializer=Roles_dot_protos_dot_roles__pb2.RoleResponse.SerializeToString,
            ),
            'CreateRole': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateRole,
                    request_deserializer=Roles_dot_protos_dot_roles__pb2.CreateRoleRequest.FromString,
                    response_serializer=Roles_dot_protos_dot_roles__pb2.RoleResponse.SerializeToString,
            ),
            'UpdateRole': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateRole,
                    request_deserializer=Roles_dot_protos_dot_roles__pb2.UpdateRoleRequest.FromString,
                    response_serializer=Roles_dot_protos_dot_roles__pb2.RoleResponse.SerializeToString,
            ),
            'DeleteRole': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteRole,
                    request_deserializer=Roles_dot_protos_dot_roles__pb2.DeleteRoleRequest.FromString,
                    response_serializer=Roles_dot_protos_dot_roles__pb2.DeleteRoleResponse.SerializeToString,
            ),
            'AssignResourceToRole': grpc.unary_unary_rpc_method_handler(
                    servicer.AssignResourceToRole,
                    request_deserializer=Roles_dot_protos_dot_roles__pb2.AssignResourceRequest.FromString,
                    response_serializer=Roles_dot_protos_dot_roles__pb2.RoleResourceResponse.SerializeToString,
            ),
            'RemoveResourceFromRole': grpc.unary_unary_rpc_method_handler(
                    servicer.RemoveResourceFromRole,
                    request_deserializer=Roles_dot_protos_dot_roles__pb2.RemoveResourceRequest.FromString,
                    response_serializer=Roles_dot_protos_dot_roles__pb2.DeleteRoleResponse.SerializeToString,
            ),
            'GetResourcesByRole': grpc.unary_unary_rpc_method_handler(
                    servicer.GetResourcesByRole,
                    request_deserializer=Roles_dot_protos_dot_roles__pb2.GetResourcesByRoleRequest.FromString,
                    response_serializer=Roles_dot_protos_dot_roles__pb2.GetResourcesByRoleResponse.SerializeToString,
            ),
            'GetAllResources': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllResources,
                    request_deserializer=Roles_dot_protos_dot_roles__pb2.Empty.FromString,
                    response_serializer=Roles_dot_protos_dot_roles__pb2.GetAllResourcesResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'roles.RoleService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('roles.RoleService', rpc_method_handlers)


class RoleService(object):

    @staticmethod
    def GetRolesByGrupo(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/roles.RoleService/GetRolesByGrupo',
            Roles_dot_protos_dot_roles__pb2.GetRolesByGrupoRequest.SerializeToString,
            Roles_dot_protos_dot_roles__pb2.GetRolesByGrupoResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetRoleById(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/roles.RoleService/GetRoleById',
            Roles_dot_protos_dot_roles__pb2.GetRoleByIdRequest.SerializeToString,
            Roles_dot_protos_dot_roles__pb2.RoleResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CreateRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/roles.RoleService/CreateRole',
            Roles_dot_protos_dot_roles__pb2.CreateRoleRequest.SerializeToString,
            Roles_dot_protos_dot_roles__pb2.RoleResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/roles.RoleService/UpdateRole',
            Roles_dot_protos_dot_roles__pb2.UpdateRoleRequest.SerializeToString,
            Roles_dot_protos_dot_roles__pb2.RoleResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/roles.RoleService/DeleteRole',
            Roles_dot_protos_dot_roles__pb2.DeleteRoleRequest.SerializeToString,
            Roles_dot_protos_dot_roles__pb2.DeleteRoleResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AssignResourceToRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/roles.RoleService/AssignResourceToRole',
            Roles_dot_protos_dot_roles__pb2.AssignResourceRequest.SerializeToString,
            Roles_dot_protos_dot_roles__pb2.RoleResourceResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def RemoveResourceFromRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/roles.RoleService/RemoveResourceFromRole',
            Roles_dot_protos_dot_roles__pb2.RemoveResourceRequest.SerializeToString,
            Roles_dot_protos_dot_roles__pb2.DeleteRoleResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetResourcesByRole(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/roles.RoleService/GetResourcesByRole',
            Roles_dot_protos_dot_roles__pb2.GetResourcesByRoleRequest.SerializeToString,
            Roles_dot_protos_dot_roles__pb2.GetResourcesByRoleResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetAllResources(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/roles.RoleService/GetAllResources',
            Roles_dot_protos_dot_roles__pb2.Empty.SerializeToString,
            Roles_dot_protos_dot_roles__pb2.GetAllResourcesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

