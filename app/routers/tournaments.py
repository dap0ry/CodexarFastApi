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
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form, WebSocket, WebSocketDisconnect, Query

import app.core.database as database
from app.core.security import get_current_user
from app.core.roles import require_admin

router = APIRouter()

# In-memory slot states: "tournament_id:slot_id" → slot_state dict
tournament_slots: dict = {}

# WebSocket connections per slot: "tid:sid" → {"p1": ws|None, "p2": ws|None}
tournament_ws_connections: dict = {}

# Events fired when a pending slot becomes ready: "tid:sid" → asyncio.Event
tournament_slot_events: dict = {}

# Locks to prevent double match creation: "tid:sid" → asyncio.Lock
tournament_match_locks: dict = {}

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
        next_match["ready_at"] = now.isoformat() + "Z"

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
        # Wake up any lobby WebSocket waiting in pending state for this slot
        if slot_key in tournament_slot_events:
            tournament_slot_events[slot_key].set()

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
        bracket = doc.pop("bracket", None)
        we = doc.get("winner_email")
        # Derive winner from bracket final if not stored (legacy tournaments)
        if not we and doc.get("status") == "finished" and bracket:
            try:
                final_match = bracket[-1][0]
                we = final_match.get("winner_email")
                if we:
                    doc["winner_email"] = we
                    from bson import ObjectId
                    await database.db.tournaments.update_one(
                        {"_id": ObjectId(doc["id"])},
                        {"$set": {"winner_email": we}}
                    )
            except (IndexError, KeyError, TypeError):
                pass
        if we:
            wu = await database.db.users.find_one({"email": we}, {"username": 1, "avatar": 1})
            if wu:
                doc["winner"] = {"email": we, "username": wu.get("username", we), "avatar": wu.get("avatar")}
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
                "ready_at": (ready_at.isoformat() + "Z") if isinstance(ready_at, datetime) else ready_at,
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
                match["ready_at"] = now.isoformat() + "Z"
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


