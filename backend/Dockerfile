# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requerimientos
COPY requirements.txt .

# Instala virtualenv y las dependencias
RUN pip install virtualenv && \
    virtualenv venv && \
    pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación Django
COPY . .

# Expone el puerto 8000 para Django
EXPOSE 8000

# Comando para ejecutar Django
CMD ["sh", "-c", ". /app/venv/bin/activate && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 GamaBackend.wsgi:application"]