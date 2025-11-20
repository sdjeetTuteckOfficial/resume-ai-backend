from fastapi import APIRouter, status, Depends, Response
from sqlalchemy.orm import Session
from typing import List
from models.job_model import TJobDetails
from schemas.job_schema import JobCreate, JobRead
from services.job_service import JobService
from utils.dependencies import AdminUser, DBSession # Import our new dependency

# Create a router instance
router = APIRouter()

# NOTE: The dependency AdminUser ensures only authenticated admins can access these endpoints.
# The actual current_user object is not used in the JobService, but it enforces the permission check.

@router.post(
    "/",
    response_model=JobRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new job detail entry (Admin required)"
)
def create_new_job(job: JobCreate, db: DBSession, admin_user: AdminUser):
    """
    Create a new job detail entry. Requires valid Admin authentication token.
    """
    return JobService.create_job(db, job)

@router.get(
    "/",
    response_model=List[JobRead],
    summary="List all job detail entries (Admin required)"
)
def read_all_jobs(db: DBSession, admin_user: AdminUser, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of all job detail entries, paginated. Requires valid Admin authentication token.
    """
    return JobService.get_jobs(db, skip=skip, limit=limit)

@router.get(
    "/{job_id}",
    response_model=JobRead,
    summary="Get a specific job detail entry by job_id (Admin required)"
)
def read_job_by_id(job_id: str, db: DBSession, admin_user: AdminUser):
    """
    Retrieve a single job detail entry using its admin-provided `job_id`. Requires valid Admin authentication token.
    """
    return JobService.get_job_by_id(db, job_id)

@router.put(
    "/{job_id}",
    response_model=JobRead,
    summary="Update an existing job detail entry by job_id (Admin required)"
)
def update_job_details(job_id: str, job_update: JobCreate, db: DBSession, admin_user: AdminUser):
    """
    Update the details of an existing job entry. Requires valid Admin authentication token.
    """
    return JobService.update_job(db, job_id, job_update)

@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a job detail entry by job_id (Admin required)"
)
def delete_job_details(job_id: str, db: DBSession, admin_user: AdminUser):
    """
    Delete a job detail entry using its admin-provided `job_id`. Returns 204 No Content on success. Requires valid Admin authentication token.
    """
    JobService.delete_job(db, job_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)