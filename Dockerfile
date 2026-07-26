FROM python:3.10-slim

WORKDIR /app

# Instalar dependencias del sistema requeridas por algunas librerías
RUN apt-get update && apt-get install -y \
    build-essential \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente y los documentos
COPY src/ ./src/
COPY docs/ ./docs/

WORKDIR /app/src

EXPOSE 8501

# Comando para ejecutar la app Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
