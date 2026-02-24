import os
from pathlib import Path
from typing import List
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
    
    # --- SECURITY ---
    # MUST be changed in production!
    secret_key: str = "change-me-at-all-costs-cyberpunk-2077"
    
    # --- STORAGE PATHS ---
    # Defaults to 'data/' in the project root
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    storage_root: str = str(base_dir / "data")
    
    @property
    def originals_dir(self) -> str:
        return str(Path(self.storage_root) / "originals")
    
    @property
    def cache_dir(self) -> str:
        return str(Path(self.storage_root) / "cache")
    
    # --- IMAGE & VIDEO ENGINE DEFAULTS ---
    default_quality: int = 80
    max_image_dimension: int = 4096
    allowed_formats: List[str] = ["jpeg", "png", "webp", "mp4", "webm", "mov"]
    
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
