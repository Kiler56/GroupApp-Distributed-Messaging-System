import os
import sys
import grpc

# Asegurar que el directorio de protos sea accesible
PROTOS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'protos')
if PROTOS_DIR not in sys.path:
    sys.path.insert(0, PROTOS_DIR)

import auth_pb2 as auth_pb2
import auth_pb2_grpc as auth_pb2_grpc

class AuthClient:
    def __init__(self):
        host = os.getenv("AUTH_SERVICE_HOST", "localhost")
        port = os.getenv("AUTH_GRPC_PORT", "50052")
        self.channel = grpc.insecure_channel(f'{host}:{port}')
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def get_user_by_email(self, email: str):
        request = auth_pb2.GetUserByEmailRequest(email=email)
        try:
            return self.stub.GetUserByEmail(request)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise e
