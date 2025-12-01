from fastapi import APIRouter, status, Response, Depends, Form, UploadFile, File, HTTPException
from typing import List, Optional
from schemas.user_details_schema import UserDetailsRead
from services.user_details_service import UserDetailsService
from utils.dependencies import AdminUser, DBSession, CurrentUser
from fastapi.responses import StreamingResponse
import io

router = APIRouter()

# ==========================================
#  USER SELF-MANAGEMENT (Authenticated)
# ==========================================

@router.post(
    "/user_entry",
    response_model=UserDetailsRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create user entry (Multipart Form)"
)
async def create_my_details(
    db: DBSession, 
    current_user: CurrentUser,
    # Form fields must be defined explicitly for Multipart
    first_name: str = Form(...),
    last_name: str = Form(...),
    gender: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    state_province: Optional[str] = Form(None),
    qualification: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    cv_file: Optional[UploadFile] = File(None) # Optional file upload
):
    """
    Create a profile entry. Accepts Multipart/Form-Data.
    """
    # Pack data into a dictionary
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "phone": phone,
        "city": city,
        "state_province": state_province,
        "qualification": qualification,
        "skills": skills
    }
    
    return await UserDetailsService.create_details(
        db, 
        data=data, 
        cv_file=cv_file, 
        user_id=current_user.id
    )

@router.put(
    "/user_entry",
    response_model=UserDetailsRead,
    summary="Update current user's entry (Multipart Form)"
)
async def update_my_details(
    db: DBSession, 
    current_user: CurrentUser,
    # All fields optional for Update
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    gender: Optional[str] = Form(None),
    phone: Optional[str] = Form(None),
    city: Optional[str] = Form(None),
    state_province: Optional[str] = Form(None),
    qualification: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    cv_file: Optional[UploadFile] = File(None)
):
    """
    Update profile entry. Accepts Multipart/Form-Data.
    """
    data = {
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "phone": phone,
        "city": city,
        "state_province": state_province,
        "qualification": qualification,
        "skills": skills
    }
    
    # Remove None values so we don't overwrite existing data with nulls
    data = {k: v for k, v in data.items() if v is not None}

    return await UserDetailsService.update_my_details(
        db, 
        user_id=current_user.id, 
        update_data=data, 
        cv_file=cv_file
    )

@router.get(
    "/user_entry/cv",
    summary="Download the CV/Resume"
)
def download_my_cv(db: DBSession, current_user: CurrentUser):
    """
    Downloads the binary file stored in the database.
    """
    return UserDetailsService.get_cv_file(db, user_id=current_user.id)

@router.get("/user_entry", response_model=UserDetailsRead)
def read_my_details(db: DBSession, current_user: CurrentUser):
    return UserDetailsService.get_my_details(db, user_id=current_user.id)