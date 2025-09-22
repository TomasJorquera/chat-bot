import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, Query
from pydantic import BaseModel
from sqlalchemy import create_engine, text, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Session

app = FastAPI()

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
    # 1) guardamos el mensaje del usuario
    with Session(engine) as session:
        session.add(Message(role="user", content=req.message))
        session.commit()

    # 2) generamos respuesta (mock, porque no hay API key)
    reply = f"Recibí tu mensaje: '{req.message}' (modo mock 🤖)"

    # 3) guardamos la respuesta del asistente
    with Session(engine) as session:
        session.add(Message(role="assistant", content=reply))
        session.commit()

    return ChatResponse(response=reply)


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
