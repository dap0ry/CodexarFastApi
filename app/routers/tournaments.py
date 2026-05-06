"""
tournaments.py — Codexar Tournaments · 1v1 bracket system
Admin-created tournaments with auto-generated brackets, byes, and 2-minute match timers.
"""

import asyncio
import math
import random
import uuid
from datetime import datetime
from typing import Optional

import cloudinary.uploader
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form

import app.core.database as database
from app.core.security import get_current_user
from app.core.roles import require_admin

router = APIRouter()

# In-memory slot states: "tournament_id:slot_id" → slot_state dict
tournament_slots: dict = {}

TBD = "__TBD__"
BYE = "__BYE__"


# ── Bracket generation ────────────────────────────────────────────────────────

def _compute_layers(shuffled: list) -> list:
    """Pre-compute which player/result reaches each round entry."""
    layer0 = [BYE if p is None else p for p in shuffled]
    layers = [layer0]
    for _ in range(int(math.log2(len(shuffled)))):
        prev = layers[-1]
        curr = []
        for i in range(0, len(prev), 2):
            a, b = prev[i], prev[i + 1]
            a_bye = a in (None, BYE)
            b_bye = b in (None, BYE)
            if a_bye and b_bye:
                curr.append(BYE)
            elif a_bye:
                curr.append(b)
            elif b_bye:
                curr.append(a)
            else:
                curr.append(TBD)
        layers.append(curr)
    return layers


def _generate_bracket(participants: list) -> list:
    n = len(participants)
    if n < 2:
        raise ValueError("Se necesitan al menos 2 participantes")

    p = 1
    while p < n:
        p *= 2

    shuffled = list(participants)
    random.shuffle(shuffled)
    while len(shuffled) < p:
        shuffled.append(None)

    num_rounds = int(math.log2(p))
    layers = _compute_layers(shuffled)

    rounds = []
    for r in range(num_rounds):
        prev_layer = layers[r]
        next_layer = layers[r + 1]
        round_matches = []
        for m in range(len(next_layer)):
            a_raw = prev_layer[2 * m]
            b_raw = prev_layer[2 * m + 1]

            p1 = None if a_raw in (TBD, BYE) else a_raw
            p2 = None if b_raw in (TBD, BYE) else b_raw

            if a_raw == BYE and b_raw == BYE:
                status, winner = "skip", None
            elif a_raw == BYE:
                status, winner = "bye", p2
            elif b_raw == BYE:
                status, winner = "bye", p1
            elif a_raw == TBD or b_raw == TBD:
                status, winner = "pending", None
            else:
                status, winner = "ready", None

            round_matches.append({
                "id": f"r{r}m{m}",
                "p1_email": p1,
                "p2_email": p2,
                "winner_email": winner,
                "match_id": None,
                "status": status,
                "ready_at": None,
            })
        rounds.append(round_matches)

    return rounds


# ── Bracket advancement ───────────────────────────────────────────────────────

async def advance_bracket(tournament_id: str, slot_id: str, winner_email: str):
    """Called when a tournament match finishes. Advances bracket state."""
    from bson import ObjectId
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        return

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        return

    bracket = tournament.get("bracket", [])
    num_rounds = len(bracket)

    # Locate the slot
    target_r = target_m = None
    for r, round_matches in enumerate(bracket):
        for m, match in enumerate(round_matches):
            if match["id"] == slot_id:
                target_r, target_m = r, m
                break
        if target_r is not None:
            break

    if target_r is None:
        return

    bracket[target_r][target_m]["winner_email"] = winner_email
    bracket[target_r][target_m]["status"] = "done"
    bracket[target_r][target_m]["match_id"] = None

    next_r = target_r + 1

    if next_r >= num_rounds:
        # Champion!
        await database.db.tournaments.update_one(
            {"_id": oid},
            {"$set": {
                "bracket": bracket,
                "status": "finished",
                "winner_email": winner_email,
                "ended_at": datetime.utcnow(),
            }}
        )
        await database.db.users.update_one(
            {"email": winner_email},
            {"$inc": {"tournament_wins": 1}}
        )
        return

    next_m = target_m // 2
    next_match = bracket[next_r][next_m]

    if target_m % 2 == 0:
        next_match["p1_email"] = winner_email
    else:
        next_match["p2_email"] = winner_email

    p1 = next_match["p1_email"]
    p2 = next_match["p2_email"]

    if p1 is not None and p2 is not None:
        next_match["status"] = "ready"
        now = datetime.utcnow()
        next_match["ready_at"] = now.isoformat()

        slot_key = f"{tournament_id}:{next_match['id']}"
        tournament_slots[slot_key] = {
            "p1_email": p1,
            "p2_email": p2,
            "p1_ready": False,
            "p2_ready": False,
            "match_id": None,
            "ready_at": now,
            "event": asyncio.Event(),
        }
        asyncio.create_task(_slot_timeout(tournament_id, next_match["id"]))

    await database.db.tournaments.update_one(
        {"_id": oid},
        {"$set": {"bracket": bracket}}
    )


