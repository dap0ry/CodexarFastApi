"""Role-checking FastAPI dependencies."""
from fastapi import HTTPException, Depends
import app.core.database as database
from app.core.security import get_current_user


async def _get_user(email: str) -> dict:
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


async def require_moderator(email: str = Depends(get_current_user)) -> dict:
    user = await _get_user(email)
    if user.get("role") not in ("moderator", "admin"):
        raise HTTPException(status_code=403, detail="Se requiere rol de moderador o superior")
    return user


async def require_admin(email: str = Depends(get_current_user)) -> dict:
    user = await _get_user(email)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
    return user
