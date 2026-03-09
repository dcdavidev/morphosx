import uuid
from mimetypes import guess_extension
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, HTTPException, Query, Response, UploadFile

from morphosx.app.core.auth import get_current_user
from morphosx.app.core.security import generate_signature, verify_signature
from morphosx.app.engine.base import initialize_registry
from morphosx.app.engine.types import ImageFormat, ProcessingOptions
from morphosx.app.settings import settings
from morphosx.app.storage.local import LocalStorage
from morphosx.app.storage.s3 import S3Storage

router = APIRouter(prefix="/assets", tags=["Assets"])


# Singleton instances
def get_storage():
    if settings.storage_type == "s3":
        if not settings.s3_bucket:
            raise ValueError("S3_BUCKET is required for s3 storage_type")
        return S3Storage(
            bucket_name=settings.s3_bucket,
            region_name=settings.s3_region,
            endpoint_url=settings.s3_endpoint,
            access_key_id=settings.s3_access_key,
            secret_access_key=settings.s3_secret_key,
        )
    return LocalStorage(base_directory=settings.storage_path)


storage = get_storage()
processor_registry = initialize_registry()


def get_mime_type(fmt: ImageFormat) -> str:
    if fmt == ImageFormat.JSON:
        return "application/json"
    elif fmt == ImageFormat.YAML:
        return "application/x-yaml"
    elif fmt == ImageFormat.XML:
        return "application/xml"
    return f"image/{fmt.value.lower()}"


