Plataforma de Chat Educativo

Una plataforma de chat educativo interactivo construida con React y Tailwind CSS.
La aplicación ofrece experiencias diferenciadas para estudiantes y docentes, incluyendo personajes interactivos, perfiles de usuario, paneles de control y herramientas de reporte.

✨ Funcionalidades

🔑 Sistema de autenticación (estudiantes y docentes)

💬 Chat interactivo con los personajes Teo y Josefina

📊 Panel de docente con gestión de estudiantes y reportes

🗂️ Panel de estudiante con perfil personalizado

📜 Historial de conversaciones descargable

✅ Validación avanzada de formularios

🎨 Interfaz moderna y responsiva con esquema de colores educativos

📱 Diseño completamente responsivo (móvil, tablet y escritorio)

🎨 Diseño

Gradiente de fondo: #E3F2FD → #BBDEFB → #90CAF9

Colores predominantes: tonos suaves de azul educativos

Tarjetas interactivas para los personajes

Burbujas modernas de chat

Barra de navegación fija con perfil de usuario

Animaciones suaves para mejorar la experiencia

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
