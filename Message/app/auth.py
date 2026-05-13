import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.protos import auth_pb2 as auth_pb2
from app.protos import auth_pb2_grpc as auth_pb2_grpc
import grpc
import sys

load_dotenv()

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    auth_grpc_server = os.getenv("AUTH_GRPC_SERVER", "127.0.0.1:50052")

    # Sync grpc client
    try:
        with grpc.insecure_channel(auth_grpc_server) as channel:
            stub = auth_pb2_grpc.AuthServiceStub(channel)
            request = auth_pb2.VerifyTokenRequest(token=token)
            
            try:
                response = stub.VerifyToken(request)
                
                return {
                    "user_id": response.user_id,
                    "username": response.username,
                    "email": response.email,
                    "token": token
                }
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                    raise HTTPException(status_code=401, detail="Invalid token")
                elif e.code() == grpc.StatusCode.NOT_FOUND:
                    raise HTTPException(status_code=404, detail="User not found")
                else:
                    raise HTTPException(status_code=503, detail="Auth service unavailable")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error during Auth")
