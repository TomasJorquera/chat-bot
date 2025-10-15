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

# ✅ CLAVE PEGADA (temporal). Sustituye por tu key válida:
GEMINI_API_KEY = "AIzaSyBfXvOOqYmVEC5NvFpbsZKsp6YcuN_RKu0"

# Config y modelo
genai.configure(api_key=GEMINI_API_KEY)
PRIMARY_MODEL = "gemini-2.5-flash"
FALLBACK_MODEL = "gemini-1.5-flash"

def get_model():
    # Si 2.5 no está habilitado en tu cuenta, cae a 1.5 automáticamente
    try:
        return genai.GenerativeModel(PRIMARY_MODEL)
    except Exception:
        return genai.GenerativeModel(FALLBACK_MODEL)

model = get_model()

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
    role = Column(String(20), nullable=False)  # "user" | "assistant" | "error"
    content = Column(String(4000), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

# crea la tabla si no existe
Base.metadata.create_all(engine)

# --- Schemas ---
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

MAX_STORE = 3900  # margen para no pasar 4000 chars en DB
MAX_REPLY = 3000  # por si el modelo devuelve mucho texto

# --- Endpoints básicos ---
@app.get("/")
def read_root():
    return {"msg": "Chatbot docente activo 🚀 (Gemini conectado)"}

@app.get("/db-test")
def test_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW()")).fetchone()
        return {"db_time": str(result[0])}

# --- Chat + persistencia ---
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        # 1) Guarda mensaje del usuario
        with Session(engine) as session:
            session.add(Message(role="user", content=req.message[:MAX_STORE]))
            session.commit()

        # 2) Llama a Gemini (robusto y con fallback)
        prompt = (
            f"Eres un asistente educativo que responde de forma amable, breve y clara. "
            f"Pregunta del usuario: {req.message}"
        )
        reply = "…"  # fallback breve

        # intento con el modelo actual
        try:
            r = model.generate_content(prompt)
            text_out = (r.text or "").strip() if hasattr(r, "text") else ""
            if not text_out:
                # reintento con fallback model
                r2 = genai.GenerativeModel(FALLBACK_MODEL).generate_content(prompt)
                text_out = (r2.text or "").strip() if hasattr(r2, "text") else ""
            if text_out:
                reply = text_out[:MAX_REPLY]
        except Exception as err:
            # loguea error pero no rompas la UX
            with Session(engine) as session:
                session.add(Message(role="error", content=f"Gemini error: {str(err)[:MAX_STORE]}"))
                session.commit()

        # 3) Guarda respuesta del asistente
        with Session(engine) as session:
            session.add(Message(role="assistant", content=reply[:MAX_STORE]))
            session.commit()

        return ChatResponse(response=reply[:MAX_REPLY])

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
