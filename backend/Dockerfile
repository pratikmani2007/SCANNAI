# SCANNAI Backend Dockerfile
# Python 3.12 Slim base for minimal footprint and enhanced security
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ENVIRONMENT=production \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR /app

# Install security updates
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pinned dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY . .

# Ensure storage directories exist with appropriate permissions
RUN mkdir -p storage/uploads storage/reports storage/temp

# Create non-root user for principle of least privilege
RUN useradd -m -u 1001 scannai && chown -R scannai:scannai /app
USER scannai

EXPOSE 8000

# Healthcheck probe
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
