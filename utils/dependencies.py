from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

# Reusing imports needed by the type hints and assumed context
from models.job_model import UserRole # Re-using the UserRole definition

# Import the completed authentication functions from the security module
# This function handles token validation, user retrieval, active status, and admin role check.
from utils.security import get_current_admin 

# Import the actual database session dependency from database.py
from database import get_db

# Import the actual User model from models/user.py
from models.user import User
# --- End Placeholder Definitions ---

# Convenience type hint for Admin users in path operations
# We now use the user's provided 'get_current_admin' function directly.
# NOTE: The previous custom check function 'get_current_admin_user' is no longer needed.
AdminUser = Annotated[User, Depends(get_current_admin)]

# Convenience type hint for DB Session
DBSession = Annotated[Session, Depends(get_db)]