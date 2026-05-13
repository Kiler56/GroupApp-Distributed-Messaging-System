from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from Grupos.config.database import engine, Base, SessionLocal
from Grupos.routers import grupoRouter, usuariosGrupoRouter
from Grupos.models.tipoEstadoUsrGrpModel import TipoEstadoUsrGrp
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        estados = ["ACTIVO", "INACTIVO", "PENDIENTE"]
        for nombre in estados:
            if not db.query(TipoEstadoUsrGrp).filter_by(nombre=nombre).first():
                db.add(TipoEstadoUsrGrp(id_estado=nombre, nombre=nombre))
        db.commit()
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()
    yield

app = FastAPI(title="Servicio de Grupos", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
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
    uvicorn.run("Grupos.main:app", host="0.0.0.0", port=8000, reload=True)
