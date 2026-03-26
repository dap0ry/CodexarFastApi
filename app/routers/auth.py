from datetime import timedelta

from fastapi import APIRouter, HTTPException, status

import app.core.database as database
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import UserRegister, UserLogin, Token

router = APIRouter()


@router.post("/api/auth/register", response_model=Token)
async def register_user(user: UserRegister):
    existing_user = await database.db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: El email ya está registrado."
        )

    hashed_password = get_password_hash(user.password)
    from datetime import datetime
    user_dict = {
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_onboarded": False,
        "elo": 0,
        "win_streak": 0
    }

    await database.db.users.insert_one(user_dict)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer", "username": None, "is_onboarded": False}


@router.post("/api/auth/login", response_model=Token)
async def login_user(user: UserLogin):
    db_user = await database.db.users.find_one({"email": user.email})

    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["email"]}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": db_user.get("username"),
        "is_onboarded": db_user.get("is_onboarded", False)
    }
