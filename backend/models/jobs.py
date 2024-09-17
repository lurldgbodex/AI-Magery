from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .config import Base


class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True, nullable=False)
    image_url = Column(String, nullable=True)
    prompts = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
