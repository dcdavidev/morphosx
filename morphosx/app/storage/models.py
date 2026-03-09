from pydantic import BaseModel
from typing import Optional


class AssetMetadata(BaseModel):
    """
    Standardized metadata for an asset in storage.
    """
    name: str
    path: str
    is_dir: bool
    size: Optional[int] = None
    modified: Optional[float] = None
