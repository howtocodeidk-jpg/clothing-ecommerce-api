import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.core.security import get_password_hash


def create_super_admin():
    db = SessionLocal()

    email = input("Enter Super Admin Email: ")
    password = input("Enter Super Admin Password: ")
    phone = input("Enter Phone Number: ")

    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        print("❌ User with this email already exists.")
        return

    role = db.query(Role).filter(Role.name == "SuperAdmin").first()
    if not role:
        print("❌ SuperAdmin role not found. Insert roles first.")
        return

    super_admin = User(
        email=email,
        phone=phone,
        password_hash=get_password_hash(password),
        role_id=role.id,
        is_verified=True
    )

    db.add(super_admin)
    db.commit()
    db.refresh(super_admin)

    print("✅ Super Admin Created Successfully!")


if __name__ == "__main__":
    create_super_admin()
