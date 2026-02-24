import pytest
import os
from moto import mock_aws
import boto3
from morphosx.app.storage.s3 import S3Storage

@pytest.fixture
def s3_setup():
    with mock_aws():
        # Create a mock bucket
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket="test-bucket")
        yield "test-bucket"

@pytest.mark.asyncio
async def test_s3_storage_save_and_get(s3_setup):
    bucket = s3_setup
    storage = S3Storage(bucket_name=bucket, region_name="us-east-1")
    
    asset_id = "test-image.jpg"
    data = b"fake-image-bytes"
    
    # Save asset
    saved_id = await storage.save_asset(asset_id, data)
    assert saved_id == asset_id
    
    # Retrieve asset
    retrieved_data = await storage.get_asset(asset_id)
    assert retrieved_data == data

@pytest.mark.asyncio
async def test_s3_storage_not_found(s3_setup):
    bucket = s3_setup
    storage = S3Storage(bucket_name=bucket, region_name="us-east-1")
    
    with pytest.raises(FileNotFoundError):
        await storage.get_asset("non-existent.jpg")
