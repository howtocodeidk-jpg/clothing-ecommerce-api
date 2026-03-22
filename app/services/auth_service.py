from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import HTTPException

from app.models.user import User
from app.models.role import Role
from app.models.otp import OTP
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.core.otp import generate_otp, otp_expiry
from app.core.rate_limiter import check_rate_limit
from app.services.email_service import send_email
from app.services.whatsapp_service import send_whatsapp
from app.utils.validators import validate_password, validate_phone
from datetime import datetime, timedelta
from app.config import settings

# ---------------- REGISTER ----------------
def register_user(db: Session, email: str, phone: str, password: str):

    validate_password(password)
    validate_phone(phone)

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already registered")

    check_rate_limit(email)

    otp_code = generate_otp()

    otp = OTP(
    email=email,
    phone=phone,
    code=otp_code,
    expires_at=datetime.utcnow() + timedelta(
        minutes=settings.OTP_EXPIRE_MINUTES
    )
)

    db.add(otp)
    db.commit()

    email_body = f"Your OTP is {otp_code}. It expires in 5 minutes."
    send_email(email, "OTP Verification", email_body)
    send_whatsapp(phone, email_body)

    return True


# ---------------- VERIFY OTP ----------------
def verify_user_otp(db: Session, email: str, code: str, password: str):

    otp = db.query(OTP).filter(
    OTP.email == email,
    OTP.code == code
).first()


    if not otp:
        raise HTTPException(400, "OTP not found")

    if otp.expires_at < datetime.utcnow():
        raise HTTPException(400, "OTP expired")

    

    role = db.query(Role).filter(Role.name == "User").first()

    new_user = User(
        email=email,
        phone=otp.phone,
        password_hash=get_password_hash(password),
        role_id=role.id,
        is_verified=True
    )

    db.add(new_user)
    db.delete(otp)
    db.commit()

    return True


# ---------------- LOGIN ----------------
def login_user(db: Session, email: str, password: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(400, "Invalid credentials")

    if not verify_password(password, user.password_hash):
        raise HTTPException(400, "Invalid credentials")

    if not user.is_active:
        raise HTTPException(403, "Account is deactivated")

    access_token = create_access_token({
    "user_id": user.id,
    "role_id": user.role_id
})


    refresh_token = create_refresh_token({
    "user_id": user.id
})


    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": user.role.name
    }


# ---------------- FORGOT PASSWORD ----------------
def forgot_password(db: Session, email: str):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(404, "User not found")

    check_rate_limit(email)

    otp_code = generate_otp()

    otp = OTP(
        email=email,
        phone=user.phone,
        code=otp_code,
        expires_at=otp_expiry()
    )

    db.add(otp)
    db.commit()

    body = f"Your password reset OTP is {otp_code}"

    send_email(email, "Reset Password OTP", body)
    send_whatsapp(user.phone, body)

    return True


# ---------------- RESET PASSWORD ----------------
def reset_password(db: Session, email: str, code: str, new_password: str):

    validate_password(new_password)

    otp = (
        db.query(OTP)
        .filter(OTP.email == email)
        .order_by(OTP.id.desc())
        .first()
    )

    if not otp:
        raise HTTPException(400, "OTP not found")

    if otp.expires_at < datetime.utcnow():
        raise HTTPException(400, "OTP expired")

    if str(otp.code) != str(code):
        raise HTTPException(400, "Invalid OTP")

    user = db.query(User).filter(User.email == email).first()

    user.password_hash = get_password_hash(new_password)

    db.delete(otp)
    db.commit()

    return True

def create_admin_user(db, email: str, phone: str, password: str):

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    admin = User(
        email=email,
        phone=phone,
        password_hash=get_password_hash(password),
        role_id=2, 
        is_verified=True,
        is_active=True
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    return admin

def delete_user_by_id(db: Session, user_id: int, current_user):

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(404, "User not found")

    # Prevent deleting yourself (optional safety)
    if user.id == current_user.id:
        raise HTTPException(400, "You cannot delete yourself")

    # ---------------- ROLE RULES ----------------

    # Super Admin deleting Admin
    if current_user.role_id == 1 and user.role_id == 2:
        db.delete(user)
        db.commit()
        return True

    # Super Admin deleting User
    if current_user.role_id == 1 and user.role_id == 3:
        db.delete(user)
        db.commit()
        return True

    # Admin deleting User
    if current_user.role_id == 2 and user.role_id == 3:
        db.delete(user)
        db.commit()
        return True

    raise HTTPException(403, "You do not have permission to delete this user")

def get_all_users(db: Session):

    users = db.query(User).filter(User.role_id == 3).all()

    return users

def get_admins_and_superadmins(db: Session):

    admins = db.query(User).filter(User.role_id.in_([1, 2])).all()

    return admins
