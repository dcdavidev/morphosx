import os
import aiofiles
from pathlib import Path
from typing import List
from morphosx.app.storage.base import BaseStorage
from morphosx.app.storage.models import AssetMetadata


class LocalStorage(BaseStorage):
    """
    Local filesystem storage provider.
    """

    def __init__(self, base_directory: str):
        self.base_dir = Path(base_directory).resolve()

    async def get_asset(self, asset_id: str) -> bytes:
        asset_path = (self.base_dir / asset_id).resolve()
        if not str(asset_path).startswith(str(self.base_dir)):
            raise PermissionError("Access denied")
        if not asset_path.exists() or not asset_path.is_file():
            raise FileNotFoundError(f"Asset '{asset_id}' not found")
        async with aiofiles.open(asset_path, mode='rb') as f:
            return await f.read()

    async def save_asset(self, asset_id: str, data: bytes) -> str:
        asset_path = (self.base_dir / asset_id).resolve()
        asset_path.parent.mkdir(parents=True, exist_ok=True)
        async with aiofiles.open(asset_path, mode='wb') as f:
            await f.write(data)
        return asset_id

    async def list_assets(self, prefix: str) -> List[AssetMetadata]:
        folder_path = (self.base_dir / prefix).resolve()
        if not str(folder_path).startswith(str(self.base_dir)):
            raise PermissionError("Access denied")
        if not folder_path.exists():
            return []

        results = []
        for entry in os.scandir(folder_path):
            stat = entry.stat()
            results.append(AssetMetadata(
                name=entry.name,
                path=str(Path(prefix) / entry.name),
                is_dir=entry.is_dir(),
                size=stat.st_size if entry.is_file() else None,
                modified=stat.st_mtime
            ))
        return results
