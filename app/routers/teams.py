"""
teams.py — Codexar Teams system
Teams: create, join, leave, manage members (max 10).
"""

import io
import logging
from datetime import datetime
from typing import Optional

import cloudinary.uploader
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, validator

import app.core.database as database
from app.core.security import get_current_user

logger = logging.getLogger(__name__)
_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}

router = APIRouter()

MAX_MEMBERS = 10
MAX_NAME_LEN = 20


# ── Helpers ──────────────────────────────────────────────────────────────────

async def _get_user(email: str) -> dict:
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


def _oid(doc: dict) -> dict:
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


# ── Schemas ───────────────────────────────────────────────────────────────────

class TeamCreate(BaseModel):
    name: str
    description: str = ""
    photo_url: Optional[str] = None

    @validator("name")
    def name_valid(cls, v):
        v = v.strip()
        if not v:
            raise ValueError("El nombre del equipo no puede estar vacío")
        if len(v) > MAX_NAME_LEN:
            raise ValueError(f"El nombre del equipo no puede tener más de {MAX_NAME_LEN} caracteres")
        return v


class TeamInvite(BaseModel):
    username: str


# ── Routes ───────────────────────────────────────────────────────────────────

@router.post("/api/teams/create")
async def create_team(body: TeamCreate, email: str = Depends(get_current_user)):
    user = await _get_user(email)
    username = user.get("username", "")

    # One team per user
    existing = await database.db.teams.find_one({"members": username})
    if existing:
        raise HTTPException(status_code=400, detail="Ya eres miembro de un equipo. Debes salir antes de crear uno nuevo.")

    # Name uniqueness
    name_taken = await database.db.teams.find_one({"name": body.name})
    if name_taken:
        raise HTTPException(status_code=409, detail="Ya existe un equipo con ese nombre.")

    doc = {
        "name":        body.name,
        "description": body.description.strip(),
        "photo_url":   body.photo_url,
        "owner":       username,
        "members":     [username],
        "invites":     [],   # pending invite usernames
        "created_at":  datetime.utcnow(),
    }
    result = await database.db.teams.insert_one(doc)
    return {"message": "Equipo creado.", "id": str(result.inserted_id)}


@router.get("/api/teams")
async def list_teams(email: str = Depends(get_current_user)):
    cursor = database.db.teams.find({}).sort("created_at", -1)
    docs = await cursor.to_list(length=100)
    result = []
    for doc in docs:
        doc = _oid(doc)
        doc.pop("invites", None)
        result.append(doc)
    return result


@router.get("/api/teams/leaderboard")
async def teams_leaderboard(email: str = Depends(get_current_user)):
    cursor = database.db.teams.find({}, {"name": 1, "photo_url": 1, "members": 1})
    teams = await cursor.to_list(length=None)
    result = []
    for team in teams:
        members = team.get("members", [])
        total_solved = 0
        if members:
            async for u in database.db.users.find(
                {"username": {"$in": members}}, {"solved_exercises": 1}
            ):
                total_solved += len(u.get("solved_exercises", []))
        result.append({
            "name":         team["name"],
            "photo_url":    team.get("photo_url"),
            "member_count": len(members),
            "total_solved": total_solved,
        })
    result.sort(key=lambda x: x["total_solved"], reverse=True)
    return result[:10]


@router.get("/api/teams/mine")
async def my_team(email: str = Depends(get_current_user)):
    user = await _get_user(email)
    username = user.get("username", "")
    team = await database.db.teams.find_one({"members": username})
    if not team:
        return None
    team = _oid(team)
    # Enrich members with online status and stats
    members_info = []
    for m in team.get("members", []):
        u = await database.db.users.find_one({"username": m})
        if u:
            members_info.append({
                "username": m,
                "elo":      u.get("elo", 0),
                "solved":   len(u.get("solved_exercises", [])),
                "avatar":   u.get("avatar"),
                "is_owner": m == team.get("owner"),
            })
    team["members_info"] = members_info
    team["total_solved"] = sum(m["solved"] for m in members_info)
    if members_info:
        team["avg_elo"]    = round(sum(m["elo"] for m in members_info) / len(members_info))
        team["avg_solved"] = round(sum(m["solved"] for m in members_info) / len(members_info))
    else:
        team["avg_elo"]    = 0
        team["avg_solved"] = 0
    return team


