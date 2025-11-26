# job_router.py
from fastapi import APIRouter, status, Response
from typing import List
from schemas.job_schema import JobCreate, JobRead
from services.job_service import JobService
# Import the new CurrentUser dependency
from utils.dependencies import AdminUser, DBSession, CurrentUser 

router = APIRouter()

# --- ADMIN ONLY (Keep AdminUser) ---
@router.post(
    "/",
    response_model=JobRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new job detail entry (Admin required)"
)
def create_new_job(job: JobCreate, db: DBSession, admin_user: AdminUser):
    return JobService.create_job(db, job)

# --- OPEN TO ALL USERS (Switch to CurrentUser) ---
@router.get(
    "/",
    response_model=List[JobRead],
    summary="List all job detail entries (Authenticated Users)"
)
def read_all_jobs(db: DBSession, current_user: CurrentUser, skip: int = 0, limit: int = 100):
    """
    Accessible by both Admins and Users.
    """
    return JobService.get_jobs(db, skip=skip, limit=limit)

@router.get(
    "/{job_id}",
    response_model=JobRead,
    summary="Get a specific job detail entry (Authenticated Users)"
)
def read_job_by_id(job_id: str, db: DBSession, current_user: CurrentUser):
    """
    Accessible by both Admins and Users.
    """
    return JobService.get_job_by_id(db, job_id)

# --- ADMIN ONLY (Keep AdminUser) ---
@router.put(
    "/{job_id}",
    response_model=JobRead,
    summary="Update an existing job detail entry (Admin required)"
)
def update_job_details(job_id: str, job_update: JobCreate, db: DBSession, admin_user: AdminUser):
    return JobService.update_job(db, job_id, job_update)

@router.delete(
    "/{job_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a job detail entry (Admin required)"
)
def delete_job_details(job_id: str, db: DBSession, admin_user: AdminUser):
    JobService.delete_job(db, job_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)