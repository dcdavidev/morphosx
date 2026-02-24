<p align="center">
  <img src="morphosx-banner.png" alt="morphosx banner" width="600px">
</p>

# morphosx 🧬

> **High performance, low footprint.**  
> Self-hosted, open-source media engine for on-the-fly image processing and delivery.

`morphosx` is a high-speed, minimal cloud storage and media manipulation server. It converts almost any media type into a optimized, web-ready image derivative on-the-fly.

---

## ⚡ Core Features

- **Folders & Navigation**: Organize assets into directories and browse them via a dedicated Listing API.
- **User-Bound Security**: Protected assets and HMAC signatures tied to specific **JWT-authenticated** users.
- **Private Folders**: Secure per-user storage using the `users/{user_id}/` path convention.
- **BIM & Architecture**: Technical Building Data Cards for **IFC** files.
- **3D & CAD Support**: Blueprints and metadata for **STL, OBJ, GLB, and GLTF**.
- **Modern Image Formats**: Support for **HEIC/HEIF** and **AVIF**.
- **Office Previews**: Summary cards for **DOCX, PPTX, and XLSX**.
- **Font Specimen**: Previews for **TTF and OTF** font files.
- **Archive Contents**: Visual content list for **ZIP and TAR**.
- **Media Engine**: Frame extraction from **Video** and waveforms from **Audio**.
- **Modern Rendering Engines**: Choice between **Pillow** and **PyVips**.
- **Cloud Ready**: Pluggable storage system supporting **Local Filesystem** and **Amazon S3**.

---

## 🛡️ Advanced Security & Authentication

MorphosX features a multi-layer security model to protect your assets.

### 1. JWT Authentication

The engine supports **Bearer JWT** tokens. If a request includes a valid token in the `Authorization` header, MorphosX identifies the `user_id` from the `sub` claim.

### 2. User-Bound HMAC Signatures

The signature payload includes: `asset_id | width | height | format | quality | preset | user_id`. A signed URL generated for one user cannot be used by another.

### 3. Private Assets

Assets stored under `users/{user_id}/` are strictly private. Access requires a valid JWT matching the owner ID and a valid HMAC signature.

---

## 📖 Usage Guide

### 1. Uploading Assets

**Public Upload**

```bash
curl -X POST "http://localhost:8000/v1/assets/upload?folder=news" -F "file=@img.jpg"
```

**Private Upload**

```bash
curl -X POST "http://localhost:8000/v1/assets/upload?private=true" \
     -H "Authorization: Bearer <TOKEN>" -F "file=@secret.pdf"
```

### 2. Listing Files

```text
GET /v1/assets/list/originals/news
```

---

## 🛠️ Automation & Development

We use `poethepoet` to automate common development tasks.

| Command                  | Description                                                        |
| :----------------------- | :----------------------------------------------------------------- |
| `poetry run poe commit`  | Interactive wizard to create **Conventional Commits**.             |
| `poetry run poe release` | **Auto-bump version**, update `CHANGELOG.md`, and create Git tags. |
| `poetry run poe check`   | Run the complete test suite via `pytest`.                          |
| `poetry run poe clean`   | Wipe all generated images from the local `data/cache`.             |

---

## ✨ Smart Presets

Use predefined aliases in `settings.py` for cleaner URLs:

- `preset=thumb`: 150x150 WebP.
- `preset=hero`: 1920px WebP.
- `preset=social`: 1200x630 JPEG.

---

## 🚀 Quick Start

### 1. Prerequisites

- **Python 3.11 - 3.14**
- **FFmpeg** (required)
- **libvips** (optional, for high performance)

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

| Category     | Extensions                 | Output Type              |
| :----------- | :------------------------- | :----------------------- |
| **BIM**      | ifc                        | Technical Project Card   |
| **3D**       | stl, obj, glb, gltf        | Technical Blueprint      |
| **Images**   | jpg, png, webp, heic, avif | Processed Image          |
| **Video**    | mp4, mov, webm, avi        | Frame @ timestamp        |
| **Audio**    | mp3, wav, ogg, flac        | Waveform Image           |
| **Docs**     | pdf, docx, pptx, xlsx      | Page Render / Summary    |
| **Text**     | json, xml, md, txt         | Syntax-highlighted Image |
| **Fonts**    | ttf, otf                   | Specimen Image           |
| **Archives** | zip, tar                   | Content List Image       |

---

## 📜 License

MIT - Built for the Open Source community.
