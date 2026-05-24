FROM python:3.12-slim

WORKDIR /app

# Copie des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code et des données
COPY app/ ./app/
COPY data/ ./data/
COPY .env .

EXPOSE 8000

# Lancement de l'API 
CMD ["uvicorn", "app.fastapi_app:app", "--host", "0.0.0.0", "--port", "8000"]