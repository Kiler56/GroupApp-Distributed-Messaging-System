from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import grpc
import os
import sys

# Asegurar que los archivos generados se pueden importar
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import app.auth_pb2 as auth_pb2
import app.auth_pb2_grpc as auth_pb2_grpc

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # Conectar al servicio de Auth vía gRPC
        with grpc.insecure_channel('127.0.0.1:50052') as channel:
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
        print("Auth error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error during Auth")
