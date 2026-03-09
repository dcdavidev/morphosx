from abc import ABC, abstractmethod
from typing import List
from morphosx.app.storage.models import AssetMetadata


class BaseStorage(ABC):
    """
    Abstract base class for storage providers.
    """

    @abstractmethod
    async def get_asset(self, asset_id: str) -> bytes:
        pass

    @abstractmethod
    async def save_asset(self, asset_id: str, data: bytes) -> str:
        pass

    @abstractmethod
    async def list_assets(self, prefix: str) -> List[AssetMetadata]:
        """
        List assets and sub-folders starting with a given prefix.
        
        :param prefix: The folder path to list.
        :return: A list of AssetMetadata objects.
        """
        pass
