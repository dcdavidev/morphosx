from abc import ABC, abstractmethod


class BaseStorage(ABC):
    """
    Abstract base class for storage providers.
    
    All storage backends (Local, S3, etc.) must implement these methods.
    """

    @abstractmethod
    async def get_asset(self, asset_id: str) -> bytes:
        """
        Retrieve raw asset bytes from storage.
        
        :param asset_id: Unique identifier for the asset (e.g., filename or UUID).
        :return: Raw bytes of the asset.
        :raises FileNotFoundError: If the asset does not exist.
        """
        pass

    @abstractmethod
    async def save_asset(self, asset_id: str, data: bytes) -> str:
        """
        Save raw asset bytes to storage.
        
        :param asset_id: The ID to associate with the asset (including extension).
        :param data: The raw bytes of the image/file.
        :return: The final asset_id (or path) where it was saved.
        """
        pass

    @abstractmethod
    async def list_assets(self, prefix: str) -> list[dict]:
        """
        List assets and sub-folders starting with a given prefix.
        
        :param prefix: The folder path to list.
        :return: A list of metadata dicts (name, type, size, etc.)
        """
        pass
