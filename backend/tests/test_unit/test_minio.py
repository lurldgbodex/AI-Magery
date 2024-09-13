import os
import unittest
from datetime import timedelta
from unittest.mock import patch, MagicMock
from minio.error import S3Error
from backend.minio.minio_service import MinioService


class TestMinioService(unittest.TestCase):

    @patch('backend.minio.minio_service.Minio')
    def setUp(self, mock_minio):
        """Set up mock environment and minio client for each test."""
        mock_client = MagicMock()
        mock_minio.return_value = mock_client

        os.environ["MINIO_SECRET_KEY"] = "mock_secret_key"
        os.environ["MINIO_ACCESS_KEY"] = "mock_access_key"
        os.environ["MINIO_URL"] = "localhost:9000"
        os.environ["MINIO_BUCKET_NAME"] = "mock-bucket-name"

        self.minio_service = MinioService()
        self.mock_client = mock_client

    def test_missing_environment_variables(self):
        """Unit test to check for missing environment
          variables for MinIO config."""
        with patch.dict('os.environ', {'MINIO_SECRET_KEY': '',
                                       'MINIO_ACCESS_KEY': '',
                                       'MINIO_URL': '',
                                       'MINIO_BUCKET_NAME': ''}):
            with self.assertRaises(ValueError) as context:
                MinioService()

            self.assertEqual(str(context.exception),
                             "Missing one or more required \
                             environment variables for MinIO config.")

    def test_create_bucket(self):
        """Unit test the Minio service method to create a bucket."""
        self.mock_client.bucket_exists.return_value = False

        self.minio_service.create_bucket()

        self.mock_client.bucket_exists.assert_called_with(
            self.minio_service.bucket_name)
        self.mock_client.make_bucket.assert_called_with(
            self.minio_service.bucket_name)

    def test_create_bucket_exist(self):
        """Unit test for Minio service method when bucket already exists."""
        self.mock_client.bucket_exists.return_value = True

        self.minio_service.create_bucket()

        self.mock_client.bucket_exists.assert_called_with(
            self.minio_service.bucket_name)
        self.mock_client.make_bucket.assert_not_called()

    def test_upload_image(self):
        """Unit test for the image upload method."""
        self.minio_service.upload_image('path/to/mock_image.png')

        self.mock_client.fput_object.assert_called_with(
            self.minio_service.bucket_name,
            'mock_image.png',
            'path/to/mock_image.png'
        )

    def test_upload_image_failure(self):
        """Unit test for image upload failure."""
        self.mock_client.fput_object.side_effect = Exception(
            "Failed to upload image")

        with self.assertRaises(Exception):
            self.minio_service.upload_image("path/to/image.png")

        self.mock_client.fput_object.assert_called_with(
            self.minio_service.bucket_name,
            'image.png',
            'path/to/image.png'
        )

    def test_get_object_url_success(self):
        """Unit test for successful generation of a pre-signed URL."""
        mock_url = 'http://minio.url/path/to/image.jpg'
        self.mock_client.presigned_get_object.return_value = mock_url
        object_name = 'path/to/image.jpg'

        url = self.minio_service.get_object_url(
            object_name, timedelta(hours=2))

        self.assertEqual(url, mock_url)
        self.mock_client.presigned_get_object.assert_called_once_with(
            self.minio_service.bucket_name, object_name, expires=timedelta(
                hours=2)
        )

    def test_get_object_url_failure(self):
        """Unit test for failure to generate pre-signed URL
          due to MinIO error."""
        self.mock_client.presigned_get_object.side_effect = S3Error(
            code='NoSuchBucket', message='The specified bucket does not exist',
            resource='/non-existent-bucket', request_id='12345',
            host_id='67890', response=404, bucket_name='non-existent-bucket'
        )

        object_name = 'path/to/image.jpg'

        with self.assertRaises(S3Error):
            self.minio_service.get_object_url(
                object_name, timedelta(hours=1))

        self.mock_client.presigned_get_object.assert_called_once_with(
            self.minio_service.bucket_name, object_name, expires=timedelta(
                hours=1)
        )