@router.websocket("/api/tournaments/{tournament_id}/{slot_id}/ws")
async def tournament_lobby_ws(
    websocket: WebSocket,
    tournament_id: str,
    slot_id: str,
    token: str = Query(...),
):
    """Tournament match lobby WebSocket. Handles pending wait and 2-min countdown."""
    from jose import jwt as jose_jwt, JWTError
    from app.core.config import JWT_SECRET, ALGORITHM
    from bson import ObjectId

    await websocket.accept()

    # ── Auth ──────────────────────────────────────────────────────────────────
    try:
        payload = jose_jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise ValueError()
    except Exception:
        await websocket.send_json({"type": "error", "message": "Token inválido"})
        await websocket.close()
        return

    # ── Fetch tournament ───────────────────────────────────────────────────────
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        await websocket.send_json({"type": "error", "message": "Torneo no encontrado"})
        await websocket.close()
        return

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        await websocket.send_json({"type": "error", "message": "Torneo no encontrado"})
        await websocket.close()
        return

    slot_key = f"{tournament_id}:{slot_id}"

    def _find_match(bracket):
        for r_list in bracket:
            for m in r_list:
                if m["id"] == slot_id:
                    return m
        return None

    match_doc = _find_match(tournament.get("bracket", []))
    if not match_doc:
        await websocket.send_json({"type": "error", "message": "Partida no encontrada"})
        await websocket.close()
        return

    # ── Handle PENDING state (opponent's match still ongoing) ─────────────────
    if match_doc["status"] == "pending":
        if email not in tournament.get("participants", []):
            await websocket.send_json({"type": "error", "message": "No eres participante de este torneo"})
            await websocket.close()
            return

        await websocket.send_json({
            "type": "pending",
            "tournament_name": tournament.get("name", ""),
            "tournament_desc": tournament.get("description", ""),
        })

        if slot_key not in tournament_slot_events:
            tournament_slot_events[slot_key] = asyncio.Event()
        ev = tournament_slot_events[slot_key]

        # Poll until slot becomes ready (event fired by advance_bracket)
        while not ev.is_set():
            try:
                await asyncio.wait_for(asyncio.shield(ev.wait()), timeout=5.0)
            except asyncio.TimeoutError:
                try:
                    await websocket.send_json({"type": "waiting"})
                except Exception:
                    return  # client disconnected

        # Re-fetch after event
        tournament = await database.db.tournaments.find_one({"_id": oid})
        if not tournament:
            await websocket.close()
            return
        match_doc = _find_match(tournament.get("bracket", []))

    # ── Slot must now be READY ─────────────────────────────────────────────────
    slot = tournament_slots.get(slot_key)
    if not slot:
        # Match already created (e.g. page refresh)
        if match_doc and match_doc.get("match_id"):
            await websocket.send_json({"type": "match_ready", "match_id": match_doc["match_id"]})
            await websocket.close()
            return

        # Server restarted — recreate slot from DB if match is still within time window
        if match_doc and match_doc.get("status") == "ready" and match_doc.get("p1_email") and match_doc.get("p2_email"):
            ready_at_str = match_doc.get("ready_at")
            try:
                ready_at = datetime.fromisoformat(ready_at_str.replace("Z", "")).replace(tzinfo=None) if ready_at_str else datetime.utcnow()
            except Exception:
                ready_at = datetime.utcnow()
            elapsed_since = (datetime.utcnow() - ready_at).total_seconds()
            if elapsed_since >= 120:
                await websocket.send_json({"type": "forfeit", "message": "Tiempo agotado. Avanzando en el bracket..."})
                await websocket.close()
                return
            tournament_slots[slot_key] = {
                "p1_email": match_doc["p1_email"],
                "p2_email": match_doc["p2_email"],
                "p1_ready": False,
                "p2_ready": False,
                "match_id": None,
                "ready_at": ready_at,
                "event": asyncio.Event(),
            }
            remaining = max(0, 120 - elapsed_since)
            asyncio.create_task(_slot_timeout(tournament_id, slot_id, remaining))
            slot = tournament_slots[slot_key]
        else:
            await websocket.send_json({"type": "error", "message": "La partida ha expirado"})
            await websocket.close()
            return

    is_p1 = email == slot.get("p1_email")
    is_p2 = email == slot.get("p2_email")
    if not is_p1 and not is_p2:
        await websocket.send_json({"type": "error", "message": "No eres participante de esta partida"})
        await websocket.close()
        return

    ready_at = slot.get("ready_at")
    elapsed = (datetime.utcnow() - ready_at).total_seconds() if ready_at else 0
    if elapsed > 125:
        await websocket.send_json({"type": "forfeit", "message": "El tiempo para unirse ha expirado"})
        await websocket.close()
        return

    side = "p1" if is_p1 else "p2"
    other_side = "p2" if is_p1 else "p1"

    # Register WS and mark ready
    if slot_key not in tournament_ws_connections:
        tournament_ws_connections[slot_key] = {"p1": None, "p2": None}
    if slot_key not in tournament_match_locks:
        tournament_match_locks[slot_key] = asyncio.Lock()

    # Close stale connection for same side (page refresh)
    old_ws = tournament_ws_connections[slot_key].get(side)
    if old_ws and old_ws is not websocket:
        try:
            await old_ws.close()
        except Exception:
            pass

    tournament_ws_connections[slot_key][side] = websocket
    slot[f"{side}_ready"] = True

    # Opponent info
    opponent_email = slot["p2_email"] if is_p1 else slot["p1_email"]
    opponent_user = await database.db.users.find_one(
        {"email": opponent_email}, {"username": 1, "avatar": 1}
    ) if opponent_email else None

    remaining_secs = max(0, int(120 - elapsed))

    await websocket.send_json({
        "type": "init",
        "tournament_name": tournament.get("name", ""),
        "tournament_desc": tournament.get("description", ""),
        "opponent": {
            "username": (opponent_user or {}).get("username", opponent_email or ""),
            "avatar": (opponent_user or {}).get("avatar"),
        },
        "remaining_seconds": remaining_secs,
    })

    # Notify opponent's WS that I arrived
    other_ws = tournament_ws_connections[slot_key].get(other_side)
    if other_ws:
        try:
            await other_ws.send_json({"type": "opponent_joined"})
        except Exception:
            pass

    # If match already exists (e.g. both joined before this WS connected)
    if slot.get("match_id"):
        await websocket.send_json({"type": "match_ready", "match_id": slot["match_id"]})
        tournament_ws_connections[slot_key][side] = None
        await websocket.close()
        return

    # ── Match creation helper ──────────────────────────────────────────────────
    async def try_create_match() -> str | None:
        lock = tournament_match_locks.get(slot_key)
        if not lock:
            return None
        async with lock:
            s = tournament_slots.get(slot_key)
            if not s:
                return None
            if s.get("match_id"):
                return s["match_id"]
            if not (s.get("p1_ready") and s.get("p2_ready")):
                return None

            from app.routers.matchmaking import active_matches, _pick_exercise, _build_player_data
            p1_user = await database.db.users.find_one({"email": s["p1_email"]})
            p2_user = await database.db.users.find_one({"email": s["p2_email"]})
            if not p1_user or not p2_user:
                return None

            p1_data = await _build_player_data(s["p1_email"], p1_user)
            p2_data = await _build_player_data(s["p2_email"], p2_user)
            chosen_ex = await _pick_exercise()
            mid = str(uuid.uuid4())

            active_matches[mid] = {
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
            s["match_id"] = mid
            s["event"].set()

            try:
                t_doc = await database.db.tournaments.find_one({"_id": oid})
                if t_doc:
                    b = t_doc.get("bracket", [])
                    for r_list in b:
                        for m in r_list:
                            if m["id"] == slot_id:
                                m["status"] = "ongoing"
                                m["match_id"] = mid
                                break
                    await database.db.tournaments.update_one({"_id": oid}, {"$set": {"bracket": b}})
            except Exception:
                pass
            return mid

    async def notify_both_and_close(mid: str):
        for s_side in ("p1", "p2"):
            w = tournament_ws_connections.get(slot_key, {}).get(s_side)
            if w:
                try:
                    await w.send_json({"type": "match_ready", "match_id": mid})
                except Exception:
                    pass
        tournament_ws_connections[slot_key]["p1"] = None
        tournament_ws_connections[slot_key]["p2"] = None

    # Immediately check if both ready
    if slot.get("p1_ready") and slot.get("p2_ready"):
        mid = await try_create_match()
        if mid:
            await notify_both_and_close(mid)
            await websocket.close()
            return

    # ── Main tick loop ─────────────────────────────────────────────────────────
    try:
        while True:
            await asyncio.sleep(1)

            s = tournament_slots.get(slot_key)
            if not s:
                break

            if s.get("match_id"):
                await websocket.send_json({"type": "match_ready", "match_id": s["match_id"]})
                break

            if s.get("p1_ready") and s.get("p2_ready"):
                mid = await try_create_match()
                if mid:
                    await notify_both_and_close(mid)
                    break

            ra = s.get("ready_at")
            if ra:
                el = (datetime.utcnow() - ra).total_seconds()
                rem = max(0, int(120 - el))
                if rem <= 0:
                    await websocket.send_json({"type": "forfeit", "message": "Tiempo agotado. Avanzando en el bracket..."})
                    break
                await websocket.send_json({"type": "tick", "remaining_seconds": rem})

    except WebSocketDisconnect:
        pass
    finally:
        if slot_key in tournament_ws_connections:
            tournament_ws_connections[slot_key][side] = None


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