async def _slot_timeout(tournament_id: str, slot_id: str, delay: float = 120.0):
    """After 2 minutes, forfeit players who haven't joined their match."""
    await asyncio.sleep(delay)
    slot_key = f"{tournament_id}:{slot_id}"
    slot = tournament_slots.get(slot_key)
    if not slot or slot.get("match_id"):
        tournament_slots.pop(slot_key, None)
        return

    p1_ready = slot.get("p1_ready", False)
    p2_ready = slot.get("p2_ready", False)

    if p1_ready and not p2_ready:
        winner = slot["p1_email"]
    elif p2_ready and not p1_ready:
        winner = slot["p2_email"]
    else:
        winner = slot["p1_email"]

    tournament_slots.pop(slot_key, None)

    from bson import ObjectId
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        return

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        return
    bracket = tournament.get("bracket", [])
    for r_list in bracket:
        for match in r_list:
            if match["id"] == slot_id and match["status"] in ("ready", "ongoing"):
                match["status"] = "forfeit"
                match["winner_email"] = winner
                await database.db.tournaments.update_one(
                    {"_id": oid}, {"$set": {"bracket": bracket}}
                )
                await advance_bracket(tournament_id, slot_id, winner)
                return


# ── Helpers ───────────────────────────────────────────────────────────────────

def _oid(doc: dict) -> dict:
    doc["id"] = str(doc["_id"])
    del doc["_id"]
    return doc


async def _enrich_bracket(bracket: list) -> list:
    emails = set()
    for round_matches in bracket:
        for match in round_matches:
            for key in ("p1_email", "p2_email", "winner_email"):
                e = match.get(key)
                if e:
                    emails.add(e)

    user_map = {}
    if emails:
        async for user in database.db.users.find(
            {"email": {"$in": list(emails)}},
            {"email": 1, "username": 1, "avatar": 1}
        ):
            user_map[user["email"]] = {
                "email": user["email"],
                "username": user.get("username", user["email"]),
                "avatar": user.get("avatar"),
            }

    def _info(email):
        if not email:
            return None
        return user_map.get(email, {"email": email, "username": email, "avatar": None})

    enriched = []
    for round_matches in bracket:
        enriched_round = []
        for match in round_matches:
            m = dict(match)
            m["p1"] = _info(match.get("p1_email"))
            m["p2"] = _info(match.get("p2_email"))
            m["winner"] = _info(match.get("winner_email"))
            enriched_round.append(m)
        enriched.append(enriched_round)
    return enriched


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/api/tournaments")
async def create_tournament(
    name: str = Form(...),
    description: str = Form(""),
    start_time: str = Form(...),
    banner: Optional[UploadFile] = File(None),
    admin: dict = Depends(require_admin),
):
    banner_url = None
    if banner and banner.filename:
        contents = await banner.read()
        if len(contents) > 5 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="El banner no puede superar 5 MB")
        import io
        result = cloudinary.uploader.upload(
            io.BytesIO(contents),
            folder="codexar/tournament_banners",
            resource_type="image",
        )
        banner_url = result.get("secure_url")

    try:
        start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido (usa ISO 8601)")

    doc = {
        "name": name.strip(),
        "description": description.strip(),
        "banner_url": banner_url,
        "created_by": admin["email"],
        "created_by_username": admin.get("username", ""),
        "status": "upcoming",
        "created_at": datetime.utcnow(),
        "start_time": start_dt,
        "participants": [],
        "bracket": [],
        "winner_email": None,
        "ended_at": None,
    }
    result = await database.db.tournaments.insert_one(doc)
    return {"message": "Torneo creado.", "id": str(result.inserted_id)}


