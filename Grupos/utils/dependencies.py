from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import grpc
import os
from Grupos.protos import auth_pb2 as auth_pb2
from Grupos.protos import auth_pb2_grpc as auth_pb2_grpc
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=os.getenv("AUTH_SERVICE_URL", "http://localhost:8000") + "/auth/login")

AUTH_GRPC_SERVER = os.getenv("AUTH_GRPC_SERVER", "localhost:50052")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Async grpc connection for FastAPI support
        async with grpc.aio.insecure_channel(AUTH_GRPC_SERVER) as channel:
            stub = auth_pb2_grpc.AuthServiceStub(channel)
            request = auth_pb2.VerifyTokenRequest(token=token)
            
            try:
                response = await stub.VerifyToken(request)
                return response.user_id
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                    raise HTTPException(status_code=401, detail="Token invalido o expirado")
                else:
                    raise HTTPException(status_code=503, detail="Servicio de autenticacion no disponible")
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error en el servicio de autenticacion")
