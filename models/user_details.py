from sqlalchemy import Column, Integer, String, ForeignKey, Text, LargeBinary
from sqlalchemy.orm import relationship, backref
from database import Base

class UserDetails(Base):
    __tablename__ = "t_user_details"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False, index=True)
    
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(String(20), nullable=True)
    phone = Column(String(20), nullable=True)
    city = Column(String(100), nullable=True)
    state_province = Column(String(100), nullable=True)
    qualification = Column(String(200), nullable=True)
    skills = Column(Text, nullable=True)
    
    # CHANGED: Store file binary data and metadata
    cv_filename = Column(String(255), nullable=True)
    cv_content_type = Column(String(100), nullable=True)
    cv_file_data = Column(LargeBinary, nullable=True) 

    user = relationship("User", backref=backref("details", uselist=False))