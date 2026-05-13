import os
import grpc
from Grupos.protos import auth_pb2 as auth_pb2
from Grupos.protos import auth_pb2_grpc as auth_pb2_grpc

class AuthClient:
    def __init__(self):
        host_port = os.getenv("AUTH_GRPC_SERVER", "localhost:50052")
        self.channel = grpc.insecure_channel(host_port)
        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def verify_token(self, token: str):
        request = auth_pb2.VerifyTokenRequest(token=token)
        return self.stub.VerifyToken(request)

    def get_user_by_email(self, email: str):
        request = auth_pb2.GetUserByEmailRequest(email=email)
        try:
            return self.stub.GetUserByEmail(request)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.NOT_FOUND:
                return None
            raise e