@router.get("/api/teams/public/{team_name}")
async def get_team_public(team_name: str):
    team = await database.db.teams.find_one({"name": team_name})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    team = _oid(team)
    team.pop("invites", None)

    members_info = []
    for m in team.get("members", []):
        u = await database.db.users.find_one({"username": m})
        if u:
            members_info.append({
                "username": m,
                "elo":      u.get("elo", 0),
                "solved":   len(u.get("solved_exercises", [])),
                "avatar":   u.get("avatar"),
                "is_owner": m == team.get("owner"),
            })

    members_info.sort(key=lambda x: x["elo"], reverse=True)
    team["members_info"]  = members_info
    team["member_count"]  = len(members_info)
    team["total_solved"]  = sum(m["solved"] for m in members_info)
    team["highest_elo"]   = members_info[0]["elo"] if members_info else 0
    team["background_url"] = team.get("background_url")
    if members_info:
        team["avg_elo"] = round(sum(m["elo"] for m in members_info) / len(members_info))
    else:
        team["avg_elo"] = 0
    return team


@router.get("/api/teams/{team_id}")
async def get_team(team_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    team = _oid(team)
    # Enrich members
    members_info = []
    for m in team.get("members", []):
        u = await database.db.users.find_one({"username": m})
        if u:
            members_info.append({
                "username": m,
                "elo":      u.get("elo", 0),
                "solved":   len(u.get("solved_exercises", [])),
                "avatar":   u.get("avatar"),
                "is_owner": m == team.get("owner"),
            })
    team["members_info"] = members_info
    team.pop("invites", None)
    if members_info:
        team["avg_elo"] = round(sum(m["elo"] for m in members_info) / len(members_info))
        team["avg_solved"] = round(sum(m["solved"] for m in members_info) / len(members_info))
    return team


@router.post("/api/teams/{team_id}/invite")
async def invite_to_team(team_id: str, body: TeamInvite, email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if team.get("owner") != username:
        raise HTTPException(status_code=403, detail="Solo el dueño puede invitar miembros")
    if len(team.get("members", [])) >= MAX_MEMBERS:
        raise HTTPException(status_code=400, detail=f"El equipo ya tiene {MAX_MEMBERS} miembros (máximo)")

    target = await database.db.users.find_one({"username": body.username})
    if not target:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if body.username in team.get("members", []):
        raise HTTPException(status_code=400, detail="El usuario ya es miembro del equipo")
    if body.username in team.get("invites", []):
        raise HTTPException(status_code=400, detail="Ya se envió una invitación a ese usuario")

    # Check target isn't already in another team
    other_team = await database.db.teams.find_one({"members": body.username})
    if other_team:
        raise HTTPException(status_code=400, detail="Ese usuario ya pertenece a otro equipo")

    await database.db.teams.update_one({"_id": oid}, {"$addToSet": {"invites": body.username}})
    return {"message": f"Invitación enviada a {body.username}"}


@router.get("/api/teams/invites/mine")
async def my_invites(email: str = Depends(get_current_user)):
    user = await _get_user(email)
    username = user.get("username", "")
    cursor = database.db.teams.find({"invites": username})
    docs = await cursor.to_list(length=20)
    result = []
    for doc in docs:
        result.append({
            "id":          str(doc["_id"]),
            "name":        doc.get("name"),
            "description": doc.get("description"),
            "photo_url":   doc.get("photo_url"),
            "owner":       doc.get("owner"),
            "member_count": len(doc.get("members", [])),
        })
    return result


@router.post("/api/teams/{team_id}/accept")
async def accept_invite(team_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if username not in team.get("invites", []):
        raise HTTPException(status_code=403, detail="No tienes invitación para este equipo")
    if len(team.get("members", [])) >= MAX_MEMBERS:
        raise HTTPException(status_code=400, detail="El equipo está lleno")

    # Check not in another team
    other = await database.db.teams.find_one({"members": username})
    if other:
        raise HTTPException(status_code=400, detail="Ya perteneces a otro equipo")

    await database.db.teams.update_one(
        {"_id": oid},
        {"$addToSet": {"members": username}, "$pull": {"invites": username}}
    )
    return {"message": "Te has unido al equipo."}


@router.post("/api/teams/{team_id}/decline")
async def decline_invite(team_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    await database.db.teams.update_one({"_id": ObjectId(team_id)}, {"$pull": {"invites": username}})
    return {"message": "Invitación rechazada."}


@router.post("/api/teams/{team_id}/join")
async def join_team(team_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if username in team.get("members", []):
        raise HTTPException(status_code=400, detail="Ya eres miembro de este equipo")
    if len(team.get("members", [])) >= MAX_MEMBERS:
        raise HTTPException(status_code=400, detail=f"El equipo está lleno ({MAX_MEMBERS} miembros máximo)")
    other = await database.db.teams.find_one({"members": username})
    if other:
        raise HTTPException(status_code=400, detail="Ya perteneces a otro equipo. Sal primero antes de unirte.")
    await database.db.teams.update_one({"_id": oid}, {"$addToSet": {"members": username}})
    return {"message": f"Te has unido al equipo {team.get('name')}."}


@router.post("/api/teams/{team_id}/leave")
async def leave_team(team_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if username not in team.get("members", []):
        raise HTTPException(status_code=400, detail="No eres miembro de este equipo")
    if team.get("owner") == username:
        # Owner leaves → dissolve team
        await database.db.teams.delete_one({"_id": oid})
        return {"message": "Equipo disuelto (el dueño lo abandonó)."}
    await database.db.teams.update_one({"_id": oid}, {"$pull": {"members": username}})
    return {"message": "Has salido del equipo."}


@router.delete("/api/teams/{team_id}")
async def delete_team(team_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    from app.core.roles import require_admin
    user = await _get_user(email)
    username = user.get("username", "")
    role = user.get("role", "user")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if team.get("owner") != username and role != "admin":
        raise HTTPException(status_code=403, detail="Solo el dueño o un admin puede disolver el equipo")
    await database.db.teams.delete_one({"_id": oid})
    return {"message": "Equipo disuelto."}


@router.patch("/api/teams/{team_id}")
async def update_team(team_id: str, body: TeamCreate, email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if team.get("owner") != username:
        raise HTTPException(status_code=403, detail="Solo el dueño puede editar el equipo")

    # Name uniqueness check
    if body.name != team.get("name"):
        name_taken = await database.db.teams.find_one({"name": body.name, "_id": {"$ne": oid}})
        if name_taken:
            raise HTTPException(status_code=409, detail="Ya existe un equipo con ese nombre.")

    await database.db.teams.update_one({"_id": oid}, {"$set": {
        "name":        body.name,
        "description": body.description.strip(),
        "photo_url":   body.photo_url,
    }})
    return {"message": "Equipo actualizado."}


@router.post("/api/teams/{team_id}/upload-photo")
async def upload_team_photo(team_id: str, photo: UploadFile = File(...), email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if team.get("owner") != username:
        raise HTTPException(status_code=403, detail="Solo el capitán puede cambiar la foto")
    if photo.content_type not in _ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG, PNG, WEBP o GIF.")
    contents = await photo.read()
    if len(contents) > 2 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="La foto no puede superar los 2 MB.")
    photo.file = io.BytesIO(contents)
    try:
        result = cloudinary.uploader.upload(
            photo.file,
            folder="Codexar/TeamPhotos",
            public_id=f"team_{team_id}_photo",
            overwrite=True,
            resource_type="auto"
        )
        url = result.get("secure_url")
        await database.db.teams.update_one({"_id": oid}, {"$set": {"photo_url": url}})
        return {"status": "success", "url": url}
    except Exception as e:
        logger.warning("Team photo upload error: %s", str(e))
        raise HTTPException(status_code=500, detail="Error subiendo la foto del equipo")


@router.post("/api/teams/{team_id}/upload-banner")
async def upload_team_banner(team_id: str, banner: UploadFile = File(...), email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if team.get("owner") != username:
        raise HTTPException(status_code=403, detail="Solo el capitán puede cambiar el banner")
    if banner.content_type not in _ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG, PNG, WEBP o GIF.")
    contents = await banner.read()
    if len(contents) > 3 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="El banner no puede superar los 3 MB.")
    banner.file = io.BytesIO(contents)
    try:
        result = cloudinary.uploader.upload(
            banner.file,
            folder="Codexar/TeamBanners",
            public_id=f"team_{team_id}_banner",
            overwrite=True,
            resource_type="auto"
        )
        url = result.get("secure_url")
        await database.db.teams.update_one({"_id": oid}, {"$set": {"banner_url": url}})
        return {"status": "success", "url": url}
    except Exception as e:
        logger.warning("Team banner upload error: %s", str(e))
        raise HTTPException(status_code=500, detail="Error subiendo el banner del equipo")


@router.post("/api/teams/{team_id}/upload-background")
async def upload_team_background(team_id: str, bg: UploadFile = File(...), email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if team.get("owner") != username:
        raise HTTPException(status_code=403, detail="Solo el capitán puede cambiar el fondo")
    if bg.content_type not in _ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG, PNG, WEBP o GIF.")
    contents = await bg.read()
    if len(contents) > 3 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="El fondo no puede superar los 3 MB.")
    bg.file = io.BytesIO(contents)
    try:
        result = cloudinary.uploader.upload(
            bg.file,
            folder="Codexar/TeamBackgrounds",
            public_id=f"team_{team_id}_bg",
            overwrite=True,
            resource_type="auto"
        )
        url = result.get("secure_url")
        await database.db.teams.update_one({"_id": oid}, {"$set": {"background_url": url}})
        return {"status": "success", "url": url}
    except Exception as e:
        logger.warning("Team bg upload error: %s", str(e))
        raise HTTPException(status_code=500, detail="Error subiendo el fondo del equipo")


@router.delete("/api/teams/{team_id}/images/{field}")
async def clear_team_image(team_id: str, field: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    field_map = {"photo": "photo_url", "banner": "banner_url", "background": "background_url"}
    if field not in field_map:
        raise HTTPException(status_code=400, detail="Campo inválido. Usa: photo, banner o background")
    user = await _get_user(email)
    username = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if team.get("owner") != username:
        raise HTTPException(status_code=403, detail="Solo el capitán puede modificar las imágenes")
    await database.db.teams.update_one({"_id": oid}, {"$unset": {field_map[field]: ""}})
    return {"message": "Imagen eliminada."}


@router.delete("/api/teams/{team_id}/members/{username}")
async def kick_member(team_id: str, username: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    requester = user.get("username", "")
    try:
        oid = ObjectId(team_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    team = await database.db.teams.find_one({"_id": oid})
    if not team:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    if team.get("owner") != requester:
        raise HTTPException(status_code=403, detail="Solo el dueño puede expulsar miembros")
    if username == requester:
        raise HTTPException(status_code=400, detail="No puedes expulsarte a ti mismo")
    if username not in team.get("members", []):
        raise HTTPException(status_code=400, detail="El usuario no es miembro del equipo")
    await database.db.teams.update_one({"_id": oid}, {"$pull": {"members": username}})
    return {"message": f"{username} ha sido expulsado del equipo."}
