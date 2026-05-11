# -*- coding: utf-8 -*-
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import grpc
import os
import sys

# Asegurar que los archivos generados se pueden importar
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import auth_pb2 as auth_pb2
import auth_pb2_grpc as auth_pb2_grpc

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/auth/login")

# Dirección del servicio gRPC de Auth
AUTH_GRPC_SERVER = os.getenv("AUTH_GRPC_SERVER", "localhost:50052")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Conexión gRPC
        # Se elimina el bloque "with" que creaba el canal de forma síncrona
        # y se usa grpc.aio para soporte asíncrono nativo en FastAPI
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
        print("Auth error:", e)
        raise HTTPException(status_code=500, detail="Error en el servicio de autenticacion")
