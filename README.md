<p align="center">
  <img src="morphosx-banner.png" alt="morphosx banner" width="600px">
</p>

# morphosx 🧬
> **High performance, low footprint.**  
> Self-hosted, open-source media engine for on-the-fly image processing and delivery.

`morphosx` is a high-speed, minimal cloud storage and media manipulation server. It converts almost any media type into a optimized, web-ready image derivative on-the-fly.

---

## ⚡ Features

- **BIM & Architecture**: Technical Building Data Cards for **IFC** files (using IfcOpenShell).
- **3D & CAD Support**: Blueprints and metadata for **STL, OBJ, GLB, and GLTF**.
- **Modern Image Formats**: Support for **HEIC/HEIF** and **AVIF**.
- **Office Previews**: Summary cards for **DOCX, PPTX, and XLSX**.
- **Font Specimen**: Previews for **TTF and OTF** font files.
- **Archive Contents**: Visual content list for **ZIP and TAR**.
- **Media Engine**: Frame extraction from **Video** and waveforms from **Audio**.
- **Document Rendering**: **PDF** page-to-image conversion.
- **RAW Development**: Professional decoding for **CR2, NEF, DNG, ARW**.
- **Cloud Ready**: Pluggable storage (Local & **S3**).

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have [Poetry](https://python-poetry.org/) and **FFmpeg** installed. For BIM support, `ifcopenshell` is included in the dependencies.

### 2. Installation
```bash
git clone https://github.com/dcdavidev/morphosx.git
cd morphosx
poetry install
```

### 3. Run the Engine
```bash
poetry run start
```

---

## 🧪 Supported Media Types

| Type | Extensions | Output |
| :--- | :--- | :--- |
| **BIM** | ifc | Technical Project Card |
| **3D** | stl, obj, glb, gltf | Technical Blueprint |
| **Images** | jpg, png, webp, heic, avif | Processed Image |
| **Video** | mp4, mov, webm, avi | Frame @ timestamp |
| **Audio** | mp3, wav, ogg, flac | Waveform Image |
| **Docs** | pdf, docx, pptx, xlsx | Rendered Page/Summary |
| **Text** | json, xml, md, txt | Syntax-highlighted Image |
| **Fonts** | ttf, otf | Specimen Image |
| **Archives** | zip, tar | Content List Image |

---

## 📜 License
MIT - Built for the OSS community.
