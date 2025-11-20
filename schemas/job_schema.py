from pydantic import BaseModel, Field
from datetime import datetime

# Base schema for creating or updating a job
class JobBase(BaseModel):
    job_id: str = Field(..., max_length=50, description="Unique identifier provided by admin.")
    job_name: str = Field(..., max_length=255, description="The human-readable name of the job.")
    job_details: str = Field(..., description="Detailed description or payload of the job.")

# Schema for creating a new job (inherits from base)
class JobCreate(JobBase):
    pass

# Schema for response/reading a job from the database
class JobRead(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime | None

    class Config:
        from_attributes = True # Allows mapping from SQLAlchemy object