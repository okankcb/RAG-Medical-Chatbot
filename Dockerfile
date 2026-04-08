FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY app/ ./app/
COPY vectorstore/ ./vectorstore/
COPY pyproject.toml .

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "app.application"]
