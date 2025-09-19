# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, fec, events

app = FastAPI(
    title="Choferes App Backend",
    description="La API para gestionar la logística de entregas.",
    version="1.0.0"
)

# Configurar CORS para permitir conexiones desde React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica las URLs permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(fec.router)
app.include_router(events.router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Endpoint principal que devuelve un mensaje de bienvenida.
    """
    return {"status": "ok", "message": "Backend de la App de Choferes está funcionando!"}