import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Session

app = FastAPI()

# --- Orígenes permitidos para CORS ---
# En producción, deberías limitar esto a tu dominio de frontend.
# Ejemplo: origins = ["http://tu-dominio.com", "https://tu-dominio.com"]
origins = [
    "*" # Temporalmente para el despliegue inicial, luego lo cambiaremos por el dominio real.
]

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# --- DB ---
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://admin:admin@db:5432/chatbotdb")
engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(20), nullable=False)          # "user" | "assistant"
    content = Column(String(4000), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

# crea la tabla si no existe
Base.metadata.create_all(engine)


# --- Schemas ---
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str


# --- Endpoints básicos ---
@app.get("/")
def read_root():
    return {"msg": "Chatbot docente activo 🚀"}

@app.get("/db-test")
def test_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW()")).fetchone()
        return {"db_time": str(result[0])}


# --- Chat (mock) + persistencia ---
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        # 1) guardamos el mensaje del usuario
        with Session(engine) as session:
            user_message = Message(role="user", content=req.message)
            session.add(user_message)
            session.commit()

        # 2) generamos respuesta (mock, porque no hay API key)
        reply = f"Recibí tu mensaje: '{req.message}' (modo mock 🤖)"

        # 3) guardamos la respuesta del asistente
        with Session(engine) as session:
            assistant_message = Message(role="assistant", content=reply)
            session.add(assistant_message)
            session.commit()

        return ChatResponse(response=reply)
    except Exception as e:
        # Log the exception e
        raise HTTPException(status_code=500, detail="Error al procesar el mensaje en el chat.")


# --- Historial ---
@app.get("/messages")
def list_messages(limit: int = Query(20, ge=1, le=100)):
    with Session(engine) as session:
        rows = session.query(Message).order_by(Message.id.desc()).limit(limit).all()
        return [
            {
                "id": r.id,
                "role": r.role,
                "content": r.content,
                "created_at": r.created_at.isoformat()
            }
            for r in rows
        ]
