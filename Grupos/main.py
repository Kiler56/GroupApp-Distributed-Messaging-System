import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Grupos.database import engine, Base, SessionLocal
from Grupos.routers import grupoRouter, usuariosGrupoRouter
from Grupos.models.tipoEstadoUsrGrpModel import TipoEstadoUsrGrp
from dotenv import load_dotenv

load_dotenv()

def seed_estados(db):


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
    uvicorn.run(app, host="0.0.0.0", port=8000)
