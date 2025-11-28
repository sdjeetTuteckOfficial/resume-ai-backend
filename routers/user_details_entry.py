#user_details_entry.py
from fastapi import APIRouter, status, Response, Depends
from typing import List
from schemas.user_details_schema import UserDetailsCreate, UserDetailsRead, UserDetailsUpdate
from services.user_details_service import UserDetailsService
from utils.dependencies import AdminUser, DBSession, CurrentUser

router = APIRouter()

# ==========================================
#  USER SELF-MANAGEMENT (Authenticated)
# ==========================================

@router.post(
    "/user_entry",
    response_model=UserDetailsRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create user entry for the current user"
)
def create_my_details(details: UserDetailsCreate, db: DBSession, current_user: CurrentUser):
    """
    Create a profile entry for the logged-in user. Fails if one already exists.
    """
    return UserDetailsService.create_details(db, details, user_id=current_user.id)

@router.get(
    "/user_entry",
    response_model=UserDetailsRead,
    summary="Get current user's entry details"
)
def read_my_details(db: DBSession, current_user: CurrentUser):
    """
    Get the profile entry of the logged-in user.
    """
    return UserDetailsService.get_my_details(db, user_id=current_user.id)

@router.put(
    "/user_entry",
    response_model=UserDetailsRead,
    summary="Update current user's entry details"
)
def update_my_details(details_update: UserDetailsUpdate, db: DBSession, current_user: CurrentUser):
    """
    Update specific fields for the logged-in user's entry.
    """
    return UserDetailsService.update_my_details(db, user_id=current_user.id, details_update=details_update)


# ==========================================
#  ADMIN MANAGEMENT
# ==========================================

@router.get(
    "/",
    response_model=List[UserDetailsRead],
    summary="List all user details (Admin only)"
)
def read_all_details(db: DBSession, admin_user: AdminUser, skip: int = 0, limit: int = 100):
    """
    Admin: View all user details in the system.
    """
    return UserDetailsService.get_all_details(db, skip=skip, limit=limit)

@router.get(
    "/{details_id}",
    response_model=UserDetailsRead,
    summary="Get specific details by ID (Admin only)"
)
def read_details_by_id(details_id: int, db: DBSession, admin_user: AdminUser):
    """
    Admin: View specific details by the Details ID (not User ID).
    """
    return UserDetailsService.get_details_by_id(db, details_id)

@router.delete(
    "/{details_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user details entry (Admin only)"
)
def delete_user_details(details_id: int, db: DBSession, admin_user: AdminUser):
    """
    Admin: Delete a user details entry.
    """
    UserDetailsService.delete_details(db, details_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)