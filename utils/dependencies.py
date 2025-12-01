# dependencies.py
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

# Import the DB generator
from database import get_db

# Import the User model
from models.user import User

# Import BOTH security functions
from utils.security import get_current_admin, get_current_active_user

# 1. Dependency for Admin Only (POST, PUT, DELETE)
AdminUser = Annotated[User, Depends(get_current_admin)]

# 2. Dependency for Any Authenticated User (GET)
# This allows Admins AND Regular Users, as long as they are active.
CurrentUser = Annotated[User, Depends(get_current_active_user)]

# 3. DB Session Dependency
DBSession = Annotated[Session, Depends(get_db)]