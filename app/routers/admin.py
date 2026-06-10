from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import app.core.database as database
from app.core.roles import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])

VALID_ROLES = ("user", "moderator", "admin")


class SetRoleBody(BaseModel):
    role: str


def _clean_user(u: dict) -> dict:
    return {
        "id":         str(u["_id"]),
        "username":   u.get("username", "—"),
        "email":      u.get("email", ""),
        "role":       u.get("role", "user"),
        "is_banned":  u.get("is_banned", False),
        "elo":        u.get("elo", 0),
        "created_at": str(u.get("created_at", "")),
    }


@router.get("/users")
async def list_users(admin: dict = Depends(require_admin)):
    cursor = database.db.users.find(
        {"is_onboarded": True},
        {"password": 0}
    ).sort("elo", -1)
    users = await cursor.to_list(length=500)
    return [_clean_user(u) for u in users]


@router.post("/ban/{username}")
async def ban_user(username: str, admin: dict = Depends(require_admin)):
    if username == admin.get("username"):
        raise HTTPException(status_code=400, detail="No puedes banearte a ti mismo")
    result = await database.db.users.update_one(
        {"username": username},
        {"$set": {"is_banned": True}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": f"{username} baneado correctamente"}


@router.post("/unban/{username}")
async def unban_user(username: str, admin: dict = Depends(require_admin)):
    result = await database.db.users.update_one(
        {"username": username},
        {"$set": {"is_banned": False}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": f"{username} desbaneado correctamente"}


@router.post("/set-role/{username}")
async def set_role(username: str, body: SetRoleBody, admin: dict = Depends(require_admin)):
    if body.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail=f"Rol inválido. Valores posibles: {VALID_ROLES}")
    if username == admin.get("username") and body.role != "admin":
        raise HTTPException(status_code=400, detail="No puedes quitarte el rol de admin a ti mismo")
    result = await database.db.users.update_one(
        {"username": username},
        {"$set": {"role": body.role}}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": f"Rol de {username} cambiado a {body.role}"}


@router.delete("/news/{news_id}")
async def delete_news(news_id: str, admin: dict = Depends(require_admin)):
    try:
        oid = ObjectId(news_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de noticia inválido")
    result = await database.db.news.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return {"message": "Noticia eliminada"}


@router.delete("/exercises/{exercise_id}")
async def delete_exercise(exercise_id: str, admin: dict = Depends(require_admin)):
    try:
        oid = ObjectId(exercise_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de ejercicio inválido")
    result = await database.db.exercises.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    return {"message": "Ejercicio eliminado"}


_PROGRESS_RESET = {
    "elo": 0,
    "max_elo": 0,
    "wins": 0,
    "matches_played": 0,
    "win_streak": 0,
    "ranked_wins": 0,
    "solved_exercises": [],
    "bot_wins": 0,
    "bot_matches": 0,
    "bot_wins_by_diff": {},
    "bot_matches_by_diff": {},
    "coins": 0,
    "lang_stats": {},
    "survival_stats": {},
    "survival_games": 0,
    "equipped_achievements": [],
    "tournaments_joined": 0,
    "tournament_wins": 0,
    "tournament_match_wins": 0,
    "tournament_match_losses": 0,
}


@router.post("/reset-user/{username}")
async def reset_user_progress(username: str, admin: dict = Depends(require_admin)):
    result = await database.db.users.update_one(
        {"username": username},
        {"$set": _PROGRESS_RESET}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": f"Progreso de {username} restablecido"}


@router.post("/reset-all-users")
async def reset_all_users_progress(admin: dict = Depends(require_admin)):
    result = await database.db.users.update_many(
        {"is_onboarded": True},
        {"$set": _PROGRESS_RESET}
    )
    return {"message": f"Progreso restablecido para {result.modified_count} usuarios"}
