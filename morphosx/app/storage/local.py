import aiofiles
from pathlib import Path
from morphosx.app.storage.base import BaseStorage


class LocalStorage(BaseStorage):
    """
    Local filesystem storage provider.
    
    Loads asset files from a specific local directory.
    """

    def __init__(self, base_directory: str):
        """
        Initialize the local storage.
        
        :param base_directory: Path to the root directory for assets.
        """
        self.base_dir = Path(base_directory).resolve()

    async def get_asset(self, asset_id: str) -> bytes:
        """
        Retrieve raw asset bytes from the local disk.
        
        :param asset_id: Relative path or filename from the base directory.
        :return: Raw bytes of the asset.
        :raises FileNotFoundError: If the asset is missing or outside base directory.
        """
        asset_path = (self.base_dir / asset_id).resolve()

        # Security check: Ensure requested path is within the base directory
        if not str(asset_path).startswith(str(self.base_dir)):
            raise PermissionError("Access outside the asset base directory is denied.")

        if not asset_path.exists() or not asset_path.is_file():
            raise FileNotFoundError(f"Asset '{asset_id}' not found at {asset_path}")

        async with aiofiles.open(asset_path, mode='rb') as f:
            return await f.read()

    async def save_asset(self, asset_id: str, data: bytes) -> str:
        """
        Save asset bytes to the local filesystem.
        
        :param asset_id: Relative path (e.g. 'f47ac10b.jpg').
        :param data: Raw bytes.
        :return: Final asset_id.
        """
        asset_path = (self.base_dir / asset_id).resolve()
        
        # Ensure parent directory exists (for subfolder support)
        asset_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(asset_path, mode='wb') as f:
            await f.write(data)
            
        return asset_id
