from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.user_details import UserDetails
from schemas.user_details_schema import UserDetailsCreate, UserDetailsUpdate

class UserDetailsService:
    
    @staticmethod
    def create_details(db: Session, details: UserDetailsCreate, user_id: int):
        # 1. Check if details already exist for this user (One-to-One enforcement)
        existing_details = db.query(UserDetails).filter(UserDetails.user_id == user_id).first()
        if existing_details:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="User details already exist. Please update the existing entry."
            )
            
        # 2. Create new entry
        db_details = UserDetails(**details.dict(), user_id=user_id)
        db.add(db_details)
        db.commit()
        db.refresh(db_details)
        return db_details

    @staticmethod
    def get_my_details(db: Session, user_id: int):
        details = db.query(UserDetails).filter(UserDetails.user_id == user_id).first()
        if not details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User details not found")
        return details

    @staticmethod
    def get_details_by_id(db: Session, details_id: int):
        details = db.query(UserDetails).filter(UserDetails.id == details_id).first()
        if not details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User details not found")
        return details
        
    @staticmethod
    def get_all_details(db: Session, skip: int = 0, limit: int = 100):
        return db.query(UserDetails).offset(skip).limit(limit).all()

    @staticmethod
    def update_my_details(db: Session, user_id: int, details_update: UserDetailsUpdate):
        db_details = db.query(UserDetails).filter(UserDetails.user_id == user_id).first()
        if not db_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User details not found")
            
        # Only update fields that were provided
        update_data = details_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_details, key, value)
            
        db.commit()
        db.refresh(db_details)
        return db_details
        
    @staticmethod
    def delete_details(db: Session, details_id: int):
        db_details = db.query(UserDetails).filter(UserDetails.id == details_id).first()
        if not db_details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User details not found")
            
        db.delete(db_details)
        db.commit()