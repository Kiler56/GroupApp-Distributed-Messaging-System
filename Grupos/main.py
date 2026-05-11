from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Grupos.database import engine, Base, SessionLocal
from Grupos.routers import grupoRouter, usuariosGrupoRouter
from Grupos.models.tipoEstadoUsrGrpModel import TipoEstadoUsrGrp

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
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_estados(db)
    finally:
        db.close()
    yield 

app = FastAPI(title="Servicio de Grupos", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(grupoRouter.router)
app.include_router(usuariosGrupoRouter.router)


@app.get("/")
def read_root():
    return {"message": "Servicio de Grupos funcionando"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
