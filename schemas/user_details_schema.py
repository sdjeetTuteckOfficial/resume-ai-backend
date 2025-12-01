from pydantic import BaseModel
from typing import Optional

# Base properties (Excluding file info)
class UserDetailsBase(BaseModel):
    first_name: str
    last_name: str
    gender: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    qualification: Optional[str] = None
    skills: Optional[str] = None

# Properties returned to the client
class UserDetailsRead(UserDetailsBase):
    id: int
    user_id: int
    cv_filename: Optional[str] = None
    # We create a computed field or just send the filename to indicate existence
    # Do not send the LargeBinary data here, it will crash the JSON response.

    class Config:
        from_attributes = True