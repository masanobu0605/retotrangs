FROM python:3.13-slim
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
RUN mkdir -p /app/data

EXPOSE 8000
ENV DB_PATH=/app/data/app.db SESSION_SECRET=devsupersecret CORS_ORIGINS=http://localhost:3000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

