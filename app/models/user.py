from typing import Optional, List
from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    username: Optional[str] = None
    is_onboarded: bool


class OnboardData(BaseModel):
    username: str
    languages: List[str]
    level: str
    description: str


class EmailVerifyRequest(BaseModel):
    email: EmailStr
    code: str


class ResendVerificationRequest(BaseModel):
    email: EmailStr
