from minio import Minio
from minio.error import S3Error
from dotenv import load_dotenv
import os
from datetime import timedelta


if os.getenv("CI") is None:
    load_dotenv()


class MinioService:
    """A class for the minIO s3 bucket functionalities"""

    def __init__(self) -> None:
        """Initializes the minio client"""
        self.minio_secret_key = os.getenv("MINIO_SECRET_KEY")
        self.minio_access_key = os.getenv("MINIO_ACCESS_KEY")
        self.minio_url = os.getenv("MINIO_URL")
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME")

        if not all([self.minio_secret_key,
                    self.minio_access_key,
                    self.minio_url, self.bucket_name
                    ]):
            raise ValueError("Missing one or more required \
                             environment variables for MinIO config.")

        self.minio_client = Minio(
            self.minio_url,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
            secure=False
        )

    def create_bucket(self) -> None:
        """Creates a minio bucket if it does not exist"""
        found = self.minio_client.bucket_exists(self.bucket_name)

        if not found:
            self.minio_client.make_bucket(self.bucket_name)
            print(f"Created bucket: {self.bucket_name}")
        else:
            print(f"Bucket {self.bucket_name} already exists")

    def upload_image(self, file_path: str) -> None:
        """
        upload an image to the connected minio bucket

        :file_path: The path of the file to upload to minio bucket
        """
        file_name = os.path.basename(file_path)
        try:
            self.minio_client.fput_object(
                self.bucket_name, file_name, file_path)
            print(f"Successfully uploaded {file_name} to bucket")
        except Exception as e:
            print(f"Failed to upload image {file_name}: {e}")
            raise e

    def get_object_url(self, object_name: str,
                       expiration: timedelta = timedelta(hours=1)) -> str:
        """
        Retrieve an image from the MinIO bucket and
        save it to the specified path

        :param object_name: The name of the object in the MinIO bucket
        :param expiration: The duration for which the pre-signed url
         will be valid
        """
        try:
            presigned_url = self.minio_client.presigned_get_object(
                self.bucket_name, object_name, expires=expiration
            )

            print(f"Pre-signed URL: {presigned_url}")
            return presigned_url
        except S3Error as err:
            print(f"Failed to generated pre-signed url: {err.message}")
            raise err
