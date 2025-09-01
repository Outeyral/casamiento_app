# Imagen base con Python 3.12
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements.txt y actualizar pip
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Crear carpeta de uploads si no existe
RUN mkdir -p uploads

# Exponer puerto que usará Flask (Render asigna un puerto por variable de entorno)
ENV PORT=10000
EXPOSE $PORT

# Variable de entorno para Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=$PORT

# Comando para correr la app
CMD ["flask", "run"]
