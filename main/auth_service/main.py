from contextlib import asynccontextmanager
from fastapi import FastAPI
from auth_service.database import engine, Base, SessionLocal
from backend.grupos.routers import grupoRouter, usuariosGrupoRouter
from auth_service import auth
from backend.grupos.models.grupoModel import Grupo
from backend.grupos.models.usuariosGrupoModel import UsuariosGrupo
from backend.grupos.models.rolGrupoModel import RolGrupo
from backend.grupos.models.tipoEstadoUsrGrpModel import TipoEstadoUsrGrp
from fastapi.middleware.cors import CORSMiddleware

def seed_estados(db):
    estados = [
        TipoEstadoUsrGrp(id_estado="ACTIVO", nombre="Activo"),
        TipoEstadoUsrGrp(id_estado="INACTIVO", nombre="Inactivo"),
    ]

    for estado in estados:
        if not db.query(TipoEstadoUsrGrp).filter_by(id_estado=estado.id_estado).first():
            db.add(estado)

    db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Tablas registradas:", list(Base.metadata.tables.keys()))
    
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_estados(db)
    finally:
        db.close()
        
    yield 

app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # para pruebas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(grupoRouter.router, prefix="/groups")
app.include_router(usuariosGrupoRouter.router, prefix="/users-groups")
app.include_router(auth.router, prefix="/auth")

@app.get("/")
def root():
    return {"message": "Users service running"}