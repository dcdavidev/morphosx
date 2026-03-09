import aioboto3
from typing import Optional, List
from morphosx.app.storage.base import BaseStorage
from morphosx.app.storage.models import AssetMetadata


class S3Storage(BaseStorage):
    """
    Amazon S3 (or S3-compatible) storage provider.
    """

    def __init__(
        self, 
        bucket_name: str, 
        region_name: str = "us-east-1",
        endpoint_url: Optional[str] = None,
        access_key_id: Optional[str] = None,
        secret_access_key: Optional[str] = None
    ):
        self.bucket_name = bucket_name
        self.session = aioboto3.Session(
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            region_name=region_name
        )
        self.endpoint_url = endpoint_url

    async def get_asset(self, asset_id: str) -> bytes:
        async with self.session.client("s3", endpoint_url=self.endpoint_url) as s3:
            try:
                response = await s3.get_object(Bucket=self.bucket_name, Key=asset_id)
                async with response["Body"] as stream:
                    return await stream.read()
            except s3.exceptions.NoSuchKey:
                raise FileNotFoundError(f"Asset '{asset_id}' not found in S3")
            except Exception as e:
                raise RuntimeError(f"S3 get failed: {str(e)}")

    async def save_asset(self, asset_id: str, data: bytes) -> str:
        async with self.session.client("s3", endpoint_url=self.endpoint_url) as s3:
            try:
                await s3.put_object(Bucket=self.bucket_name, Key=asset_id, Body=data)
                return asset_id
            except Exception as e:
                raise RuntimeError(f"S3 save failed: {str(e)}")

    async def list_assets(self, prefix: str) -> List[AssetMetadata]:
        if prefix and not prefix.endswith("/"):
            prefix += "/"
            
        async with self.session.client("s3", endpoint_url=self.endpoint_url) as s3:
            try:
                paginator = s3.get_paginator("list_objects_v2")
                results = []
                
                async for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix, Delimiter="/"):
                    for folder in page.get("CommonPrefixes", []):
                        name = folder["Prefix"].strip("/").split("/")[-1]
                        results.append(AssetMetadata(
                            name=name,
                            path=folder["Prefix"],
                            is_dir=True
                        ))
                    
                    for obj in page.get("Contents", []):
                        if obj["Key"] == prefix:
                            continue
                        results.append(AssetMetadata(
                            name=obj["Key"].split("/")[-1],
                            path=obj["Key"],
                            is_dir=False,
                            size=obj["Size"],
                            modified=obj["LastModified"].timestamp()
                        ))
                return results
            except Exception as e:
                raise RuntimeError(f"S3 list failed: {str(e)}")
