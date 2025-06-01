# ---- Build stage ----
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Poetry for dependency export (or use pip)
COPY pyproject.toml .
RUN pip install --upgrade pip && pip install poetry && poetry export -f requirements.txt --output requirements.txt --without-hashes

# Install runtime dependencies
RUN pip install -r requirements.txt --no-cache-dir

# ---- Runtime stage ----
FROM python:3.11-slim
WORKDIR /app

# Create non‑root user
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Copy installed packages and source code
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .

ENV PYTHONUNBUFFERED=1
ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
