from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

import app.core.database as database
from app.core.security import get_current_user

router = APIRouter()

ACHIEVEMENTS_CATALOG = [
    # Ejercicios resueltos
    {"key": "exercises_1",   "category": "exercises",   "title": "Iniciado",            "description": "Resuelve 1 ejercicio",              "threshold": 1,   "rarity": "common",    "icon": "💻"},
    {"key": "exercises_5",   "category": "exercises",   "title": "Aprendiz",            "description": "Resuelve 5 ejercicios",             "threshold": 5,   "rarity": "uncommon",  "icon": "💻"},
    {"key": "exercises_10",  "category": "exercises",   "title": "Desarrollador",       "description": "Resuelve 10 ejercicios",            "threshold": 10,  "rarity": "rare",      "icon": "💻"},
    {"key": "exercises_25",  "category": "exercises",   "title": "Experto en Código",   "description": "Resuelve 25 ejercicios",            "threshold": 25,  "rarity": "epic",      "icon": "💻"},
    {"key": "exercises_50",  "category": "exercises",   "title": "Maestro del Código",  "description": "Resuelve 50 ejercicios",            "threshold": 50,  "rarity": "legendary", "icon": "💻"},
    {"key": "exercises_100", "category": "exercises",   "title": "Leyenda del Código",  "description": "Resuelve 100 ejercicios",           "threshold": 100, "rarity": "ultimate",  "icon": "💻"},
    # Partidas ganadas
    {"key": "wins_1",        "category": "wins",        "title": "Primera Victoria",    "description": "Gana 1 partida",                    "threshold": 1,   "rarity": "common",    "icon": "⚔️"},
    {"key": "wins_5",        "category": "wins",        "title": "Combatiente",         "description": "Gana 5 partidas",                   "threshold": 5,   "rarity": "uncommon",  "icon": "⚔️"},
    {"key": "wins_10",       "category": "wins",        "title": "Veterano",            "description": "Gana 10 partidas",                  "threshold": 10,  "rarity": "rare",      "icon": "⚔️"},
    {"key": "wins_25",       "category": "wins",        "title": "Guerrero",            "description": "Gana 25 partidas",                  "threshold": 25,  "rarity": "epic",      "icon": "⚔️"},
    {"key": "wins_50",       "category": "wins",        "title": "Campeón",             "description": "Gana 50 partidas",                  "threshold": 50,  "rarity": "legendary", "icon": "⚔️"},
    {"key": "wins_100",      "category": "wins",        "title": "Leyenda de Batalla",  "description": "Gana 100 partidas",                 "threshold": 100, "rarity": "ultimate",  "icon": "⚔️"},
    # Clasificatorias ganadas
    {"key": "ranked_1",      "category": "ranked_wins", "title": "Clasificado",         "description": "Gana 1 partida clasificatoria",     "threshold": 1,   "rarity": "common",    "icon": "🏆"},
    {"key": "ranked_5",      "category": "ranked_wins", "title": "Competidor",          "description": "Gana 5 partidas clasificatorias",   "threshold": 5,   "rarity": "uncommon",  "icon": "🏆"},
    {"key": "ranked_10",     "category": "ranked_wins", "title": "Rival Peligroso",     "description": "Gana 10 partidas clasificatorias",  "threshold": 10,  "rarity": "rare",      "icon": "🏆"},
    {"key": "ranked_25",     "category": "ranked_wins", "title": "Élite Clasificada",   "description": "Gana 25 partidas clasificatorias",  "threshold": 25,  "rarity": "epic",      "icon": "🏆"},
    {"key": "ranked_50",     "category": "ranked_wins", "title": "Maestro Clasificado", "description": "Gana 50 partidas clasificatorias",  "threshold": 50,  "rarity": "legendary", "icon": "🏆"},
    {"key": "ranked_100",    "category": "ranked_wins", "title": "Predador del Ranking","description": "Gana 100 partidas clasificatorias", "threshold": 100, "rarity": "ultimate",  "icon": "🏆"},
]

_CATALOG_MAP = {a["key"]: a for a in ACHIEVEMENTS_CATALOG}


def _get_stat(user: dict, category: str) -> int:
    if category == "exercises":
        return len(user.get("solved_exercises", []))
    if category == "wins":
        return user.get("wins", 0)
    if category == "ranked_wins":
        return user.get("ranked_wins", 0)
    return 0


class EquipRequest(BaseModel):
    achievement_key: str
    replace_key: Optional[str] = None


@router.get("/api/achievements/")
async def get_achievements(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    equipped = user.get("equipped_achievements", [])
    result = []
    for ach in ACHIEVEMENTS_CATALOG:
        current = _get_stat(user, ach["category"])
        pct = min(100, int((current / ach["threshold"]) * 100))
        result.append({
            **ach,
            "current": current,
            "unlocked": current >= ach["threshold"],
            "equipped": ach["key"] in equipped,
            "progress_pct": pct,
        })
    return {"achievements": result, "equipped": equipped}


@router.get("/api/achievements/equipped")
async def get_equipped(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    equipped_keys = user.get("equipped_achievements", [])
    result = [_CATALOG_MAP[k] for k in equipped_keys if k in _CATALOG_MAP]
    return {"equipped": result}


@router.post("/api/achievements/equip")
async def equip_achievement(body: EquipRequest, email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    ach = _CATALOG_MAP.get(body.achievement_key)
    if not ach:
        raise HTTPException(status_code=404, detail="Logro no encontrado")

    if _get_stat(user, ach["category"]) < ach["threshold"]:
        raise HTTPException(status_code=400, detail="Logro no desbloqueado aún")

    equipped = list(user.get("equipped_achievements", []))

    if body.achievement_key in equipped:
        raise HTTPException(status_code=400, detail="Este logro ya está equipado")

    if len(equipped) >= 3:
        if not body.replace_key:
            raise HTTPException(
                status_code=409,
                detail="Ya tienes 3 logros equipados. Indica replace_key para reemplazar uno.",
            )
        if body.replace_key not in equipped:
            raise HTTPException(status_code=400, detail="El logro a reemplazar no está equipado")
        equipped.remove(body.replace_key)

    equipped.append(body.achievement_key)
    await database.db.users.update_one(
        {"email": email}, {"$set": {"equipped_achievements": equipped}}
    )
    return {"equipped": equipped}


@router.post("/api/achievements/unequip")
async def unequip_achievement(body: EquipRequest, email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    equipped = list(user.get("equipped_achievements", []))
    if body.achievement_key not in equipped:
        raise HTTPException(status_code=400, detail="Este logro no está equipado")

    equipped.remove(body.achievement_key)
    await database.db.users.update_one(
        {"email": email}, {"$set": {"equipped_achievements": equipped}}
    )
    return {"equipped": equipped}
