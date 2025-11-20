from sqlalchemy.orm import Session
from models.job_model import TJobDetails
from schemas.job_schema import JobCreate
from fastapi import HTTPException, status

class JobService:
    @staticmethod
    def create_job(db: Session, job: JobCreate) -> TJobDetails:
        # Check for existing job_id to maintain uniqueness constraint
        if db.query(TJobDetails).filter(TJobDetails.job_id == job.job_id).first():
            raise HTTPException(status_code=400, detail=f"Job ID '{job.job_id}' already exists.")

        db_job = TJobDetails(**job.model_dump())
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job

    @staticmethod
    def get_jobs(db: Session, skip: int = 0, limit: int = 100) -> list[TJobDetails]:
        return db.query(TJobDetails).offset(skip).limit(limit).all()

    @staticmethod
    def get_job_by_id(db: Session, job_id: str) -> TJobDetails:
        job = db.query(TJobDetails).filter(TJobDetails.job_id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        return job

    @staticmethod
    def update_job(db: Session, job_id: str, job_update: JobCreate) -> TJobDetails:
        db_job = JobService.get_job_by_id(db, job_id)
        
        # Check if the new job_id conflicts with another existing job
        if job_update.job_id != db_job.job_id and db.query(TJobDetails).filter(TJobDetails.job_id == job_update.job_id).first():
             raise HTTPException(status_code=400, detail=f"Cannot update: Job ID '{job_update.job_id}' already in use.")

        for key, value in job_update.model_dump(exclude_unset=True).items():
            setattr(db_job, key, value)
        
        db.commit()
        db.refresh(db_job)
        return db_job

    @staticmethod
    def delete_job(db: Session, job_id: str) -> None:
        db_job = JobService.get_job_by_id(db, job_id)
        db.delete(db_job)
        db.commit()