"""
tournaments.py — Codexar Tournaments system
Admin-created team tournaments. First team to solve all exercises wins.
"""

from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

import app.core.database as database
from app.core.security import get_current_user
from app.core.roles import require_admin

router = APIRouter()


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

class TournamentCreate(BaseModel):
    name: str
    description: str = ""
    prize: str = ""
    start_time: datetime
    exercise_ids: List[str]   # list of exercise _id strings


class TournamentProgressUpdate(BaseModel):
    exercise_id: str


# ── Routes ───────────────────────────────────────────────────────────────────

@router.post("/api/tournaments")
async def create_tournament(body: TournamentCreate, admin: dict = Depends(require_admin)):
    from bson import ObjectId

    # Validate exercise IDs
    valid_ids = []
    for eid in body.exercise_ids:
        try:
            oid = ObjectId(eid)
        except Exception:
            raise HTTPException(status_code=400, detail=f"ID de ejercicio inválido: {eid}")
        ex = await database.db.exercises.find_one({"_id": oid})
        if not ex:
            raise HTTPException(status_code=404, detail=f"Ejercicio no encontrado: {eid}")
        valid_ids.append(eid)

    doc = {
        "name":         body.name.strip(),
        "description":  body.description.strip(),
        "prize":        body.prize.strip(),
        "start_time":   body.start_time,
        "exercise_ids": valid_ids,
        "status":       "upcoming",   # upcoming | active | finished
        "created_by":   admin.get("username", ""),
        "created_at":   datetime.utcnow(),
        "participants": [],   # list of team_ids
        "progress":     {},   # { team_id: [solved_exercise_ids] }
        "winner_team":  None,
        "ended_at":     None,
    }
    result = await database.db.tournaments.insert_one(doc)
    return {"message": "Torneo creado.", "id": str(result.inserted_id)}


@router.get("/api/tournaments")
async def list_tournaments(email: str = Depends(get_current_user)):
    cursor = database.db.tournaments.find({}).sort("start_time", -1)
    docs = await cursor.to_list(length=50)
    result = []
    for doc in docs:
        doc = _oid(doc)
        doc.pop("progress", None)
        result.append(doc)
    return result


@router.get("/api/tournaments/active")
async def list_active_tournaments(email: str = Depends(get_current_user)):
    cursor = database.db.tournaments.find({"status": {"$in": ["upcoming", "active"]}}).sort("start_time", 1)
    docs = await cursor.to_list(length=20)
    result = []
    for doc in docs:
        doc = _oid(doc)
        doc.pop("progress", None)
        result.append(doc)
    return result


@router.get("/api/tournaments/{tournament_id}")
async def get_tournament(tournament_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    tournament = _oid(tournament)

    # Enrich participant teams
    teams_info = []
    for team_id in tournament.get("participants", []):
        try:
            t = await database.db.teams.find_one({"_id": ObjectId(team_id)})
        except Exception:
            continue
        if t:
            solved = tournament.get("progress", {}).get(team_id, [])
            teams_info.append({
                "id":       team_id,
                "name":     t.get("name"),
                "photo_url": t.get("photo_url"),
                "member_count": len(t.get("members", [])),
                "solved":   len(solved),
                "total":    len(tournament.get("exercise_ids", [])),
            })
    tournament["teams_info"] = teams_info
    return tournament


@router.post("/api/tournaments/{tournament_id}/register")
async def register_team(tournament_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")

    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    if tournament.get("status") == "finished":
        raise HTTPException(status_code=400, detail="El torneo ya ha terminado")

    # User must be in a team
    team = await database.db.teams.find_one({"members": username})
    if not team:
        raise HTTPException(status_code=400, detail="Debes pertenecer a un equipo para participar en torneos")
    if team.get("owner") != username:
        raise HTTPException(status_code=403, detail="Solo el capitán del equipo puede inscribir al equipo")

    team_id = str(team["_id"])
    if team_id in tournament.get("participants", []):
        raise HTTPException(status_code=400, detail="Tu equipo ya está inscrito en este torneo")

    await database.db.tournaments.update_one(
        {"_id": oid},
        {"$addToSet": {"participants": team_id}}
    )
    return {"message": "Equipo inscrito en el torneo."}


@router.post("/api/tournaments/{tournament_id}/submit-solve")
async def submit_tournament_solve(tournament_id: str, body: TournamentProgressUpdate, email: str = Depends(get_current_user)):
    """Mark an exercise as solved for a team in this tournament."""
    from bson import ObjectId
    user = await _get_user(email)
    username = user.get("username", "")

    try:
        t_oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de torneo inválido")

    tournament = await database.db.tournaments.find_one({"_id": t_oid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    if tournament.get("status") != "active":
        raise HTTPException(status_code=400, detail="El torneo no está activo")

    # Find user's team
    team = await database.db.teams.find_one({"members": username})
    if not team:
        raise HTTPException(status_code=400, detail="No perteneces a ningún equipo")
    team_id = str(team["_id"])
    if team_id not in tournament.get("participants", []):
        raise HTTPException(status_code=400, detail="Tu equipo no está inscrito en este torneo")

    # Verify exercise is in tournament
    if body.exercise_id not in tournament.get("exercise_ids", []):
        raise HTTPException(status_code=400, detail="Ese ejercicio no forma parte del torneo")

    # Add to team's solved list
    progress_key = f"progress.{team_id}"
    await database.db.tournaments.update_one(
        {"_id": t_oid},
        {"$addToSet": {progress_key: body.exercise_id}}
    )

    # Check if team solved all exercises
    tournament_fresh = await database.db.tournaments.find_one({"_id": t_oid})
    solved = tournament_fresh.get("progress", {}).get(team_id, [])
    total = tournament_fresh.get("exercise_ids", [])
    if set(total) <= set(solved):
        # This team won
        await database.db.tournaments.update_one(
            {"_id": t_oid},
            {"$set": {"status": "finished", "winner_team": team_id, "ended_at": datetime.utcnow()}}
        )
        return {"message": "¡Tu equipo ha ganado el torneo!", "won": True}

    return {"message": "Progreso registrado.", "won": False, "solved": len(solved), "total": len(total)}


@router.patch("/api/tournaments/{tournament_id}/status")
async def update_tournament_status(tournament_id: str, status: str, admin: dict = Depends(require_admin)):
    from bson import ObjectId
    if status not in ("upcoming", "active", "finished"):
        raise HTTPException(status_code=400, detail="Estado inválido")
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    result = await database.db.tournaments.update_one({"_id": oid}, {"$set": {"status": status}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return {"message": f"Estado del torneo actualizado a {status}."}


@router.delete("/api/tournaments/{tournament_id}")
async def delete_tournament(tournament_id: str, admin: dict = Depends(require_admin)):
    from bson import ObjectId
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    result = await database.db.tournaments.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return {"message": "Torneo eliminado."}
