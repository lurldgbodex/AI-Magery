from fastapi.testclient import TestClient
from io import BytesIO
from PIL import Image
from backend.api.main import app
from unittest.mock import patch, MagicMock


client = TestClient(app)


class Job:
    def __init__(self, job_id, status, prompt):
        self.job_id = job_id
        self.status = status
        self.prompts = prompt


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Welcome to the Image Transformation API!"


@patch('backend.api.main.create_job')
def test_create_new_job(mock_create_job):

    image_bytes = BytesIO()
    image = Image.new('RGB', (100, 100))
    image.save(image_bytes, format='JPEG')
    image_bytes.seek(0)

    prompts = "Turn this into a cartoon."

    mock_job = MagicMock()
    mock_job.job_id = 1
    mock_job.status = "pending"
    mock_create_job.return_value = mock_job

    response = client.post(
        "/api/v1/jobs/upload",
        files={"image": ("test_image.png", image_bytes, "image/jpeg")},
        data={"prompts": prompts}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == 1
    assert data["message"] == "image transformation job created successfully"


@patch('backend.api.main.create_job')
def test_create_new_job_invalid_image(mock_create_job):
    image = "invalid-image"
    prompts = "test prompt"

    response = client.post(
        "/api/v1/jobs/upload",
        files={"image": ("test_image.png", image, "image/png")},
        data={"prompts": prompts}
    )

    assert response.status_code == 400


@patch('backend.api.main.get_job_by_id')
def test_read_job_found(mock_get_job_by_id):
    # Setup
    mock_job = Job(job_id=1, status="pending", prompt="test prompt")
    mock_get_job_by_id.return_value = mock_job

    response = client.get("/api/v1/jobs/1")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == 1
    assert data["status"] == "pending"
    assert data["prompts"] == "test prompt"


# Test to handle job not found
@patch('backend.api.main.get_job_by_id')
def test_read_job_not_found(mock_get_job_by_id):
    # Setup
    mock_get_job_by_id.return_value = None

    response = client.get("/api/v1/jobs/999")

    # Assertions
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Job not found"
