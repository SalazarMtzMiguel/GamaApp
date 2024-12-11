# Usa una imagen base de Python
FROM python:3.10-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia los archivos de requerimientos
COPY requirements.txt .

# Instala virtualenv y las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install virtualenv && \
    virtualenv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt && \
    pip list && \
    cat requirements.txt

# Instalar dependencias necesarias para Java y GAMA
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    wget \
    ca-certificates \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Configurar JAVA_HOME y actualizar PATH
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Descargar e instalar GAMA headless
RUN wget https://github.com/gama-platform/gama/releases/download/1.9.3/GAMA_1.9.3_Linux_with_JDK.deb -O /tmp/GAMA.deb && \
    dpkg -i /tmp/GAMA.deb && \
    rm /tmp/GAMA.deb

# Crear los directorios necesarios para GAMA
RUN mkdir -p /app/.workspace0/.metadata

# Copiar el script gama-headless.sh al directorio de trabajo
COPY gama-headless.sh /app/gama-headless.sh

# Establecer permisos de ejecución para el script
RUN chmod +x /app/gama-headless.sh

# Copia el código de la aplicación Django
COPY . .

# Expone el puerto 8000 para Django
EXPOSE 8000

# Comando para ejecutar Django
CMD ["sh", "-c", ". /app/venv/bin/activate && python manage.py migrate && daphne -b 0.0.0.0 -p 8000 GamaBackend.asgi:application"]