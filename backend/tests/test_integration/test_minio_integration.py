import pytest
from backend.minio.minio_service import MinioService


@pytest.fixture
def minio_service():
    return MinioService()


def test_create_bucket_integration(minio_service):
    """
    Integration test to ensure minio correctly creates a bucket
    """
    minio_service.create_bucket()

    assert minio_service.minio_client.bucket_exists(
        minio_service.bucket_name) is True


def test_upload_image_integration(minio_service):
    """
    integration test to ensure that file upload to minio is successful
    """
    minio_service.create_bucket()

    file_path = 'backend/logo-sg.png'
    minio_service.upload_image(file_path)

    bucket_objects = list(minio_service
                          .minio_client
                          .list_objects(minio_service.bucket_name))

    assert any(obj.object_name == "logo-sg.png" for obj in bucket_objects)
