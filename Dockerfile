
# Pull official base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
# libpq-dev is for postgres, libjpeg/zlib for pillow
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN addgroup --system app && adduser --system --group app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/
RUN chown -R app:app /app

# Copy and setup entrypoint
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh && chown app:app /app/entrypoint.sh

# Switch to non-root user
USER app

# Expose port
EXPOSE 8000

# Command to run the application
ENTRYPOINT ["/app/entrypoint.sh"]
