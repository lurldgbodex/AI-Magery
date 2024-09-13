import pytest
from backend.minio.minio_service import MinioService


@pytest.fixture(scope='module')
def minio_service():
    """
    Fixture to initialize the MinioService class.
    """
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
    object_name = 'logo-sg.png'
    minio_service.upload_image(file_path)

    bucket_objects = list(minio_service
                          .minio_client
                          .list_objects(minio_service.bucket_name))

    assert any(obj.object_name == object_name for obj in bucket_objects)

    minio_service.minio_client.remove_object(
        minio_service.bucket_name, object_name)


def test_get_object_url_integration(minio_service):
    """
    Test retrieving a pre-signed url from the MinIO Service.
    """
    object_name = "test-image.jpg"

    with open("/tmp/test-image.jpg", "w") as f:
        f.write("This is a test image content")

    minio_service.minio_client.fput_object(
        minio_service.bucket_name,
        object_name,
        "/tmp/test-image.jpg"
    )

    presigned_url = minio_service.get_object_url(object_name)

    assert presigned_url is not None
    assert presigned_url.startswith("http")

    minio_service.minio_client.remove_object(
        minio_service.bucket_name, object_name)
