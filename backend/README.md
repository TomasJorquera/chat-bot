Chatbot Docente – Backend

Proyecto de PMV para el chatbot docente.
Incluye un backend con FastAPI y una base de datos PostgreSQL, todo en Docker.

Estado actual

Backend en FastAPI con endpoints de prueba.
Base de datos PostgreSQL integrada.
Endpoint /chat en modo mock (responde con mensajes simples).
Swagger UI disponible en http://localhost:8000/docs.

Instrucciones de uso

Clonar el repositorio:
git clone https://github.com/nriosgamboa/chatbot-docente.git
cd chatbot-docente

Levantar el proyecto:
docker compose up --build

El backend queda funcionando en http://localhost:8000.
