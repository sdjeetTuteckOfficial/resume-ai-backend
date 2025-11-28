#user_details_schema.py
from pydantic import BaseModel
from typing import Optional

# Base properties shared by Create, Update, and Read schemas
class UserDetailsBase(BaseModel):
    first_name: str
    last_name: str
    gender: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    qualification: Optional[str] = None
    skills: Optional[str] = None
    cv_file_url: Optional[str] = None

# Properties required during creation
class UserDetailsCreate(UserDetailsBase):
    pass

# Properties for updating (all fields optional)
class UserDetailsUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    qualification: Optional[str] = None
    skills: Optional[str] = None
    cv_file_url: Optional[str] = None

# Properties returned to the client
class UserDetailsRead(UserDetailsBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True