# --- STAGE 1: Builder ---
FROM python:3.12-slim AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=2.0.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$PATH"

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libvips-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies (only project dependencies)
RUN poetry install --no-root --sync


# --- STAGE 2: Runtime ---
FROM python:3.12-slim AS runtime

WORKDIR /app

# Install runtime system dependencies
# ffmpeg: for video/audio processing
# libvips: for high-performance image engine
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libvips \
    && rm -rf /var/lib/apt/lists/*

# Copy installed python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create storage directories
RUN mkdir -p data/originals data/cache data/users

# Expose FastAPI default port
EXPOSE 8000

# Set environment defaults
ENV MORPHOSX_STORAGE_TYPE="local" \
    MORPHOSX_ENGINE_TYPE="pillow"

# Run the application
CMD ["uvicorn", "morphosx.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
