FROM python:3.12-slim

# Environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install build dependencies needed for some Python packages (bcrypt, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy application files (including model files)
COPY . /app

# Expose backend and frontend ports
EXPOSE 8000 8080

# Run both backend (uvicorn) and a simple static file server for the frontend.
# We run them in the same container for simplicity; both ports are exposed.
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 & python -m http.server 8080 --directory . & wait"]
