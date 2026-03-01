# MorphosX Configuration

MorphosX can be configured via environment variables or a `.env` file. All settings are managed using Pydantic to ensure data validity.

## General Variables

- **`SECRET_KEY`**: (Mandatory) Secret key used for HMAC signature generation and validation.
- **`API_PREFIX`**: API endpoint prefix (e.g., `http://localhost:8000`).
- **`STORAGE_TYPE`**: Type of storage used (`local` or `s3`).
- **`STORAGE_PATH`**: Local path for asset storage (default: `./data`).
- **`ENGINE_TYPE`**: Image processing engine (`vips` or `pil`).

## S3 Configuration (if `STORAGE_TYPE=s3`)

- **`S3_BUCKET`**: Name of the S3 bucket.
- **`S3_REGION`**: AWS region.
- **`S3_ENDPOINT`**: S3 endpoint URL (required for MinIO or DigitalOcean Spaces).
- **`S3_ACCESS_KEY`**: S3 access key.
- **`S3_SECRET_KEY`**: S3 secret key.

## Image Processing Parameters

- **`DEFAULT_QUALITY`**: Default compression quality (default: `80`).
- **`MAX_IMAGE_DIMENSION`**: Maximum allowed size for `width` or `height` (default: `4000`).
- **`PRESETS`**: JSON string defining available presets.
  *Example*: `'{"thumb": {"width": 200, "height": 200, "format": "webp"}}'`

## Complete `.env` File Example

```bash
# Security
SECRET_KEY="a-very-secret-and-complex-key"
API_PREFIX="https://api.morphosx.io"

# Storage (S3 Example)
STORAGE_TYPE="s3"
S3_BUCKET="my-assets"
S3_REGION="eu-west-1"
S3_ACCESS_KEY="AKIA..."
S3_SECRET_KEY="abc123..."

# Engine
ENGINE_TYPE="vips"
DEFAULT_QUALITY=85
MAX_IMAGE_DIMENSION=5000

# Presets
PRESETS='{"avatar": {"width": 100, "height": 100, "format": "webp"}, "hero": {"width": 1920, "quality": 90}}'
```
