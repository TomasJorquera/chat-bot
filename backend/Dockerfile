FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /code

# Copia solo el archivo de dependencias primero para aprovechar el cache de Docker
COPY ./backend/requirements.txt /code/requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu aplicación
COPY ./backend /code/

# 👇 Ejecuta uvicorn vía Python para evitar problemas de PATH
# Render espera que el servicio se ejecute en el puerto 10000.
# El flag --reload no se recomienda para producción.
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
