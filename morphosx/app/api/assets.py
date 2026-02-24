from pathlib import Path
import uuid
from mimetypes import guess_extension
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, UploadFile, File

from morphosx.app.core.security import verify_signature, generate_signature
from morphosx.app.engine.processor import ImageProcessor, ProcessingOptions, ImageFormat
from morphosx.app.storage.local import LocalStorage
from morphosx.app.settings import settings


router = APIRouter(prefix="/assets", tags=["Assets"])

# Singleton instances
processor = ImageProcessor()
storage = LocalStorage(base_directory=settings.storage_root)


@router.post("/upload")
async def upload_asset(file: UploadFile = File(...)):
    """
    Upload a new asset, save to 'originals/' folder.
    Returns a default signed URL for WebP format.
    """
    asset_uuid = str(uuid.uuid4())
    ext = guess_extension(file.content_type) or ".bin"
    asset_id = f"originals/{asset_uuid}{ext}"

    try:
        content = await file.read()
        saved_id = await storage.save_asset(asset_id, content)
        
        # Clean ID for the response
        clean_id = Path(saved_id).name
        
        # Generate a sample signed URL for default WebP
        sample_fmt = ImageFormat.WEBP
        sample_q = settings.default_quality
        sig = generate_signature(clean_id, None, None, sample_fmt.value.lower(), sample_q, settings.secret_key)
        
        return {
            "asset_id": clean_id,
            "url": f"{settings.api_prefix}/assets/{clean_id}?s={sig}",
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
    s: str = Query(..., alias="signature", description="HMAC-SHA256 signature (first 16 chars)"),
):
    """
    Retrieve and process an asset on-the-fly with signature verification.
    """
    # 1. Signature Verification (SECURITY FIRST)
    # Validate before touching storage or engine
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
    
    # 2. Define Cache Paths
    # asset_id = 'uuid.jpg' -> cache_path = 'cache/uuid.jpg/w300_hauto_q80.webp'
    cache_key = options.get_cache_key()
    derivative_id = f"cache/{asset_id}/{cache_key}"

    try:
        # 2. Cache Check (HIT)
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
            # 3. Cache Miss (MISS)
            pass

        # 4. Fetch Original (Always from originals/ folder)
        original_id = f"originals/{asset_id}"
        source_bytes = await storage.get_asset(original_id)
        
        # 5. Transform
        processed_data, mime_type = processor.process(source_bytes, options)
        
        # 6. Store derivative for future requests (Async background)
        # In a real-world scenario, we might use BackgroundTasks for this
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
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