@router.post("/upload")
async def upload_asset(
    file: UploadFile = File(...),
    private: bool = Query(False),
    folder: Optional[str] = Query(None),
    current_user: Optional[str] = Depends(get_current_user),
):
    """
    Upload a new asset.
    - If 'private=True' and user is logged in: saved to 'users/{user_id}/{folder}/'
    - Otherwise: saved to 'originals/{folder}/'
    """
    asset_uuid = str(uuid.uuid4())
    ext = guess_extension(file.content_type) or ".bin"

    # Determine base prefix
    if private:
        if not current_user:
            raise HTTPException(status_code=401, detail="Authentication required for private uploads")
        base_prefix = f"users/{current_user}"
    else:
        base_prefix = "originals"

    # Sanitize and add custom folder if provided
    path_parts = [base_prefix]
    if folder:
        sanitized_folder = folder.strip("/")
        if sanitized_folder:
            path_parts.append(sanitized_folder)

    asset_id = f"{'/'.join(path_parts)}/{asset_uuid}{ext}"

    try:
        content = await file.read()
        saved_id = await storage.save_asset(asset_id, content)

        # Clean ID for the response (for private assets we keep the user prefix)
        clean_id = saved_id if private else Path(saved_id).name

        # Determine if it's a video to suggest thumbnail params
        is_video = ext.lower() in {".mp4", ".webm", ".mov", ".avi"}

        # Generate a sample signed URL
        sample_fmt = ImageFormat.WEBP
        sample_q = settings.default_quality
        sig = generate_signature(
            asset_id=clean_id,
            width=None,
            height=None,
            format=sample_fmt.value.lower(),
            quality=sample_q,
            secret_key=settings.secret_key,
            user_id=current_user if private else None,
        )

        url = f"{settings.api_prefix}/assets/{clean_id}?s={sig}"
        if is_video:
            url += "&t=1"

        return {
            "asset_id": clean_id,
            "url": url,
            "is_private": private,
            "owner": current_user if private else "public",
            "mime_type": file.content_type,
            "size": len(content),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")


def _apply_preset(
    w: Optional[int],
    h: Optional[int],
    fmt: Optional[ImageFormat],
    q: Optional[int],
    preset: Optional[str],
):
    target_w, target_h, target_fmt, target_q = w, h, fmt, q
    if not target_q:
        target_q = settings.default_quality

    if preset:
        if preset not in settings.presets:
            raise HTTPException(status_code=400, detail=f"Invalid preset: {preset}")

        config = settings.presets[preset]
        target_w = w if w else config.get("width")
        target_h = h if h else config.get("height")
        target_fmt = fmt if fmt else ImageFormat(config.get("format").upper())
        target_q = q if q else config.get("quality", settings.default_quality)

    if not target_fmt:
        target_fmt = ImageFormat.WEBP

    return target_w, target_h, target_fmt, target_q


def _verify_asset_access(asset_id: str, current_user: Optional[str]):
    if asset_id.startswith("users/"):
        parts = asset_id.split("/")
        if len(parts) < 3:
            raise HTTPException(status_code=400, detail="Invalid private asset path")

        owner_id = parts[1]
        if current_user != owner_id:
            raise HTTPException(status_code=403, detail="Not authorized to access this private asset")


def _verify_request_signature(
    asset_id: str,
    w: Optional[int],
    h: Optional[int],
    fmt: Optional[ImageFormat],
    q: Optional[int],
    s: str,
    preset: Optional[str],
    current_user: Optional[str],
):
    is_valid = verify_signature(
        asset_id=asset_id,
        width=w,
        height=h,
        format=fmt.value.lower() if fmt else "",
        quality=q if q else 0,
        signature_to_verify=s,
        secret_key=settings.secret_key,
        preset=preset,
        user_id=current_user,
    )

    if not is_valid:
        raise HTTPException(status_code=403, detail="Invalid signature")


@router.get("/{asset_id:path}")
async def get_processed_asset(
    asset_id: str,
    w: Optional[int] = Query(None, alias="width", ge=1, le=settings.max_image_dimension),
    h: Optional[int] = Query(None, alias="height", ge=1, le=settings.max_image_dimension),
    fmt: Optional[ImageFormat] = Query(None, alias="format"),
    q: Optional[int] = Query(None, alias="quality", ge=1, le=100),
    preset: Optional[str] = Query(None, alias="preset"),
    t: float = Query(0.0, alias="time", ge=0.0),
    p: int = Query(1, alias="page", ge=1),
    s: str = Query(..., alias="signature", description="HMAC-SHA256 signature"),
    current_user: Optional[str] = Depends(get_current_user),
):
    """
    Retrieve and process an asset.
    Supports Smart Presets and User-bound protected assets.
    """
    target_w, target_h, target_fmt, target_q = _apply_preset(w, h, fmt, q, preset)

    _verify_asset_access(asset_id, current_user)
    _verify_request_signature(asset_id, w, h, fmt, q, s, preset, current_user)

    options = ProcessingOptions(
        width=target_w,
        height=target_h,
        format=target_fmt,
        quality=target_q,
        time=t,
        page=p,
    )

    # 2. Define Cache Paths
    cache_key = options.get_cache_key()
    derivative_id = f"cache/{asset_id}/{cache_key}"

    try:
        # 3. Cache Check (HIT)
        try:
            derivative_bytes = await storage.get_asset(derivative_id)
            return Response(
                content=derivative_bytes,
                media_type=get_mime_type(options.format),
                headers={
                    "Cache-Control": "public, max-age=31536000, immutable",
                    "X-MorphosX-Cache": "HIT",
                },
            )
        except FileNotFoundError:
            # 4. Cache Miss (MISS)
            pass

        # 5. Fetch Original (Always from originals/ folder)
        original_id = f"originals/{asset_id}"
        source_bytes = await storage.get_asset(original_id)

        # 6. Transform Pipeline (Using Registry)
        processor = processor_registry.get_processor(asset_id)
        if not processor:
            raise HTTPException(status_code=415, detail="Unsupported media type")

        processed_data, mime_type = processor.process(source_bytes, options, filename=asset_id)

        # 7. Store derivative for future requests
        await storage.save_asset(derivative_id, processed_data)

        return Response(
            content=processed_data,
            media_type=mime_type,
            headers={
                "Cache-Control": "public, max-age=31536000, immutable",
                "X-MorphosX-Cache": "MISS",
            },
        )

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Asset not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.get("/list/{path:path}")
async def list_assets(path: str = "", current_user: Optional[str] = Depends(get_current_user)):
    """
    List files and folders in a given path.
    """
    # Security: If path starts with users/, verify ownership
    if path.startswith("users/"):
        parts = path.split("/")
        if len(parts) >= 2:
            owner_id = parts[1]
            if current_user != owner_id:
                raise HTTPException(status_code=403, detail="Not authorized to browse this folder")

    # If path is empty, default to listing 'originals/' (public root)
    if not path:
        path = "originals"

    try:
        items = await storage.list_assets(path)
        return {"path": path, "items": items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Listing failed: {str(e)}")
