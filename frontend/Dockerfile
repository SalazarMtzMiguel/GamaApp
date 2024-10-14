# Usa una imagen base de Node.js
FROM node:18-alpine

# Establece el directorio de trabajo
WORKDIR /app

# Instala Vue CLI globalmente
RUN npm install -g @vue/cli

# Crea un nuevo proyecto Vue.js (puedes personalizar el nombre y las opciones)
RUN vue create -p default my-app

# Cambia al directorio del proyecto
WORKDIR /app/my-app

# Compila la aplicación Vue.js para producción
RUN npm run build

# Expone el puerto 8080
EXPOSE 8080

# Comando para ejecutar el servidor de producción de Vue.js
CMD ["npm", "run", "serve"]
