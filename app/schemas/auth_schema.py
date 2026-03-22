from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    email: EmailStr
    phone: str
    password: str

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class OTPVerifySchema(BaseModel):
    email: EmailStr
    password: str
    code: str

class ForgotPasswordSchema(BaseModel):
    email: EmailStr

class ResetPasswordSchema(BaseModel):
    email: EmailStr
    code: str
    new_password: str

class CreateAdminSchema(BaseModel):
    email: EmailStr
    phone: str
    password: str
