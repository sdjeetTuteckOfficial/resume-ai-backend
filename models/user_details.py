from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship, backref
from database import Base

class UserDetails(Base):
    # Updated table name as requested
    __tablename__ = "t_user_details"

    id = Column(Integer, primary_key=True, index=True)
    # Foreign key linking to the existing User model (assuming users table is still "users")
    # unique=True enforces 1-to-1 at the Database level
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    state_province = Column(String(100), nullable=True)
    qualification = Column(String(200), nullable=True)
    skills = Column(Text, nullable=True)  # Store as comma-separated text or JSON string
    cv_file_url = Column(String(500), nullable=True) # Path to the uploaded resume

    # Relationship back to the User model
    # uselist=False ensures accessing user.details returns a single object, not a list
    user = relationship("User", backref=backref("details", uselist=False))