@router.get("/api/tournaments")
async def list_tournaments(email: str = Depends(get_current_user)):
    cursor = database.db.tournaments.find({}).sort("created_at", -1)
    docs = await cursor.to_list(length=50)
    result = []
    for doc in docs:
        doc = _oid(doc)
        doc.pop("bracket", None)
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

    bracket = tournament.get("bracket", [])
    if bracket:
        tournament["bracket"] = await _enrich_bracket(bracket)

    # Enrich participants
    participants_info = []
    for pe in tournament.get("participants", []):
        u = await database.db.users.find_one({"email": pe}, {"email": 1, "username": 1, "avatar": 1})
        if u:
            participants_info.append({
                "email": pe,
                "username": u.get("username", pe),
                "avatar": u.get("avatar"),
            })
    tournament["participants_info"] = participants_info

    # Enrich winner
    we = tournament.get("winner_email")
    if we:
        wu = await database.db.users.find_one({"email": we}, {"email": 1, "username": 1, "avatar": 1})
        if wu:
            tournament["winner"] = {
                "email": we,
                "username": wu.get("username", we),
                "avatar": wu.get("avatar"),
            }

    # In-memory slot readiness states
    slot_states = {}
    for key, state in tournament_slots.items():
        if key.startswith(f"{tournament_id}:"):
            sid = key[len(tournament_id) + 1:]
            ready_at = state.get("ready_at")
            slot_states[sid] = {
                "p1_ready": state["p1_ready"],
                "p2_ready": state["p2_ready"],
                "match_id": state.get("match_id"),
                "ready_at": ready_at.isoformat() if isinstance(ready_at, datetime) else ready_at,
            }
    tournament["slot_states"] = slot_states

    return tournament


