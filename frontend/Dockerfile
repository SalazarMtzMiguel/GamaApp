# Usa una imagen base de Node.js
FROM node:18-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo package.json y package-lock.json (si está disponible)
COPY package.json ./

# Instala las dependencias del proyecto
RUN npm install

# Copia el código de la aplicación Vue.js
COPY . .

# Expone el puerto 8080
EXPOSE 8080

# Comando para ejecutar el servidor de desarrollo de Vue.js
CMD ["npm", "run", "serve"]
