from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database import SessionLocal
from app.schemas.auth_schema import *
from app.services.auth_service import *
from app.utils.response import success_response
from app.utils.dependencies import require_role
from app.utils.dependencies import require_role
from app.core.security import get_current_user


router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register")
def register(data: RegisterSchema, db: Session = Depends(get_db)):
    register_user(db, data.email, data.phone, data.password)
    return success_response("OTP sent successfully")


@router.post("/verify-otp")
def verify(data: OTPVerifySchema, db: Session = Depends(get_db)):
    verify_user_otp(db, data.email, data.code, data.password)
    return success_response("Account verified successfully")


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):
    tokens = login_user(db, data.email, data.password)
    return success_response("Login successful", tokens)


@router.post("/forgot-password")
def forgot(data: ForgotPasswordSchema, db: Session = Depends(get_db)):
    forgot_password(db, data.email)
    return success_response("OTP sent to email and WhatsApp")


@router.post("/reset-password")
def reset(data: ResetPasswordSchema, db: Session = Depends(get_db)):
    reset_password(db, data.email, data.code, data.new_password)
    return success_response("Password reset successful")

@router.post("/create-admin")
def create_admin(
    data: CreateAdminSchema,
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1])) 
):
    create_admin_user(db, data.email, data.phone, data.password)
    return success_response("Admin created successfully")

@router.delete("/delete-user/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    delete_user_by_id(db, user_id, current_user)
    return success_response("User deleted successfully")

@router.get("/users")
def list_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1, 2])) 
):
    users = get_all_users(db)

    return success_response(
        "Users fetched successfully",
        data=[
            {
                "id": user.id,
                "email": user.email,
                "role": user.role_id
            }
            for user in users
        ]
    )

@router.get("/admins")
def list_admins(
    db: Session = Depends(get_db),
    current_user = Depends(require_role([1]))
):
    admins = get_admins_and_superadmins(db)

    return success_response(
        "Admins and Super Admins fetched successfully",
        data=[
            {
                "id": admin.id,
                "email": admin.email,
                "role": admin.role_id
            }
            for admin in admins
        ]
    )
