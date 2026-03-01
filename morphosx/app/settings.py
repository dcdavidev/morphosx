import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Centralized application settings and environment variables.
    
    All variables can be overridden by environment variables with 
    the 'MORPHOSX_' prefix (e.g., MORPHOSX_SECRET_KEY).
    """
    
    # --- BASIC APP CONFIG ---
    app_name: str = "morphosx"
    debug: bool = False
    api_prefix: str = "/v1"
    port: int = 6100
    
    # --- SECURITY ---
    # MUST be changed in production!
    secret_key: str = "change-me-at-all-costs-cyberpunk-2077"
    
    # --- STORAGE PATHS ---
    # Defaults to 'storage/' in the project root
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    storage_path: str = str(base_dir / "storage")
    
    # --- STORAGE BACKEND ---
    # Choice: 'local' or 's3'
    storage_type: str = "local"
    s3_bucket: Optional[str] = None
    s3_region: str = "us-east-1"
    s3_endpoint: Optional[str] = None
    s3_access_key: Optional[str] = None
    s3_secret_key: Optional[str] = None
    
    @property
    def originals_dir(self) -> str:
        return str(Path(self.storage_path) / "originals")
    
    @property
    def cache_dir(self) -> str:
        return str(Path(self.storage_path) / "cache")
    
    # --- IMAGE & MEDIA ENGINE ---
    # Choice: 'pillow' or 'vips'
    engine_type: str = "vips"
    default_quality: int = 80
    max_image_dimension: int = 4096
    allowed_formats: List[str] = ["jpeg", "png", "webp", "mp4", "webm", "mov", "mp3", "wav", "ogg", "flac", "pdf", "cr2", "nef", "dng", "arw", "json", "xml", "md", "heic", "heif", "avif", "docx", "pptx", "xlsx", "ttf", "otf", "stl", "obj", "glb", "zip", "tar", "ifc", "gltf"]
    
    # --- SMART PRESETS ---
    # Predefined transformation aliases
    presets: dict = {
        "thumb": {"width": 150, "height": 150, "format": "webp", "quality": 70},
        "hero": {"width": 1920, "format": "webp", "quality": 85},
        "social": {"width": 1200, "height": 630, "format": "jpeg", "quality": 90},
        "preview": {"width": 400, "format": "png", "quality": 80}
    }
    
    # --- ENVIRONMENT CONFIG ---
    model_config = SettingsConfigDict(
        env_prefix="MORPHOSX_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Singleton instance
settings = Settings()
