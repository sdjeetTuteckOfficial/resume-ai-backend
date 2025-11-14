# ==================== routers/auth.py ====================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.user import UserCreate, UserLogin, UserResponse, Token, VerifyOTP, ForgotPassword, ResetPassword
from services.auth_service import AuthService
from utils.security import get_current_active_user, get_current_admin
from models.user import User, UserRole

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    #Register a new user
    return AuthService.create_user(db, user)

@router.post("/register-admin", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_admin(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    #Register a new admin (only accessible by existing admins)
    return AuthService.create_user(db, user, role=UserRole.ADMIN)

@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    #Login user
    access_token, user = AuthService.login_user(db, user_credentials.email, user_credentials.password)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/verify-otp")
def verify_otp(otp_data: VerifyOTP, db: Session = Depends(get_db)):
    #Verify OTP for email verification
    AuthService.verify_otp(db, otp_data.email, otp_data.otp, "verification")
    return {"message": "Email verified successfully"}

@router.post("/forgot-password")
def forgot_password(forgot_data: ForgotPassword, db: Session = Depends(get_db)):
    #Request password reset OTP
    AuthService.forgot_password(db, forgot_data.email)
    return {"message": "OTP sent to your email"}

@router.post("/reset-password")
def reset_password(reset_data: ResetPassword, db: Session = Depends(get_db)):
    #Reset password using OTP
    AuthService.reset_password(db, reset_data.email, reset_data.otp, reset_data.new_password)
    return {"message": "Password reset successfully"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    #Get current user information
    return current_user

@router.get("/admin/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin)
):
    #Get all users (admin only)
    users = db.query(User).all()
    return users