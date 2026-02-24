# morphosx 🧬
> **High performance, low footprint.**  
> Self-hosted, open-source media engine for on-the-fly image processing and delivery.

`morphosx` is a high-speed, minimal cloud storage and image manipulation server. Designed as a lightweight alternative to Cloudinary, it focuses on extreme efficiency, asynchronous processing, and secure distribution.

---

## ⚡ Features

- **On-the-fly Processing**: Resize, reformat (WebP, JPEG, PNG), and optimize images in memory.
- **Cyber-Security**: HMAC-SHA256 URL signing to prevent DoS attacks and unauthorized derivative generation.
- **Async Engine**: Built with **FastAPI** and **Pillow**, leveraging `aiofiles` for non-blocking I/O.
- **Derivative Caching**: Process once, serve forever. Intelligent caching of transformed variants.
- **Zero-Disk I/O Pipeline**: Image processing happens entirely in RAM using `BytesIO`.
- **Modular Storage**: Extensible storage backends (Local Filesystem ready, S3 planned).

## 🛠️ Tech Stack

- **Linguaggio**: Python 3.11+ (Strict typing)
- **Framework**: FastAPI (Asynchronous)
- **Processing**: Pillow (with future PyVips support)
- **Settings**: Pydantic-settings (Environment-based)
- **Formatter**: Black & isort

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have [Poetry](https://python-poetry.org/) installed.

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
curl -X POST "http://localhost:8000/v1/assets/upload" 
     -F "file=@your-image.jpg"
```
*Returns an `asset_id` and a signed URL.*

### Request a Variant
```text
GET /v1/assets/{asset_id}?width=300&format=webp&signature={hmac}
```

---

## 📁 Structure
```text
morphosx/
├── app/
│   ├── api/        # FastAPI Routers
│   ├── core/       # Security & Logic
│   ├── engine/     # Image Processing Engine
│   ├── storage/    # Storage Adapters (Local/S3)
│   └── settings.py # Centralized Config
└── data/           # Originals and Cache
```

## 📜 License
MIT - Built for the OSS community.
