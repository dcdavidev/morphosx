# MorphosX - Asset Processing Engine

MorphosX is a high-performance asset processing engine designed to securely and efficiently manage, transform, and serve multimedia files.

## Main Features

- **On-the-fly Transformation**: Real-time image resizing, format conversion, and optimization.
- **Multi-Format Support**: Handles Images, Video (frame extraction), Audio (waveform), PDF Documents (page to image), 3D models, Office files, RAW, and more.
- **Integrated Security**: Protected via HMAC-SHA256 signatures to prevent abuse (DoS) and unauthorized access.
- **Flexible Storage**: Supports local file systems and Amazon S3 (or S3-compatible services like MinIO).
- **Private Assets**: Management of files linked to specific users with granular permissions.
- **Smart Caching**: Automatic derivative caching for ultra-fast response times.

## Architecture

MorphosX is built on:
- **FastAPI**: For a high-performance, asynchronous API interface.
- **Libvips / Pillow**: For low-latency image processing.
- **FFmpeg**: For video and audio support.
- **Poetry**: For Python dependency management.

## Quick Install (Docker)

```bash
docker build -t morphosx .
docker run -p 8000:8000 --env-file .env morphosx
```

The API will be available at `http://localhost:8000`.
Interactive documentation (Swagger) is available at `http://localhost:8000/docs`.
