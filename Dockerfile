# ================================================
# Silicoscan — Dockerfile
# ================================================
# Sistem Skrining Paru-Paru AI untuk Silikosis
#
# Build:
#   docker build -t silicoscan .
#
# Run (CPU):
#   docker run -p 8000:8000 silicoscan
#
# Run (GPU - NVIDIA):
#   docker run --gpus all -p 8000:8000 silicoscan
# ================================================

FROM python:3.11-slim

# System dependencies for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Working directory
WORKDIR /app

# Copy requirements first (Docker cache optimization)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p uploads results models

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

# Run
CMD ["python", "app.py"]
