# Usamos la imagen base oficial de Python 3.12 slim
FROM python:3.12-slim

# Establecemos el directorio de trabajo
WORKDIR /app

# Instalamos dependencias del sistema necesarias para Pillow y otras librerías
RUN apt-get update && apt-get install -y \
    build-essential \
    zlib1g-dev \
    libjpeg-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev tk8.6-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiamos los requirements
COPY requirements.txt .

# Actualizamos pip
RUN pip install --upgrade pip

# Instalamos las dependencias de Python
RUN pip install -r requirements.txt

# Copiamos el resto del código
COPY . .

# Comando por defecto para correr la app
CMD ["python", "app.py"]
