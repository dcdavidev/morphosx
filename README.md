<p align="center">
  <img src="morphosx-banner.png" alt="morphosx banner" width="600px">
</p>

# morphosx 🧬
> **High performance, low footprint.**  
> Self-hosted, open-source media engine for on-the-fly image processing and delivery.

`morphosx` is a high-performance media processing server designed to convert almost any file type into web-optimized image derivatives in real-time. It handles storage, security via HMAC signatures, and efficient distribution of multimedia assets.

---

## ⚡ Core Features

### 🖼️ Universal Image Engine
- **Live Transformations**: Resizing, format switching, and in-memory compression.
- **Modern Formats**: Native support for **HEIC/HEIF** (iPhone) and **AVIF** (Next-gen).
- **RAW Development**: Professional processing of photographic raw files (**CR2, NEF, DNG, ARW**) with camera white balance support.
- **Vector Rendering**: Raster preview generation from **SVG** files.

### 🎬 Media & Documents
- **Video Thumbnails**: High-precision frame extraction from **MP4, WEBM, MOV, AVI** using the `time` parameter.
- **Audio Waveforms**: Visual waveform generation for **MP3, WAV, OGG, FLAC**.
- **PDF Rendering**: Conversion of specific pages into sharp images (using the `page` parameter).
- **Office Cards**: Summary card generation for **DOCX, PPTX, XLSX** with key text extraction.

### 🏗️ Engineering & Design
- **BIM Technical Cards**: Architectural metadata extraction (walls, floors, windows) from **IFC** files.
- **3D Blueprints**: Technical sheets with bounding boxes and metadata for **STL, OBJ, GLB, GLTF**.
- **Font Specimen**: Generation of complete typographic specimens from **TTF** and **OTF** files.
- **Archive Explorer**: Content visualization for **ZIP** and **TAR** archives in a "folder preview" format.

### 🚀 Performance & Architecture
- **Dual Engine**: Choose between **Pillow** (stability) or **PyVips** (extreme speed for large files) via `MORPHOSX_ENGINE_TYPE`.
- **Modular Storage**: Support for **Local Filesystem** and **Amazon S3** (or S3-compatible providers like MinIO/DigitalOcean).
- **Zero-Disk I/O**: Entire processing pipeline runs in RAM using `BytesIO` buffers.
- **Intelligent Caching**: Derivatives are computed once and served instantly for subsequent requests.

---

## 🛡️ Security: HMAC-SHA256
MorphosX protects your resources by preventing unauthorized variant generation (protecting against DoS attacks). Every URL must be signed with an HMAC that includes:
`asset_id | width | height | format | quality | preset`

---

## ✨ Smart Presets
Instead of sending complex parameters, you can use predefined aliases in `settings.py`:
- `preset=thumb`: 150x150 WebP (Ideal for avatars/thumbnails).
- `preset=hero`: 1920px WebP (Ideal for banners).
- `preset=social`: 1200x630 JPEG (Ideal for OpenGraph/Social sharing).

---

## 🚀 Quick Start

### 1. Prerequisites
- **Python 3.11 - 3.14**
- **FFmpeg** (for video and audio)
- **libvips** (optional, for ultra-high performance)

### 2. Installation
```bash
git clone https://github.com/dcdavidev/morphosx.git
cd morphosx
poetry install
```

### 3. Configuration (.env)
```bash
MORPHOSX_SECRET_KEY="your-cyber-secret"
MORPHOSX_STORAGE_TYPE="local" # or "s3"
MORPHOSX_ENGINE_TYPE="pillow" # or "vips"
```

### 4. Start
```bash
poetry run start
```

---

## 🧪 Supported Media Table

| Category | Extensions | Output Type |
| :--- | :--- | :--- |
| **Images** | jpg, png, webp, heic, avif | Processed Image |
| **Video** | mp4, mov, webm, avi | Frame @ timestamp |
| **Audio** | mp3, wav, ogg, flac | Waveform Image |
| **Documents** | pdf, docx, pptx, xlsx | Page Render / Summary |
| **BIM** | ifc | Technical Project Card |
| **3D / CAD** | stl, obj, glb, gltf | Technical Blueprint |
| **Text / Code**| json, xml, md, txt | Syntax-highlighted Image |
| **Typography** | ttf, otf | Font Specimen Image |
| **Archives** | zip, tar | Content List Image |

---

## 📁 Project Structure
```text
morphosx/
├── app/
│   ├── api/        # FastAPI Endpoints
│   ├── core/       # Security & HMAC Signing
│   ├── engine/     # Specialized Engines (Video, 3D, BIM, etc.)
│   ├── storage/    # Local and S3 Adapters
│   └── settings.py # Centralized Configuration
└── data/           # Original assets and Derivative Cache
```

## 📜 License
MIT - Built for the Open Source community.
