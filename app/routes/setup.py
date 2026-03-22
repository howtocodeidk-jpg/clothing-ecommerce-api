from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.user import User
from app.models.role import Role
from app.core.security import get_password_hash

router = APIRouter(prefix="/setup", tags=["Setup"])

SECRET_KEY = "DRAPE_SETUP_2025"  # change this to something only you know

class SuperAdminCreate(BaseModel):
    secret:   str
    email:    str
    password: str
    phone:    str

@router.post("/create-superadmin")
def create_super_admin(data: SuperAdminCreate, db: Session = Depends(get_db)):

    # Verify secret so random people can't use this
    if data.secret != SECRET_KEY:
        return {"error": "Invalid secret key"}

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        return {"error": "User already exists"}

    role = db.query(Role).filter(Role.name == "SuperAdmin").first()
    if not role:
        return {"error": "SuperAdmin role not found"}

    user = User(
        email         = data.email,
        phone         = data.phone,
        password_hash = get_password_hash(data.password),
        role_id       = role.id,
        is_verified   = True,
    )
    db.add(user)
    db.commit()

    return {"success": True, "message": "Super Admin created!"}