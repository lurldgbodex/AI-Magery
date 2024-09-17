from sqlalchemy.orm import Session
from datetime import datetime
from backend.models.jobs import Job


def create_job(db: Session, status: str, image_url: str, prompts: str):
    new_job = Job(status=status, image_url=image_url, prompts=prompts)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


def get_job_by_id(db: Session, job_id: int):
    """function to get a job by id in the databse
    :param job_id: id of the job to get
    :db: database session

    :returns: the job
    """
    return db.query(Job).filter(Job.job_id == job_id).first()


def update_job_status(db: Session, job_id: int, status: str):
    """updates the status of job in the database
    :param db: database session
    :job_id: id of the job to update
    :status: status data

    :return: the Job
    """
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if job:
        job.status = status
        if status == "processing":
            job.started_at = datetime.now()
        if status == "completed":
            job.completed_at = datetime.now()

        db.commit()
        db.refresh(job)
    return job


def update_image_url(db: Session, job_id: int, image_url: str):
    """update the image url in the database
    :param job_id: id of the job to update
    :param image_url: url of the image
    """
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if job:
        job.image_url = image_url
        db.commit()
        db.refresh(job)
    return job


def get_all_jobs(db: Session):
    """gets all job in the database
    :param db: database session

    :returns: all jobs
    """
    return db.query(Job).all()


def delete_job(db: Session, job_id: int):
    """deletes a job from the database
    :param db: database session
    :param job_id: id of the job to delete
    """
    job = db.query(Job).filter(Job.job_id == job_id).first()
    if job:
        db.delete(job)
        db.commit()
    return job