@router.post("/api/tournaments/{tournament_id}/join")
async def join_tournament(tournament_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    if tournament.get("status") != "upcoming":
        raise HTTPException(status_code=400, detail="El torneo ya ha comenzado o ha terminado")
    if email in tournament.get("participants", []):
        raise HTTPException(status_code=400, detail="Ya estás inscrito en este torneo")

    await database.db.tournaments.update_one({"_id": oid}, {"$addToSet": {"participants": email}})
    return {"message": "Inscrito en el torneo."}


@router.post("/api/tournaments/{tournament_id}/leave")
async def leave_tournament(tournament_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    if tournament.get("status") != "upcoming":
        raise HTTPException(status_code=400, detail="No puedes abandonar un torneo ya iniciado")
    if email not in tournament.get("participants", []):
        raise HTTPException(status_code=400, detail="No estás inscrito")

    await database.db.tournaments.update_one({"_id": oid}, {"$pull": {"participants": email}})
    return {"message": "Has abandonado el torneo."}


@router.post("/api/tournaments/{tournament_id}/start")
async def start_tournament(tournament_id: str, admin: dict = Depends(require_admin)):
    from bson import ObjectId
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    if tournament.get("status") != "upcoming":
        raise HTTPException(status_code=400, detail="El torneo ya está activo o ha terminado")

    participants = tournament.get("participants", [])
    if len(participants) < 2:
        raise HTTPException(status_code=400, detail="Se necesitan al menos 2 participantes para iniciar")

    bracket = _generate_bracket(participants)
    now = datetime.utcnow()

    # Initialize in-memory slots for all "ready" matches
    for round_matches in bracket:
        for match in round_matches:
            if match["status"] == "ready":
                slot_key = f"{tournament_id}:{match['id']}"
                tournament_slots[slot_key] = {
                    "p1_email": match["p1_email"],
                    "p2_email": match["p2_email"],
                    "p1_ready": False,
                    "p2_ready": False,
                    "match_id": None,
                    "ready_at": now,
                    "event": asyncio.Event(),
                }
                match["ready_at"] = now.isoformat()
                asyncio.create_task(_slot_timeout(tournament_id, match["id"]))

    await database.db.users.update_many(
        {"email": {"$in": participants}},
        {"$inc": {"tournaments_joined": 1}}
    )

    await database.db.tournaments.update_one(
        {"_id": oid},
        {"$set": {"status": "active", "bracket": bracket, "started_at": now}}
    )
    return {"message": "Torneo iniciado.", "participants": len(participants)}


@router.post("/api/tournaments/{tournament_id}/match/{slot_id}/join")
async def join_match_slot(
    tournament_id: str,
    slot_id: str,
    email: str = Depends(get_current_user),
):
    from bson import ObjectId
    from app.routers.matchmaking import active_matches, _pick_exercise, _build_player_data

    slot_key = f"{tournament_id}:{slot_id}"
    slot = tournament_slots.get(slot_key)

    if not slot:
        try:
            oid = ObjectId(tournament_id)
        except Exception:
            raise HTTPException(status_code=400, detail="ID inválido")
        tournament = await database.db.tournaments.find_one({"_id": oid})
        if not tournament:
            raise HTTPException(status_code=404, detail="Torneo no encontrado")
        for r_list in tournament.get("bracket", []):
            for m in r_list:
                if m["id"] == slot_id:
                    if m.get("match_id"):
                        return {"status": "started", "match_id": m["match_id"]}
                    raise HTTPException(status_code=400, detail="El tiempo para unirse ha expirado")
        raise HTTPException(status_code=404, detail="Slot no encontrado")

    if slot.get("match_id"):
        return {"status": "started", "match_id": slot["match_id"]}

    is_p1 = email == slot["p1_email"]
    is_p2 = email == slot["p2_email"]
    if not is_p1 and not is_p2:
        raise HTTPException(status_code=403, detail="No eres participante de esta partida")

    ready_at = slot.get("ready_at")
    if ready_at and (datetime.utcnow() - ready_at).total_seconds() > 125:
        raise HTTPException(status_code=400, detail="El tiempo para unirse ha expirado")

    if is_p1:
        slot["p1_ready"] = True
    else:
        slot["p2_ready"] = True

    if slot["p1_ready"] and slot["p2_ready"]:
        p1_user = await database.db.users.find_one({"email": slot["p1_email"]})
        p2_user = await database.db.users.find_one({"email": slot["p2_email"]})
        if not p1_user or not p2_user:
            raise HTTPException(status_code=500, detail="Error al crear la partida")

        p1_data = await _build_player_data(slot["p1_email"], p1_user)
        p2_data = await _build_player_data(slot["p2_email"], p2_user)
        chosen_ex = await _pick_exercise()

        match_id = str(uuid.uuid4())
        active_matches[match_id] = {
            "player1": p1_data,
            "player2": p2_data,
            "p1_progress": 0,
            "p2_progress": 0,
            "exercise": chosen_ex,
            "status": "ongoing",
            "winner": None,
            "match_type": "tournament",
            "tournament_id": tournament_id,
            "slot_id": slot_id,
            "event": asyncio.Event(),
        }

        slot["match_id"] = match_id
        slot["event"].set()

        # Update bracket in DB
        try:
            oid = ObjectId(tournament_id)
            tournament = await database.db.tournaments.find_one({"_id": oid})
            if tournament:
                bracket = tournament.get("bracket", [])
                for r_list in bracket:
                    for m in r_list:
                        if m["id"] == slot_id:
                            m["status"] = "ongoing"
                            m["match_id"] = match_id
                            break
                await database.db.tournaments.update_one(
                    {"_id": oid}, {"$set": {"bracket": bracket}}
                )
        except Exception:
            pass

        return {"status": "started", "match_id": match_id}

    return {"status": "waiting"}


@router.get("/api/tournaments/{tournament_id}/match/{slot_id}/poll")
async def poll_match_slot(
    tournament_id: str,
    slot_id: str,
    email: str = Depends(get_current_user),
):
    slot_key = f"{tournament_id}:{slot_id}"
    slot = tournament_slots.get(slot_key)

    if not slot:
        raise HTTPException(status_code=404, detail="Slot no disponible o expirado")

    if not (email == slot["p1_email"] or email == slot["p2_email"]):
        raise HTTPException(status_code=403, detail="No eres participante de esta partida")

    if slot.get("match_id"):
        return {"status": "started", "match_id": slot["match_id"]}

    try:
        await asyncio.wait_for(slot["event"].wait(), timeout=20.0)
        return {"status": "started", "match_id": slot.get("match_id")}
    except asyncio.TimeoutError:
        return {"status": "waiting"}


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
    for k in [k for k in tournament_slots if k.startswith(f"{tournament_id}:")]:
        tournament_slots.pop(k, None)
    return {"message": "Torneo eliminado."}
