import os
from datetime import datetime
from typing import List

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, Session

# --- Gemini ---
import google.generativeai as genai

# Aqui esta la API key de Gemini
GEMINI_API_KEY = "AIzaSyC_Cc0CatwLXuXhn-gd0nv9yQyR19xugyU"

# Configuración del modelo Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")  # ← modelo nuevo y recomendado

# --- App FastAPI ---
app = FastAPI()

# --- CORS ---
origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DB ---
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://admin:admin@db:5432/chatbotdb"
)
engine = create_engine(DATABASE_URL, future=True, pool_pre_ping=True)

Base = declarative_base()

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(String(20), nullable=False)  # "user" | "assistant"
    content = Column(String(4000), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

# Crea la tabla si no existe
Base.metadata.create_all(engine)

# --- Schemas ---
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

# --- Endpoints ---
@app.get("/")
def read_root():
    return {"msg": "Chatbot docente activo 🚀 (Gemini 2.5 conectado)"}


@app.get("/db-test")
def test_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW()")).fetchone()
        return {"db_time": str(result[0])}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        # 1️ Guardamos el mensaje del usuario
        with Session(engine) as session:
            user_message = Message(role="user", content=req.message)
            session.add(user_message)
            session.commit()

        # 2️ Generamos respuesta con Gemini
        prompt = f"Eres un asistente educativo que responde de forma amable, breve y clara. Pregunta del usuario: {req.message}"
        response = model.generate_content(prompt)
        reply = response.text.strip() if response and hasattr(response, "text") else "No entendí bien la pregunta 🤔"

        # 3️ Guardamos la respuesta del asistente
        with Session(engine) as session:
            assistant_message = Message(role="assistant", content=reply)
            session.add(assistant_message)
            session.commit()

        return ChatResponse(response=reply)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en el chat: {str(e)}")


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
