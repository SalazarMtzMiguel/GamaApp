# Dockerfile para GAMA Headless
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar dependencias necesarias
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

# Listar los archivos en el sistema de archivos para verificar la ubicación del script
RUN find / -name "gama-headless.sh"


# Crear los directorios necesarios para GAMA
RUN mkdir -p /working_dir/.workspace0/.metadata

# Establecer el directorio de trabajo
WORKDIR /working_dir

# Comando por defecto para ejecutar el contenedor
ENTRYPOINT ["gama-headless"]
CMD ["-socket", "6868"]