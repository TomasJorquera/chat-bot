FROM python:3.11

# Directorio de trabajo
WORKDIR /code

# 1) Instalar dependencias desde el requirements de la carpeta interna
COPY ./backend/backend/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copiar el código de la carpeta interna
COPY ./backend/backend /code/

# 3) Ejecutar la app (ahora sí hay /code/main.py)
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
