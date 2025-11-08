# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /app

# System deps (optional but useful)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python deps first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY main_server.py agent_logic.py chatbot_frontend.html ./

# Environment
ENV PYTHONUNBUFFERED=1
# Default Java API inside compose
ENV JAVA_API_BASE_URL="http://java-stock-api:8080/api/v1/stock"

EXPOSE 8000

CMD ["uvicorn", "main_server:app", "--host", "0.0.0.0", "--port", "8000"]
