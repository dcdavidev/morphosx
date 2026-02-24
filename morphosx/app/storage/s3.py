import aioboto3
from typing import Optional
from morphosx.app.storage.base import BaseStorage


class S3Storage(BaseStorage):
    """
    Amazon S3 (or S3-compatible) storage provider.
    
    Uses aioboto3 for asynchronous communication with the storage service.
    """

    def __init__(
        self, 
        bucket_name: str, 
        region_name: str = "us-east-1",
        endpoint_url: Optional[str] = None,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None
    ):
        """
        Initialize S3 storage.
        
        :param bucket_name: Name of the S3 bucket.
        :param region_name: AWS region.
        :param endpoint_url: Custom S3 endpoint (for MinIO, DigitalOcean Spaces, etc.)
        :param access_key_id: AWS access key.
        :param secret_access_key: AWS secret key.
        """
        self.bucket_name = bucket_name
        self.session = aioboto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name
        )
        self.endpoint_url = endpoint_url

    async def get_asset(self, asset_id: str) -> bytes:
        """
        Retrieve raw asset bytes from S3.
        
        :param asset_id: The key (path) of the object in S3.
        :return: Raw bytes.
        """
        async with self.session.client("s3", endpoint_url=self.endpoint_url) as s3:
            try:
                response = await s3.get_object(Bucket=self.bucket_name, Key=asset_id)
                async with response["Body"] as stream:
                    return await stream.read()
            except s3.exceptions.NoSuchKey:
                raise FileNotFoundError(f"Asset '{asset_id}' not found in S3 bucket '{self.bucket_name}'")
            except Exception as e:
                raise RuntimeError(f"S3 get_asset failed: {str(e)}")

    async def save_asset(self, asset_id: str, data: bytes) -> str:
        """
        Upload asset bytes to S3.
        
        :param asset_id: The key (path) to save as in S3.
        :param data: Raw bytes.
        :return: The final asset_id (key).
        """
        async with self.session.client("s3", endpoint_url=self.endpoint_url) as s3:
            try:
                await s3.put_object(Bucket=self.bucket_name, Key=asset_id, Body=data)
                return asset_id
            except Exception as e:
                raise RuntimeError(f"S3 save_asset failed: {str(e)}")
