# --- STAGE 1: Builder ---
FROM python:3.12-slim AS builder

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libvips-dev \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies first (layer caching)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --all-extras

# Copy source and install project
COPY . .
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --all-extras


# --- STAGE 2: Runtime ---
FROM python:3.12-slim AS runtime

WORKDIR /app

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libvips42 \
    curl \
    ca-certificates \
    gnupg \
    && curl -1sLf 'https://artifacts-cli.infisical.com/setup.deb.sh' | bash \
    && apt-get update && apt-get install -y infisical \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /app/.venv /app/.venv

# Add virtualenv to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set environment defaults
ENV MORPHOSX_PORT=6100 \
    MORPHOSX_STORAGE_TYPE="local" \
    MORPHOSX_ENGINE_TYPE="vips" \
    MORPHOSX_STORAGE_PATH="/app/storage"

# Create storage directories
RUN mkdir -p storage/originals storage/cache storage/users

# Expose FastAPI custom port
EXPOSE 6100

# Run the application
CMD ["uvicorn", "morphosx.app.main:app", "--host", "0.0.0.0", "--port", "6100"]
