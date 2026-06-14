FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render injects $PORT at runtime; bind gunicorn to it.
CMD gunicorn app:app --bind 0.0.0.0:${PORT:-8000}
