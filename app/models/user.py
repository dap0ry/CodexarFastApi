import re
from typing import Optional, List
from pydantic import BaseModel, field_validator

_EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


class UserRegister(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def email_format(cls, v: str) -> str:
        v = v.strip().lower()
        if not _EMAIL_RE.match(v):
            raise ValueError("Email inválido")
        return v

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if len(v) > 128:
            raise ValueError("La contraseña no puede superar los 128 caracteres")
        return v


class UserLogin(BaseModel):
    email: str
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
    email: str
    code: str


class ResendVerificationRequest(BaseModel):
    email: str
