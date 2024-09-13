# AI-MAGERY

## Overview

[![.github/workflows/pyton-ci.yml](https://github.com/lurldgbodex/ai-magery/actions/workflows/pyton-ci.yml/badge.svg)](https://github.com/lurldgbodex/ai-magery/actions/workflows/pyton-ci.yml)

This is the backend component of the AI Image Transformation Application. It handles API requests for image transformation tasks and uses AI models like Stable Diffusion to generate modified images.

## Features

- **Image Upload:** Accepts image uploads from users.
- **Image Transformation:** Processes images through Stable Diffusion and modifies key elements (e.g., background, attire).
- **Background Task Processing:** Celery is used to handle image transformation tasks asynchronously.

## Technology Stack

- **FastAPI**: Web framework for the backend API.
- **Celery**: Distributed task queue for background processing.
- **Redis**: Message broker for Celery tasks.
- **Stable Diffusion**: AI model for image transformation.

## Setup Instructions

### 1. Install Dependencies

Ensure that you have the project dependencies installed in a virtual environment.

```bash
pip install -r requirements.txt
```

### 2. Setup Minio

#### Quick Setup

- Create a .env file in the root of the project and define the following vaules

```bash
    MINIO_USER=your-minio_user
    MINIO_PASSWORD=your-minio_password
```

- Run MinIO with Docker compose

```bash
 docker compose up -d
```

- MinIO will be available on:
  - MinIO console: http://localhost:9001 \
    Log in using the `MINIO_USER` AND `MINIO_PASSWORD` values you set
  - MinIO API: http://localhost:9000
- Access MinIO console: Once the service is running, visit the MinIO console, log in using the credentials from your .env file, and configure your access_key and secret_key if needed.
- Create a .env file in the `backend/` directory and define the following values

```bash
    MINIO_URL=localhost:9000
    MINIO_ACCESS_KEY=your-access-key
    MINIO_SECRET_KEY=your-secret-key
    MINIO_BUCKET_NAME=your-bucket-name
```

### 3. Run the FastAPI Application

To run the FastAPI app locally:

```bash
uvicorn api.main:app --reload
```

The API should now be accessible at `http://127.0.0.1:8000`

### 4. Running the celery workers

Start the celery worker to handle background tasks:

```bash
 celery -A tasks worker --loglevel=info
```

Make sure Redis is running

## Directory Structure

```graphql
backend/
|
|-- api/                    # FastAPI routes and api setup
|-- tasks/                  # Celery tasks
|-- models/                 # Stable Diffusion model management
|-- venv/                   # virtual environment
|-- requirements.txt        # python dependencies
|__ README.md               # backend documentation
```

## Endpoints

Image upload and Transformation

- `POST /api/v1/upload-image`: Uploads an image and returns the status of the transformation process.
- `GET /api/v1/result/{task_id}`: Retrieves the transformed image once the processing is complete.

## Future Plans

- Add advanced image transformation capabilities
- Add security measures for file uploads and storage

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.
