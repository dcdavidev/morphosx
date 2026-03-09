from unittest.mock import AsyncMock, patch

import pytest

from morphosx.app.storage.s3 import S3Storage


@pytest.mark.asyncio
async def test_s3_storage_save_and_get():
    """
    Test S3Storage using AsyncMock for aioboto3 to avoid issues with moto/aiobotocore.
    """
    bucket = "test-bucket"
    storage = S3Storage(bucket_name=bucket, region_name="us-east-1")

    asset_id = "test-image.jpg"
    data = b"fake-image-bytes"

    # Mock aioboto3 session and client
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client

    # Mock get_object response
    mock_body = AsyncMock()
    mock_body.__aenter__.return_value = mock_body
    mock_body.read.return_value = data
    mock_client.get_object.return_value = {"Body": mock_body}

    with patch.object(storage.session, "client", return_value=mock_client):
        # Test save_asset
        saved_id = await storage.save_asset(asset_id, data)
        assert saved_id == asset_id
        mock_client.put_object.assert_called_once_with(
            Bucket=bucket, Key=asset_id, Body=data
        )

        # Test get_asset
        retrieved_data = await storage.get_asset(asset_id)
        assert retrieved_data == data
        mock_client.get_object.assert_called_once_with(Bucket=bucket, Key=asset_id)


@pytest.mark.asyncio
async def test_s3_storage_not_found():
    """Test S3Storage when asset is missing (with mocked exceptions)."""
    bucket = "test-bucket"
    storage = S3Storage(bucket_name=bucket, region_name="us-east-1")

    # Mock client and its exceptions
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client

    # Simulate NoSuchKey exception
    class NoSuchKey(Exception):
        pass

    mock_client.exceptions.NoSuchKey = NoSuchKey
    mock_client.get_object.side_effect = NoSuchKey("Key not found")

    with patch.object(storage.session, "client", return_value=mock_client):
        with pytest.raises(FileNotFoundError):
            await storage.get_asset("missing.jpg")
