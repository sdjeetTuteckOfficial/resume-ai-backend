from sqlalchemy import Column, Integer, String, DateTime, func, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

# --- Assumed Base and UserRole definitions for compilation ---
Base = declarative_base()

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

# --- New TJobDetails Model ---
class TJobDetails(Base):
    __tablename__ = "t_job_details" # Renamed for consistency

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String(50), unique=True, index=True, nullable=False)
    job_name = Column(String(255), nullable=False)
    job_details = Column(String, nullable=False) # Use String for long text
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())