from pathlib import Path
import uuid
from mimetypes import guess_extension
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, UploadFile, File

from morphosx.app.core.security import verify_signature, generate_signature
from morphosx.app.engine.processor import ImageProcessor, ProcessingOptions, ImageFormat
from morphosx.app.engine.video import VideoProcessor
from morphosx.app.engine.audio import AudioProcessor
from morphosx.app.engine.document import DocumentProcessor
from morphosx.app.engine.raw import RawProcessor
from morphosx.app.engine.vips import VipsProcessor
from morphosx.app.engine.text import TextProcessor
from morphosx.app.engine.office import OfficeProcessor
from morphosx.app.engine.font import FontProcessor
from morphosx.app.engine.model3d import Model3DProcessor
from morphosx.app.engine.archive import ArchiveProcessor
from morphosx.app.storage.local import LocalStorage
from morphosx.app.storage.s3 import S3Storage
from morphosx.app.settings import settings


router = APIRouter(prefix="/assets", tags=["Assets"])

# Singleton instances factory
def get_storage():
    if settings.storage_type == "s3":
        if not settings.s3_bucket:
            raise ValueError("S3_BUCKET is required for s3 storage_type")
        return S3Storage(
            bucket_name=settings.s3_bucket,
            region_name=settings.s3_region,
            endpoint_url=settings.s3_endpoint,
            access_key_id=settings.s3_access_key,
            secret_access_key=settings.s3_secret_key
        )
    return LocalStorage(base_directory=settings.storage_root)

def get_processor():
    if settings.engine_type == "vips":
        return VipsProcessor()
    return ImageProcessor()

storage = get_storage()
processor = get_processor()
video_processor = VideoProcessor()
audio_processor = AudioProcessor()
document_processor = DocumentProcessor()
raw_processor = RawProcessor()
text_processor = TextProcessor()
office_processor = OfficeProcessor()
font_processor = FontProcessor()
model3d_processor = Model3DProcessor()
archive_processor = ArchiveProcessor()

VIDEO_EXTENSIONS = {".mp4", ".webm", ".mov", ".avi"}
AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac"}
DOCUMENT_EXTENSIONS = {".pdf"}
RAW_EXTENSIONS = {".cr2", ".nef", ".dng", ".arw"}
TEXT_EXTENSIONS = {".json", ".xml", ".md"}
OFFICE_EXTENSIONS = {".docx", ".pptx", ".xlsx"}
FONT_EXTENSIONS = {".ttf", ".otf"}
MODEL3D_EXTENSIONS = {".stl", ".obj", ".glb"}
ARCHIVE_EXTENSIONS = {".zip", ".tar", ".gz"}



