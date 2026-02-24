<p align="center">
  <img src="morphosx-banner.png" alt="morphosx banner" width="600px">
</p>

# morphosx 🧬

> **High performance, low footprint.**  
> Self-hosted, open-source media engine for on-the-fly image processing and delivery.

`morphosx` is a high-speed, minimal cloud storage and media manipulation server. It converts almost any media type into a optimized, web-ready image derivative on-the-fly.

---

## ⚡ Core Features

- **User-Bound Security**: Protected assets and HMAC signatures tied to specific **JWT-authenticated** users.
- **Private Folders**: Secure per-user storage using the `users/{user_id}/` path convention.
- **Universal Rendering**: Support for BIM (IFC), 3D (STL/OBJ/GLB), Office, Font Specimen, Archives, Video, Audio and RAW.
- **Modern Engines**: Choice between **Pillow** and **PyVips** (ultra-fast).
- **Cloud Ready**: Pluggable storage system (Local & **Amazon S3**).

---

## 🚀 Installation & Deployment

### 1. Using Docker (Recommended)

The easiest way to run Morphosx with all features and system dependencies pre-installed.

```bash
docker run -p 8000:8000 --env-file .env ghcr.io/dcdavidev/morphosx:latest
```

### 2. Using pip (from PyPI)

You can install Morphosx as a library or a standalone CLI tool.

```bash
# Core installation (standard images only)
pip install morphosx

# Full installation (all media types support)
pip install "morphosx[full]"

# Selective installation
pip install "morphosx[video,pdf,3d]"
```

**Note**: Some extras require system libraries (e.g., `ffmpeg` for video, `libvips` for vips engine).

---

## 📖 Usage Guide

### Start the Server

If installed via pip, you can use the global command:

```bash
morphosx start --port 8000 --reload
```

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

## ✨ Smart Presets

Use predefined aliases in `settings.py` for cleaner URLs:

- `preset=thumb`: 150x150 WebP.
- `preset=hero`: 1920px WebP.
- `preset=social`: 1200x630 JPEG.

---

## 🛡️ Advanced Security

Morphosx uses **HMAC-SHA256** to prevent DoS attacks.
The signature payload includes: `asset_id | width | height | format | quality | preset | user_id`.

---

## 🧪 Supported Media Table

| Category       | Extra      | Extensions          | Output Type            |
| :------------- | :--------- | :------------------ | :--------------------- |
| **BIM**        | `[bim]`    | ifc                 | Technical Project Card |
| **3D**         | `[3d]`     | stl, obj, glb, gltf | Technical Blueprint    |
| **Images**     | Core       | jpg, png, webp      | Processed Image        |
| **Modern Img** | `[modern]` | heic, avif          | Processed Image        |
| **RAW**        | `[raw]`    | cr2, nef, dng, arw  | Developed Image        |
| **Video**      | `[video]`  | mp4, mov, webm, avi | Frame @ timestamp      |
| **Audio**      | `[video]`  | mp3, wav, ogg, flac | Waveform Image         |
| **Docs**       | `[pdf]`    | pdf                 | Page Render            |
| **Office**     | `[office]` | docx, pptx, xlsx    | Summary Card           |
| **Text**       | Core       | json, xml, md, txt  | Syntax-highlighted     |
| **Typography** | Core       | ttf, otf            | Font Specimen          |
| **Archives**   | Core       | zip, tar            | Content List           |

---

## 📜 License

MIT - Built for the Open Source community.
