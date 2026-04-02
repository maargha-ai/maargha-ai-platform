# -------- STAGE 1: Builder --------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install only required build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# -------- STAGE 2: Runtime --------
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=user_service.settings

WORKDIR /app

# Runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project
COPY . .

# 👉 IMPORTANT FIX: move into correct Django folder
WORKDIR /app/user_service

# Create non-root user
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Collect static files
RUN python manage.py collectstatic --noinput --clear

EXPOSE 8080

# (Optional: remove if no /health endpoint exists)
# HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
#     CMD curl -f http://localhost:8080/health/ || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "--timeout", "120", "user_service.wsgi:application"]