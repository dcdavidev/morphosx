## v0.5.1 (2026-03-01)

### Fix

- resolve IndentationError in assets.py

## v0.5.0 (2026-03-01)

### Feat

- support custom port 6100, unify storage paths, and set vips as default engine

### Fix

- change port to 6100, change env vars

## v0.4.0 (2026-02-24)

### Feat

- add GitHub Actions workflow for PyPI publishing

## v0.3.0 (2026-02-24)

### Feat

- add GitHub Actions workflow for Docker publishing on tag push
- add Dockerfile for containerized deployment

### Fix

- correct Dockerfile syntax for multi-line instructions

## v0.2.0 (2026-02-24)

### Feat

- complete folder navigation and listing API with security checks
- enhance upload logic to support private and public asset distinction
- add user-bound security, private folders, and JWT authentication
- implement Smart Presets system for transformation aliases
- add support for BIM (IFC) and GLTF media types
- add support for archive content previews (ZIP, TAR)
- add support for 3D model technical previews (STL, OBJ, GLB)
- add support for font specimen generation (TTF, OTF)
- add support for Office documents (DOCX, PPTX, XLSX) summary cards
- add support for HEIC, HEIF, and AVIF modern image formats
- add support for Markdown, JSON and XML rendering
- implement S3 storage and PyVips image processor
- implement RAW image processing support with rawpy
- implement PDF document to image extraction
- implement audio waveform generation
- implement video processing and thumbnail extraction with FFmpeg
- implement morphosx core engine, storage, and security layers
