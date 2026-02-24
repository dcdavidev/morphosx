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
- **BIM & Architecture**: Technical Building Data Cards for **IFC** files (using IfcOpenShell).
- **3D & CAD Support**: Blueprints and metadata for **STL, OBJ, GLB, and GLTF**.
- **Modern Image Formats**: Support for **HEIC/HEIF** and **AVIF**.
- **Office Previews**: Summary cards for **DOCX, PPTX, and XLSX**.
- **Font Specimen**: Previews for **TTF and OTF** font files.
- **Archive Contents**: Visual content list for **ZIP and TAR**.
- **Media Engine**: Frame extraction from **Video** and waveforms from **Audio**.
- **Document Rendering**: **PDF** page-to-image conversion.
- **RAW Development**: Professional decoding for **CR2, NEF, DNG, ARW**.
- **Modern Rendering Engines**: Choice between **Pillow** and **PyVips**.
- **Cloud Ready**: Pluggable storage system supporting **Local Filesystem** and **Amazon S3**.

---

## 🛡️ Advanced Security & Authentication

MorphosX features a multi-layer security model to protect your assets.

### 1. JWT Authentication
The engine supports **Bearer JWT** tokens. If a request includes a valid token in the `Authorization` header, MorphosX identifies the `user_id` from the `sub` claim.

### 2. User-Bound HMAC Signatures
Signatures can be tied to a specific user. A signed URL generated for User A will be rejected if accessed by User B, even for the same asset and parameters.
The signature payload includes: `asset_id | width | height | format | quality | preset | user_id`

### 3. Private Assets
Assets stored under the `users/{user_id}/` path are strictly private. Access is only granted if:
1. The requester is authenticated via a valid JWT.
2. The `user_id` in the token matches the owner ID in the path.
3. The HMAC signature correctly validates against that specific `user_id`.

---

## 📖 Usage Guide

### 1. Uploading Assets
You can upload assets to the public root or private user folders, optionally specifying a sub-folder.

**Public Upload with Folders**
```bash
curl -X POST "http://localhost:8000/v1/assets/upload?folder=marketing/2026" \
     -F "file=@banner.jpg"
```
*Stores the file in `originals/marketing/2026/uuid.jpg`.*

**Private Upload (User-Protected)**
```bash
curl -X POST "http://localhost:8000/v1/assets/upload?private=true&folder=personal" \
     -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
     -F "file=@document.pdf"
```
*Stores the file in `users/{user_id}/personal/uuid.pdf`.*

---

### 2. Listing & Navigation
Browse your storage using the Listing API.

**List Public Files**
```text
GET /v1/assets/list/originals/marketing
```

**List Private Files**
```bash
curl -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
     "http://localhost:8000/v1/assets/list/users/123/personal"
```
*Returns a JSON array of files and folders with metadata (size, type, modification date).*

---

### 3. Retrieving & Processing Assets
To fetch an asset, you must provide a valid `signature` (HMAC-SHA256).

**Basic Image Transformation**
```text
GET /v1/assets/originals/marketing/banner.jpg?width=800&format=webp&signature=...
```

**Requesting Private Assets**
```bash
curl -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
     "http://localhost:8000/v1/assets/users/123/doc.pdf?page=1&signature=..."
```

---

### 4. Parameter Reference

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `width` | `int` | Target width in pixels. |
| `height` | `int` | Target height in pixels. |
| `format` | `str` | Output format: `webp`, `jpeg`, `png`. |
| `quality` | `int` | Compression quality (1-100). |
| `preset` | `str` | Use a predefined configuration (e.g., `thumb`, `hero`). |
| `time` | `float`| **[Video Only]** Extraction timestamp in seconds. |
| `page` | `int` | **[PDF Only]** Page number to render (starts at 1). |
| `signature`| `str` | **[Required]** 16-character HMAC signature. |

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
- **FFmpeg** (for video and audio)
- **libvips** (optional)

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
| **BIM** | ifc | Technical Project Card |
| **3D** | stl, obj, glb, gltf | Technical Blueprint |
| **Images** | jpg, png, webp, heic, avif | Processed Image |
| **Video** | mp4, mov, webm, avi | Frame @ timestamp |
| **Audio** | mp3, wav, ogg, flac | Waveform Image |
| **Docs** | pdf, docx, pptx, xlsx | Page Render / Summary |
| **Text** | json, xml, md, txt | Syntax-highlighted Image |
| **Fonts** | ttf, otf | Specimen Image |
| **Archives** | zip, tar | Content List Image |

---

## 📜 License
MIT - Built for the Open Source community.
