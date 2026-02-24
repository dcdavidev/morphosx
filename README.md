<p align="center">
  <img src="morphosx-banner.png" alt="morphosx banner" width="600px">
</p>

# morphosx 🧬
> **High performance, low footprint.**  
> Self-hosted, open-source media engine for on-the-fly image processing and delivery.

`morphosx` is a high-speed, minimal cloud storage and media manipulation server. It focuses on extreme efficiency, asynchronous processing, and secure distribution across multiple media types.

---

## ⚡ Features

- **On-the-fly Image Processing**: Resize, reformat (WebP, JPEG, PNG), and optimize images in memory.
- **Video Thumbnails**: Extract high-quality frames from video files (MP4, WEBM, MOV, AVI) at any given timestamp.
- **Audio Waveforms**: Generate visual representations of audio tracks (MP3, WAV, OGG, FLAC) as processed images.
- **Document Rendering**: Convert PDF pages into crisp images for easy previewing.
- **RAW Development**: Professional RAW image decoding (CR2, NEF, DNG, ARW) with camera white-balance support.
- **Cyber-Security**: HMAC-SHA256 URL signing to prevent DoS attacks and unauthorized derivative generation.
- **Async Engine**: Built with **FastAPI**, leveraging `aiofiles` and non-blocking I/O.
- **Derivative Caching**: Process once, serve forever. Intelligent caching of transformed variants.
- **Zero-Disk I/O Pipeline**: Most transformations happen entirely in RAM using `BytesIO` buffers.

## 🛠️ Tech Stack

- **Language**: Python 3.11+ (Strict typing)
- **Framework**: FastAPI (Asynchronous)
- **Engines**: 
  - **Pillow**: Core image manipulation.
  - **FFmpeg**: Video frame extraction.
  - **PyMuPDF**: PDF rendering.
  - **rawpy**: Professional RAW decoding.
- **Settings**: Pydantic-settings (Environment-based)
- **Storage**: Extensible adapter system (Local Filesystem, S3 planned).

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have [Poetry](https://python-poetry.org/) and **FFmpeg** installed on your system.

### 2. Installation
```bash
git clone https://github.com/dcdavidev/morphosx.git
cd morphosx
poetry install
```

### 3. Setup Environment
Create a `.env` file or export variables:
```bash
MORPHOSX_SECRET_KEY="your-cyber-secret-key"
MORPHOSX_DEBUG=True
```

### 4. Run the Engine
```bash
poetry run start
```
The server will be available at `http://localhost:8000`.

---

## 🧪 API Usage

### Upload an Asset
```bash
curl -X POST "http://localhost:8000/v1/assets/upload" \
     -F "file=@your-media.jpg"
```
*Returns an `asset_id` and a signed URL.*

### Request a Variant
```text
GET /v1/assets/{asset_id}?width=300&format=webp&signature={hmac}
```

- **Video frame**: Add `time=2.5` to get the frame at 2.5 seconds.
- **PDF page**: Add `page=2` to render the second page.
- **Audio waveform**: Request a width/height to get the generated waveform.

---

## 📁 Structure
```text
morphosx/
├── app/
│   ├── api/        # FastAPI Routers
│   ├── core/       # Security & Logic
│   ├── engine/     # Specialized Engines (Video, Audio, PDF, RAW)
│   ├── storage/    # Storage Adapters (Local/S3)
│   └── settings.py # Centralized Config
└── data/           # Originals and Cache
```

## 📜 License
MIT - Built for the OSS community.
