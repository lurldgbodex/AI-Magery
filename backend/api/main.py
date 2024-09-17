from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from backend.models.config import SessionLocal, engine
from backend.models.jobs import Base
from backend.api.crud import create_job, get_job_by_id
from backend.utils.validate_image import validate_image


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    """
    The default home page url of the api.
    displays a welcome message when a get request is received.
    """
    return {
        "message": "Welcome to the Image Transformation API!"
    }


@app.post("/api/v1/jobs/upload")
async def create_new_job(
    prompts: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    endpoint to create a new job. takes image and prompts from user
    : params prompts: user instruction to transform inage
    : params image: image to transform
    """
    validate_image(image)

    image_filename = f"temp_{image.filename}"
    with open(image_filename, "wb") as buffer:
        buffer.write(await image.read())

    job = create_job(db=db, status="pending", image_url=None, prompts=prompts)
    return {
        "job_id": job.job_id,
        "message": "image transformation job created successfully"
    }


@app.get("/api/v1/jobs/{job_id}")
def read_job(job_id: int, db: Session = Depends(get_db)):
    """
    defines the endpoint to get a job
    : params job_id: id of the job to get
    """
    job = get_job_by_id(db=db, job_id=job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
