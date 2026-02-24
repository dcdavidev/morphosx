<p align="center">
  <img src="morphosx-banner.png" alt="morphosx banner" width="600px">
</p>

# morphosx 🧬
> **High performance, low footprint.**  
> Self-hosted, open-source media engine for on-the-fly image processing and delivery.

`morphosx` is a high-speed, minimal cloud storage and media manipulation server. It converts almost any media type into a optimized, web-ready image derivative on-the-fly.

---

## ⚡ Features

- **Modern Image Formats**: Support for **HEIC/HEIF** and **AVIF** out of the box.
- **Office Previews**: Generate summary cards for **DOCX, PPTX, and XLSX** files.
- **Font Specimen**: Create beautiful previews for **TTF and OTF** font files.
- **3D Blueprints**: Technical metadata and bounding-box summaries for **STL, OBJ, and GLB**.
- **Archive Contents**: List files inside **ZIP and TAR** archives as a folder-style image.
- **Video Thumbnails**: Extract high-quality frames from video files (MP4, WEBM, MOV, AVI).
- **Audio Waveforms**: Generate visual representations of audio tracks (MP3, WAV, OGG, FLAC).
- **Document Rendering**: Convert **PDF** pages into crisp images.
- **RAW Development**: Professional RAW image decoding (CR2, NEF, DNG, ARW).
- **Modern Rendering Engines**: Choice between **Pillow** (stable) and **PyVips** (ultra-fast).
- **Cloud Ready**: Pluggable storage system supporting **Local Filesystem** and **Amazon S3**.
- **Cyber-Security**: HMAC-SHA256 URL signing for secure distribution.

## 🛠️ Tech Stack

- **Engines**: Pillow, PyVips, FFmpeg, PyMuPDF, rawpy, trimesh, python-docx, etc.
- **Core**: FastAPI, aioboto3, pydantic-settings.

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have [Poetry](https://python-poetry.org/) and **FFmpeg** installed. For PyVips support, install `libvips`.

### 2. Installation
```bash
git clone https://github.com/dcdavidev/morphosx.git
cd morphosx
poetry install
```

### 3. Setup Environment
```bash
MORPHOSX_SECRET_KEY="your-secret"
MORPHOSX_STORAGE_TYPE="local" # or "s3"
MORPHOSX_ENGINE_TYPE="pillow" # or "vips"
```

### 4. Run the Engine
```bash
poetry run start
```

---

## 🧪 Supported Media Types

| Type | Extensions | Output |
| :--- | :--- | :--- |
| **Images** | jpg, png, webp, heic, avif | Processed Image |
| **Video** | mp4, mov, webm, avi | Frame @ timestamp |
| **Audio** | mp3, wav, ogg, flac | Waveform Image |
| **Docs** | pdf, docx, pptx, xlsx | Rendered Page/Summary |
| **Text** | json, xml, md, txt | Syntax-highlighted Image |
| **3D** | stl, obj, glb | Technical Blueprint |
| **Fonts** | ttf, otf | Specimen Image |
| **Archives** | zip, tar | Content List Image |

---

## 📜 License
MIT - Built for the OSS community.
