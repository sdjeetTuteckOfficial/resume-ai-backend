from sqlalchemy import Column, Integer, String, ForeignKey, Text, LargeBinary
from sqlalchemy.orm import relationship, backref
from database import Base

# Ensure this import path is correct
from models.job_model import TJobDetails 

class UserDetails(Base):
    __tablename__ = "t_user_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    
    # --- THE FIX IS HERE ---
    # Don't use quotes "t_job_details.id". Use the class attribute TJobDetails.id
    # This ensures SQLAlchemy knows exactly which model you mean.
    job_id = Column(Integer, ForeignKey(TJobDetails.id), nullable=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    state_province = Column(String(100), nullable=True)
    qualification = Column(String(200), nullable=True)
    skills = Column(Text, nullable=True)
    
    # File binary data
    cv_filename = Column(String(255), nullable=True)
    cv_content_type = Column(String(100), nullable=True)
    cv_file_data = Column(LargeBinary, nullable=True) 

    # Relationships
    user = relationship("User", backref=backref("details", uselist=False))
    
    # This relationship is correct
    job = relationship(TJobDetails, backref="applicants")