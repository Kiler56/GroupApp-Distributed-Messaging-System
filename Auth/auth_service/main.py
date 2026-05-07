from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth_service.database import engine, Base, SessionLocal
from auth_service import auth
from fastapi.middleware.cors import CORSMiddleware
import threading
import grpc
import sys
import os
from concurrent import futures

from auth_service.config import GRPC_PORT, ALLOWED_ORIGINS

# Añadir el directorio actual al path para que gRPC encuentre los módulos generados
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import auth_pb2 as auth_pb2
import auth_pb2_grpc as auth_pb2_grpc
from auth_service.models import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # Arrancar servidor gRPC en un hilo aparte
    threading.Thread(target=serve_grpc, daemon=True).start()
    yield 

class AuthGRPCService(auth_pb2_grpc.AuthServiceServicer):
    def GetUserByEmail(self, request, context):
        db = SessionLocal()
        user = db.query(User).filter(User.email == request.email).first()
        db.close()
        if not user:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('User not found')
            return auth_pb2.UserResponse()
        return auth_pb2.UserResponse(
            id_usuario=user.id_usuario,
            username=user.username,
            email=user.email
        )

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthGRPCService(), server)
    server.add_insecure_port(f'[::]:{GRPC_PORT}')
    server.start()
    print(f"Auth gRPC server started on port {GRPC_PORT}")
    server.wait_for_termination()

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def root():
    return {"message": "Auth service running"}