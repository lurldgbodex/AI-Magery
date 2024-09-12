import pytest
from unittest.mock import patch, MagicMock
from backend.minio.minio_service import MinioService


@pytest.fixture
def minio_service(monkeypatch):
    with patch('backend.minio.minio_service.Minio') as mock_minio:
        mock_client = MagicMock()
        mock_minio.return_value = mock_client

        monkeypatch.setenv("MINIO_SECRET_KEY", "mock_secret_key")
        monkeypatch.setenv("MINIO_ACCESS_KEY", "mock_access_key")
        monkeypatch.setenv("MINIO_URL", "localhost:9000")
        monkeypatch.setenv("MINIO_BUCKET_NAME", "mock-bucket-name")

        service = MinioService()

        return service, mock_client


def test_create_bucket(minio_service):
    """unit test the minio service method to create a bucket"""
    minio_service, mock_client = minio_service

    mock_client.bucket_exists.return_value = False

    minio_service.create_bucket()

    mock_client.bucket_exists.assert_called_with(minio_service.bucket_name)
    mock_client.make_bucket.assert_called_with(minio_service.bucket_name)


def test_create_bucket_exist(minio_service):
    """unit test for minio service method to create a bucket when exist"""
    minio_service, mock_client = minio_service

    mock_client.bucket_exists.return_value = True

    minio_service.create_bucket()

    mock_client.bucket_exists.assert_called_with(minio_service.bucket_name)
    mock_client.make_bucket.assert_not_called()


def test_upload_image(minio_service):
    minio_service, mock_client = minio_service

    minio_service.upload_image('path/to/mock_image.png')

    mock_client.fput_object.assert_called_with(
        minio_service.bucket_name,
        'mock_image.png',
        'path/to/mock_image.png'
    )
