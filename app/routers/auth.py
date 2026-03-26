import random
import string
from datetime import datetime, timedelta

import bcrypt
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

import app.core.database as database
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, JWT_SECRET, ALGORITHM
from app.core.security import get_password_hash, verify_password, create_access_token, get_current_user
from app.models.user import UserRegister, UserLogin, Token, EmailVerifyRequest, ResendVerificationRequest
from app.services.email_service import send_verification_email

router = APIRouter()
_bearer = HTTPBearer()

VERIFICATION_EXPIRE_MINUTES = 5


def _generate_code() -> str:
    return "".join(random.choices(string.digits, k=6))


def _hash_code(code: str) -> str:
    return bcrypt.hashpw(code.encode(), bcrypt.gensalt()).decode()


def _check_code(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


@router.post("/api/auth/register")
async def register_user(user: UserRegister):
    # Block if email already has a verified account
    existing_user = await database.db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: El email ya está registrado."
        )

    # Remove any previous pending verification for this email (allow retry)
    await database.db.email_verifications.delete_many({"email": user.email})

    hashed_password = get_password_hash(user.password)
    code = _generate_code()

    await database.db.email_verifications.insert_one({
        "email": user.email,
        "hashed_password": hashed_password,
        "code_hash": _hash_code(code),
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=VERIFICATION_EXPIRE_MINUTES),
    })

    sent = await send_verification_email(user.email, code)
    if not sent:
        await database.db.email_verifications.delete_many({"email": user.email})
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No se pudo enviar el email de verificación. Inténtalo de nuevo."
        )

    return {"message": "verification_sent", "email": user.email}


@router.post("/api/auth/verify-email", response_model=Token)
async def verify_email(body: EmailVerifyRequest):
    doc = await database.db.email_verifications.find_one({"email": body.email})

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay verificación pendiente para este email."
        )

    if datetime.utcnow() > doc["expires_at"]:
        await database.db.email_verifications.delete_many({"email": body.email})
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="El código ha expirado. Vuelve a registrarte para recibir uno nuevo."
        )

    if not _check_code(body.code, doc["code_hash"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Código incorrecto."
        )

    # Create the verified user
    user_dict = {
        "email": body.email,
        "password": doc["hashed_password"],
        "created_at": datetime.utcnow(),
        "is_onboarded": False,
        "elo": 0,
        "win_streak": 0,
    }
    await database.db.users.insert_one(user_dict)
    await database.db.email_verifications.delete_many({"email": body.email})

    access_token = create_access_token(
        data={"sub": body.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer", "username": None, "is_onboarded": False}


@router.post("/api/auth/resend-verification")
async def resend_verification(body: ResendVerificationRequest):
    doc = await database.db.email_verifications.find_one({"email": body.email})

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay verificación pendiente para este email."
        )

    code = _generate_code()
    await database.db.email_verifications.update_one(
        {"email": body.email},
        {"$set": {
            "code_hash": _hash_code(code),
            "expires_at": datetime.utcnow() + timedelta(minutes=VERIFICATION_EXPIRE_MINUTES),
        }}
    )

    sent = await send_verification_email(body.email, code)
    if not sent:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="No se pudo reenviar el email. Inténtalo de nuevo."
        )

    return {"message": "resent"}


@router.post("/api/auth/login", response_model=Token)
async def login_user(user: UserLogin):
    db_user = await database.db.users.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": db_user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.get("username"),
        "is_onboarded": db_user.get("is_onboarded", False),
    }


async def _revoke_token(credentials: HTTPAuthorizationCredentials):
    """Decode token and add its JTI to the revoked_tokens collection."""
    try:
        payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        exp = payload.get("exp")
        if jti:
            await database.db.revoked_tokens.insert_one({
                "jti": jti,
                "expires_at": datetime.utcfromtimestamp(exp),
            })
    except JWTError:
        pass  # Token already invalid — nothing to revoke


@router.post("/api/auth/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(_bearer)):
    await _revoke_token(credentials)
    return {"message": "Sesión cerrada correctamente"}


@router.post("/api/auth/refresh", response_model=Token)
async def refresh_token(
    email: str = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
):
    # Revoke old token
    await _revoke_token(credentials)

    # Issue new token
    db_user = await database.db.users.find_one({"email": email})
    new_token = create_access_token(
        data={"sub": email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {
        "access_token": new_token,
        "token_type": "bearer",
        "username": db_user.get("username") if db_user else None,
        "is_onboarded": db_user.get("is_onboarded", False) if db_user else False,
    }
