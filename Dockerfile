# --- Stage 1: Builder ---
FROM python:3.12-slim as builder

WORKDIR /app

# Prevent python from writing pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies required for building python packages
# (e.g. gcc for psycopg2, zlib for pillow)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and build wheels
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# --- Stage 2: Final ---
FROM python:3.12-slim

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install runtime dependencies (e.g. libpq for postgres, libjpeg for pillow)
RUN apt-get update && apt-get install -y \
    libpq-5 \
    libjpeg62-turbo \
    && rm -rf /var/lib/apt/lists/*

# Copy built wheels from builder stage
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy project code
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

EXPOSE 8000

# Use Gunicorn as the production server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "project.wsgi:application"]
