import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models.jobs import Base
from backend.api.crud import create_job, get_job_by_id, update_job_status, \
    update_image_url, get_all_jobs, delete_job


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)


def test_create_job(db):
    job = create_job(db, status="pending", image_url=None,
                     prompts="test prompt")
    assert job.status == "pending"
    assert job.image_url is None
    assert job.prompts == 'test prompt'
    assert job.job_id is not None


def test_get_job_by_id(db):
    new_job = create_job(db, status="pending",
                         image_url=None, prompts="test prompt")
    fetched_job = get_job_by_id(db, new_job.job_id)
    assert fetched_job.job_id == new_job.job_id
    assert fetched_job.prompts == new_job.prompts


def test_update_job_status(db):
    job = create_job(db, status="pending", image_url=None,
                     prompts="test prompt")
    updated_job = update_job_status(db, job.job_id, "processing")
    assert updated_job.status == "processing"
    assert updated_job.started_at is not None

    # update status to completed
    updated_job = update_job_status(db, job.job_id, "completed")
    assert updated_job.status == "completed"
    assert updated_job.completed_at is not None


def test_update_image_url(db):
    job = create_job(db, status="pending", image_url=None,
                     prompts="test prompt")
    updated_job = update_image_url(
        db, job.job_id, "http://example.com/image.png")
    assert updated_job.image_url == "http://example.com/image.png"


def test_get_all_jobs(db):
    create_job(db, status="pending", image_url=None, prompts="test prompt")
    create_job(db, status="completed",
               image_url="http://example.ocm", prompts="test prompt2")
    jobs = get_all_jobs(db)
    assert len(jobs) == 2
    assert jobs[0].status == "pending"
    assert jobs[1].status == "completed"


def test_delete_job(db):
    job = create_job(db, status="pending", image_url=None,
                     prompts="test prompt")
    deleted_job = delete_job(db, job.job_id)
    assert deleted_job is not None
    assert get_job_by_id(db, job.job_id) is None
