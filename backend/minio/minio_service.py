from minio import Minio
from dotenv import load_dotenv
import os


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
        """upload an image to the connected minio bucket"""
        file_name = os.path.basename(file_path)
        try:
            self.minio_client.fput_object(
                self.bucket_name, file_name, file_path)
            print(f"Successfully uploaded {file_name} to bucket")
        except Exception as e:
            print(f"Failed to upload image {file_name}: {e}")
