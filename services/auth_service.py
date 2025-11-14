# ==================== services/auth_service.py ====================
from sqlalchemy.orm import Session
from models.user import User, UserRole
from models.otp import OTP
from schemas.user import UserCreate
from utils.security import hash_password, verify_password, create_access_token, generate_otp
from utils.email import send_otp_email
from datetime import datetime, timedelta, timezone
from config import settings
from fastapi import HTTPException, status

class AuthService:
    @staticmethod
    def create_user(db: Session, user: UserCreate, role: UserRole = UserRole.USER):
        print("USER>>>>>>👻", role)
        # Check if user exists
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        if db.query(User).filter(User.username == user.username).first():
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Create user
        db_user = User(
            email=user.email,
            username=user.username,
            hashed_password=hash_password(user.password),
            role=role,
            is_active=True,
            is_verified=False
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Generate and send OTP
        otp_code = generate_otp()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
        
        otp = OTP(
            email=user.email,
            otp_code=otp_code,
            purpose="verification",
            expires_at=expires_at
        )
        db.add(otp)
        db.commit()
        
        # Send OTP email
        send_otp_email(user.email, otp_code, "verification")
        
        return db_user
    
    @staticmethod
    def login_user(db: Session, email: str, password: str):
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        if not user.is_active:
            raise HTTPException(status_code=400, detail="User account is inactive")
        
        access_token = create_access_token(data={"sub": user.email})
        return access_token, user
    
    @staticmethod
    def verify_otp(db: Session, email: str, otp_code: str, purpose: str):
        otp = db.query(OTP).filter(
            OTP.email == email,
            OTP.otp_code == otp_code,
            OTP.purpose == purpose,
            OTP.is_used == False
        ).first()
        
        if not otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")
        
        if datetime.now(timezone.utc) > otp.expires_at:
            raise HTTPException(status_code=400, detail="OTP has expired")
        
        otp.is_used = True
        db.commit()
        
        if purpose == "verification":
            user = db.query(User).filter(User.email == email).first()
            if user:
                user.is_verified = True
                db.commit()
        
        return True
    
    @staticmethod
    def forgot_password(db: Session, email: str):
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Generate and send OTP
        otp_code = generate_otp()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=settings.OTP_EXPIRE_MINUTES)
        
        otp = OTP(
            email=email,
            otp_code=otp_code,
            purpose="reset_password",
            expires_at=expires_at
        )
        db.add(otp)
        db.commit()
        
        # Send OTP email
        send_otp_email(email, otp_code, "reset_password")
        
        return True
    
    @staticmethod
    def reset_password(db: Session, email: str, otp_code: str, new_password: str):
        # Verify OTP
        AuthService.verify_otp(db, email, otp_code, "reset_password")
        
        # Update password
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user.hashed_password = hash_password(new_password)
        db.commit()
        
        return True