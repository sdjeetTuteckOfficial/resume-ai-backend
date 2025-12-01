from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, UploadFile
from fastapi.responses import StreamingResponse, Response
from models.user_details import UserDetails
import io

class UserDetailsService:
    
    @staticmethod
    async def create_details(db: Session, data: dict, cv_file: UploadFile, user_id: int):
        # 1. Check if details exist
        existing_details = db.query(UserDetails).filter(UserDetails.user_id == user_id).first()
        if existing_details:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="User details already exist. Please update."
            )
            
        # 2. Handle File (if provided)
        file_data = None
        filename = None
        content_type = None
        
        if cv_file:
            file_data = await cv_file.read()
            filename = cv_file.filename
            content_type = cv_file.content_type

        # 3. Create entry
        try:
            db_details = UserDetails(
                **data, # This now includes job_id
                cv_file_data=file_data,
                cv_filename=filename,
                cv_content_type=content_type,
                user_id=user_id
            )
            db.add(db_details)
            db.commit()
            db.refresh(db_details)
            return db_details
        except IntegrityError as e:
            db.rollback()
            # This handles cases where the job_id provided does not exist in t_job_details
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid data provided. Check if Job ID exists."
            )

    @staticmethod
    async def update_my_details(db: Session, user_id: int, update_data: dict, cv_file: UploadFile):
        db_details = db.query(UserDetails).filter(UserDetails.user_id == user_id).first()
        if not db_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User details not found")
            
        try:
            # 1. Update text fields (includes job_id if present)
            for key, value in update_data.items():
                setattr(db_details, key, value)
                
            # 2. Update File (only if a new one is uploaded)
            if cv_file:
                db_details.cv_file_data = await cv_file.read()
                db_details.cv_filename = cv_file.filename
                db_details.cv_content_type = cv_file.content_type
                
            db.commit()
            db.refresh(db_details)
            return db_details
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid data provided. Check if Job ID exists."
            )

    # ... (Get methods remain unchanged) ...
    @staticmethod
    def get_my_details(db: Session, user_id: int):
        details = db.query(UserDetails).filter(UserDetails.user_id == user_id).first()
        if not details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User details not found")
        return details

    @staticmethod
    def get_cv_file(db: Session, user_id: int):
        details = db.query(UserDetails).filter(UserDetails.user_id == user_id).first()
        
        if not details or not details.cv_file_data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CV not found")

        return Response(
            content=details.cv_file_data,
            media_type=details.cv_content_type or "application/octet-stream",
            headers={
                "Content-Disposition": f'attachment; filename="{details.cv_filename}"'
            }
        )