@router.post("/upload")
async def upload_asset(file: UploadFile = File(...)):
    """
    Upload a new asset (Image or Video), save to 'originals/' folder.
    Returns a default signed URL for processing.
    """
    asset_uuid = str(uuid.uuid4())
    ext = guess_extension(file.content_type) or ".bin"
    asset_id = f"originals/{asset_uuid}{ext}"

    try:
        content = await file.read()
        saved_id = await storage.save_asset(asset_id, content)
        
        # Clean ID for the response
        clean_id = Path(saved_id).name
        
        # Determine if it's a video to suggest thumbnail params
        is_video = ext.lower() in VIDEO_EXTENSIONS
        
        # Generate a sample signed URL for default WebP
        sample_fmt = ImageFormat.WEBP
        sample_q = settings.default_quality
        sig = generate_signature(clean_id, None, None, sample_fmt.value.lower(), sample_q, settings.secret_key)
        
        url = f"{settings.api_prefix}/assets/{clean_id}?s={sig}"
        if is_video:
            url += "&t=1" # Default to 1s thumbnail

        return {
            "asset_id": clean_id,
            "url": url,
            "is_video": is_video,
            "original_filename": file.filename,
            "mime_type": file.content_type,
            "size": len(content)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


@router.get("/{asset_id:path}")
async def get_processed_asset(
    asset_id: str,
    w: Optional[int] = Query(None, alias="width", ge=1, le=settings.max_image_dimension),
    h: Optional[int] = Query(None, alias="height", ge=1, le=settings.max_image_dimension),
    fmt: Optional[ImageFormat] = Query(None, alias="format"),
    q: int = Query(settings.default_quality, alias="quality", ge=1, le=100),
    t: float = Query(0.0, alias="time", ge=0.0),
    p: int = Query(1, alias="page", ge=1),
    s: str = Query(..., alias="signature", description="HMAC-SHA256 signature"),
):
    """
    Retrieve and process an asset.
    If it's a video, extract a frame. If it's a document, extract a page.
    """
    # 1. Signature Verification (SECURITY FIRST)
    fmt_val = fmt if fmt else ImageFormat.WEBP
    is_valid = verify_signature(
        asset_id=asset_id,
        width=w,
        height=h,
        format=fmt_val.value.lower(),
        quality=q,
        signature_to_verify=s,
        secret_key=settings.secret_key
    )
    
    if not is_valid:
        raise HTTPException(status_code=403, detail="Invalid signature")

    options = ProcessingOptions(
        width=w,
        height=h,
        format=fmt_val,
        quality=q
    )
    
    # 2. Define Cache Paths (Include timestamp or page for media derivatives)
    cache_key = options.get_cache_key()
    is_video = Path(asset_id).suffix.lower() in VIDEO_EXTENSIONS
    is_document = Path(asset_id).suffix.lower() in DOCUMENT_EXTENSIONS
    
    if is_video:
        cache_key = f"t{t}_{cache_key}"
    elif is_document:
        cache_key = f"p{p}_{cache_key}"

    derivative_id = f"cache/{asset_id}/{cache_key}"

    try:
        # 3. Cache Check (HIT)
        try:
            derivative_bytes = await storage.get_asset(derivative_id)
            return Response(
                content=derivative_bytes,
                media_type=f"image/{options.format.value.lower()}",
                headers={
                    "Cache-Control": "public, max-age=31536000, immutable",
                    "X-MorphosX-Cache": "HIT"
                }
            )
        except FileNotFoundError:
            # 4. Cache Miss (MISS)
            pass

        # 5. Fetch Original (Always from originals/ folder)
        original_id = f"originals/{asset_id}"
        source_bytes = await storage.get_asset(original_id)
        
        # 6. Transform Pipeline
        is_audio = Path(asset_id).suffix.lower() in AUDIO_EXTENSIONS
        is_raw = Path(asset_id).suffix.lower() in RAW_EXTENSIONS
        is_text = Path(asset_id).suffix.lower() in TEXT_EXTENSIONS
        is_office = Path(asset_id).suffix.lower() in OFFICE_EXTENSIONS
        is_font = Path(asset_id).suffix.lower() in FONT_EXTENSIONS
        is_model3d = Path(asset_id).suffix.lower() in MODEL3D_EXTENSIONS
        is_archive = Path(asset_id).suffix.lower() in ARCHIVE_EXTENSIONS

        if is_video:
            # Video: Extract Frame -> Process as Image
            frame_bytes = video_processor.extract_thumbnail(source_bytes, t)
            processed_data, mime_type = processor.process(frame_bytes, options)
        elif is_audio:
            # Audio: Generate Waveform -> Process as Image
            waveform_bytes = audio_processor.generate_waveform(source_bytes, w or 800, h or 200)
            processed_data, mime_type = processor.process(waveform_bytes, options)
        elif is_document:
            # Document: Extract Page -> Process as Image
            # We extract at 150 DPI to ensure crisp text before potential downscaling
            page_bytes = document_processor.extract_page_as_image(source_bytes, p, dpi=150)
            processed_data, mime_type = processor.process(page_bytes, options)
        elif is_raw:
            # RAW: Extract Preview -> Process as Image
            preview_bytes = raw_processor.extract_preview(source_bytes)
            processed_data, mime_type = processor.process(preview_bytes, options)
        elif is_text:
            # Text: Render to Image -> Process as Image
            rendered_bytes = text_processor.render_to_image(source_bytes, asset_id, options)
            processed_data, mime_type = processor.process(rendered_bytes, options)
        elif is_office:
            # Office: Generate Summary Card -> Process as Image
            office_card_bytes = office_processor.render_thumbnail(source_bytes, asset_id)
            processed_data, mime_type = processor.process(office_card_bytes, options)
        elif is_font:
            # Font: Render Specimen -> Process as Image
            specimen_bytes = font_processor.render_specimen(source_bytes, {})
            processed_data, mime_type = processor.process(specimen_bytes, options)
        elif is_model3d:
            # 3D: Generate Blueprint -> Process as Image
            model_bytes = model3d_processor.render_thumbnail(source_bytes, asset_id)
            processed_data, mime_type = processor.process(model_bytes, options)
        elif is_archive:
            # Archive: Generate Content List -> Process as Image
            archive_bytes = archive_processor.render_thumbnail(source_bytes, asset_id)
            processed_data, mime_type = processor.process(archive_bytes, options)
        else:
            # Image: Process directly
            processed_data, mime_type = processor.process(source_bytes, options)
        
        # 7. Store derivative for future requests
        await storage.save_asset(derivative_id, processed_data)
        
        return Response(
            content=processed_data,
            media_type=mime_type,
            headers={
                "Cache-Control": "public, max-age=31536000, immutable",
                "X-MorphosX-Cache": "MISS"
            }
        )
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Asset not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")
