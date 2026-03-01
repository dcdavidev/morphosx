# Asset Transformation and Processing

MorphosX allows you to manipulate assets in real-time using URL parameters. All GET requests must be signed (parameter `s` or `signature`).

## Transformation Parameters (Query Params)

Key parameters for images and derivatives include:

- **`width` (alias: `w`)**: Target width in pixels.
- **`height` (alias: `h`)**: Target height in pixels.
- **`format` (alias: `fmt`)**: Output format (e.g., `webp`, `jpeg`, `png`).
- **`quality` (alias: `q`)**: Compression quality (1-100).
- **`preset`**: Name of a predefined preset (e.g., `thumb`, `banner`).
- **`signature` (alias: `s`)**: Mandatory security parameter.

## Specialized Processing by File Type

MorphosX supports transformations across various media:

### Video (Frame Extraction)
- **`time` (alias: `t`)**: Extract a frame at the specified second (default: `0.0`).
- The extracted frame is processed according to image parameters (`w`, `h`, `fmt`).

### Audio (Waveform Generation)
- Generates an image representing the audio waveform.
- `w` and `h` control the dimensions of the waveform image.

### Documents (PDF to Image)
- **`page` (alias: `p`)**: Extract a specific PDF page as an image (default: `1`).
- The page is rendered at high quality and subsequently resized if requested.

### Other Supported Formats
- **RAW**: Extract integrated previews.
- **Office (DOCX, XLSX, PPTX)**: Auto-generate a summary card.
- **Fonts (TTF, OTF)**: Auto-generate a character specimen.
- **3D Models (STL, OBJ, GLB)**: 2D preview rendering (thumbnail).
- **Archives (ZIP, TAR)**: Content list visualization as an image.
- **BIM (IFC)**: Generate a structured data summary as an image.

## Smart Presets

Presets group common configurations together. Instead of sending `w=200&h=200&fmt=webp`, you can define a `thumb` preset in server settings and request it like so:
`GET /assets/file.jpg?preset=thumb&s=HASH`

*Explicit query parameters take precedence over preset values.*
