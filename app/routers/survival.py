import asyncio
import json
import uuid

from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect, Query
from jose import JWTError, jwt

import app.core.database as database
from app.core.config import JWT_SECRET, ALGORITHM
from app.core.security import get_current_user
from app.routers.matchmaking import _pick_exercise

router = APIRouter()

# ── In-memory stores ──────────────────────────────────────────────────────────
survival_rooms: dict = {}    # { room_id: room_data }
survival_invites: dict = {}  # { invite_id: invite_data }

# ── Difficulty config ─────────────────────────────────────────────────────────
SURVIVAL_CONFIG = {
    "normal":    {"start_time": 60,  "bonus": 10, "label": "NORMAL"},
    "dificil":   {"start_time": 45,  "bonus": 7,  "label": "DIFÍCIL"},
    "demencial": {"start_time": 30,  "bonus": 5,  "label": "DEMENCIAL"},
}


# ── Broadcast helpers ─────────────────────────────────────────────────────────

async def _broadcast(room: dict, msg: dict):
    """Send msg to all connected players in the room."""
    dead = []
    for em, ws in list(room["connections"].items()):
        try:
            await ws.send_text(json.dumps(msg))
        except Exception:
            dead.append(em)
    for em in dead:
        room["connections"].pop(em, None)


async def _send_to(ws: WebSocket, msg: dict):
    try:
        await ws.send_text(json.dumps(msg))
    except Exception:
        pass


def _room_players_payload(room: dict) -> list:
    return [
        {"email": p["email"], "username": p["username"], "avatar": p["avatar"]}
        for p in room["players"]
    ]


def _exercise_payload(ex: dict) -> dict:
    """Strip heavy fields not needed by frontend (keep test_cases and stub)."""
    return {
        "id":          ex.get("id", ""),
        "title":       ex.get("title", ""),
        "difficulty":  ex.get("difficulty", ""),
        "category":    ex.get("category", ""),
        "description": ex.get("description", ""),
        "test_cases":  ex.get("test_cases", []),
        "stub":        ex.get("stub", {}),
    }


# ── Timer ─────────────────────────────────────────────────────────────────────

async def _run_timer(room_id: str):
    room = survival_rooms.get(room_id)
    if not room:
        return

    tick = 0
    while room.get("status") == "in_game" and room["time_left"] > 0:
        await asyncio.sleep(1)
        if room_id not in survival_rooms:
            return
        room = survival_rooms[room_id]
        if room.get("status") != "in_game":
            return

        room["time_left"] -= 1
        tick += 1

        # Broadcast time_sync every 5 seconds
        if tick % 5 == 0:
            await _broadcast(room, {"type": "time_sync", "time_left": room["time_left"]})

    if room_id in survival_rooms and room.get("status") == "in_game":
        await _end_game(room_id)


async def _end_game(room_id: str):
    room = survival_rooms.get(room_id)
    if not room or room.get("status") == "finished":
        return

    room["status"] = "finished"
    if room.get("timer_task") and not room["timer_task"].done():
        room["timer_task"].cancel()

    exercises_solved = room["exercises_solved"]
    diff_key = room["difficulty"]

    # Update each player's survival stats in MongoDB
    for player in room["players"]:
        player_email = player["email"]
        new_record = False
        try:
            user_doc = await database.db.users.find_one(
                {"email": player_email},
                {"survival_stats": 1}
            )
            current_max = 0
            if user_doc:
                current_max = (
                    user_doc
                    .get("survival_stats", {})
                    .get(diff_key, {})
                    .get("max_exercises", 0)
                )
            if exercises_solved > current_max:
                await database.db.users.update_one(
                    {"email": player_email},
                    {"$set": {f"survival_stats.{diff_key}.max_exercises": exercises_solved}}
                )
                new_record = True

            # Send personalized game_over to this player's connection
            ws = room["connections"].get(player_email)
            if ws:
                try:
                    await ws.send_text(json.dumps({
                        "type":             "game_over",
                        "exercises_solved": exercises_solved,
                        "difficulty":       diff_key,
                        "new_record":       new_record,
                    }))
                except Exception:
                    pass
        except Exception:
            pass

    # Schedule room cleanup after 60s
    async def _cleanup():
        await asyncio.sleep(60)
        survival_rooms.pop(room_id, None)

    asyncio.create_task(_cleanup())


# ── HTTP Endpoints ────────────────────────────────────────────────────────────

@router.post("/api/survival/room")
async def create_room(difficulty: str = "normal", email: str = Depends(get_current_user)):
    difficulty = difficulty.lower()
    if difficulty not in SURVIVAL_CONFIG:
        raise HTTPException(status_code=400, detail="Dificultad no válida. Usa: normal, dificil, demencial")

    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")

    room_id = str(uuid.uuid4())
    survival_rooms[room_id] = {
        "room_id":         room_id,
        "host_email":      email,
        "difficulty":      difficulty,
        "status":          "lobby",
        "players":         [
            {
                "email":    email,
                "username": user.get("username", ""),
                "avatar":   user.get("avatar", ""),
            }
        ],
        "connections":     {},
        "exercise":        None,
        "exercise_num":    0,
        "exercises_solved": 0,
        "time_left":       float(SURVIVAL_CONFIG[difficulty]["start_time"]),
        "timer_task":      None,
    }
    return {"room_id": room_id, "difficulty": difficulty}


@router.get("/api/survival/room/{room_id}")
async def get_room(room_id: str, email: str = Depends(get_current_user)):
    room = survival_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")

    player_emails = [p["email"] for p in room["players"]]
    if email not in player_emails:
        raise HTTPException(status_code=403, detail="No eres miembro de esta sala")

    return {
        "room_id":    room["room_id"],
        "difficulty": room["difficulty"],
        "status":     room["status"],
        "host_email": room["host_email"],
        "players":    _room_players_payload(room),
    }


@router.post("/api/survival/room/{room_id}/start")
async def start_room(room_id: str, email: str = Depends(get_current_user)):
    room = survival_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    if room["host_email"] != email:
        raise HTTPException(status_code=403, detail="Solo el anfitrión puede iniciar la partida")
    if room["status"] != "lobby":
        raise HTTPException(status_code=400, detail="La partida ya fue iniciada")

    exercise = await _pick_exercise()
    room["exercise"]     = exercise
    room["exercise_num"] = 1
    room["status"]       = "in_game"

    config = SURVIVAL_CONFIG[room["difficulty"]]
    room["time_left"] = float(config["start_time"])

    # Broadcast game_started to all WS connections
    await _broadcast(room, {
        "type":         "game_started",
        "exercise":     _exercise_payload(exercise),
        "time_left":    room["time_left"],
        "exercise_num": room["exercise_num"],
    })

    # Spawn server-side countdown
    task = asyncio.create_task(_run_timer(room_id))
    room["timer_task"] = task

    return {"ok": True}


# ── Invite endpoints ──────────────────────────────────────────────────────────

@router.post("/api/survival/invite/{room_id}/{target_username}")
async def survival_invite(room_id: str, target_username: str, email: str = Depends(get_current_user)):
    room = survival_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    if room["status"] != "lobby":
        raise HTTPException(status_code=400, detail="La partida ya fue iniciada")
    if len(room["players"]) >= 4:
        raise HTTPException(status_code=400, detail="La sala ya está llena (máximo 4 jugadores)")

    sender = await database.db.users.find_one({"email": email})
    target = await database.db.users.find_one({"username": target_username})
    if not sender or not target:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if target["email"] not in sender.get("friends", []):
        raise HTTPException(status_code=403, detail="Solo puedes invitar a tus amigos")

    # Check target is not already in room
    player_emails = [p["email"] for p in room["players"]]
    if target["email"] in player_emails:
        raise HTTPException(status_code=400, detail="El usuario ya está en la sala")

    invite_id = str(uuid.uuid4())
    survival_invites[invite_id] = {
        "invite_id":      invite_id,
        "from_email":     email,
        "from_username":  sender.get("username", email),
        "to_email":       target["email"],
        "room_id":        room_id,
        "difficulty":     room["difficulty"],
        "status":         "pending",
    }
    return {"invite_id": invite_id}


@router.get("/api/survival/pending-invites")
async def get_pending_invites(email: str = Depends(get_current_user)):
    result = [
        {
            "invite_id":     iid,
            "from_username": inv["from_username"],
            "room_id":       inv["room_id"],
            "difficulty":    inv["difficulty"],
        }
        for iid, inv in survival_invites.items()
        if inv["to_email"] == email and inv["status"] == "pending"
    ]
    return result


@router.post("/api/survival/accept/{invite_id}")
async def accept_invite(invite_id: str, email: str = Depends(get_current_user)):
    inv = survival_invites.get(invite_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invitación no encontrada")
    if inv["to_email"] != email:
        raise HTTPException(status_code=403, detail="No eres el destinatario")
    if inv["status"] != "pending":
        raise HTTPException(status_code=400, detail="Invitación ya procesada")

    room_id = inv["room_id"]
    room = survival_rooms.get(room_id)
    if not room:
        inv["status"] = "expired"
        raise HTTPException(status_code=404, detail="La sala ya no existe")
    if room["status"] != "lobby":
        inv["status"] = "expired"
        raise HTTPException(status_code=400, detail="La partida ya fue iniciada")
    if len(room["players"]) >= 4:
        inv["status"] = "expired"
        raise HTTPException(status_code=400, detail="La sala está llena")

    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")

    # Add player to room
    room["players"].append({
        "email":    email,
        "username": user.get("username", ""),
        "avatar":   user.get("avatar", ""),
    })
    inv["status"] = "accepted"

    # Notify existing WS connections of new player
    await _broadcast(room, {
        "type":    "player_joined",
        "players": _room_players_payload(room),
    })

    return {"room_id": room_id, "difficulty": room["difficulty"]}


@router.post("/api/survival/reject/{invite_id}")
async def reject_invite(invite_id: str, email: str = Depends(get_current_user)):
    inv = survival_invites.get(invite_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invitación no encontrada")
    if inv["to_email"] != email:
        raise HTTPException(status_code=403, detail="No eres el destinatario")
    inv["status"] = "rejected"
    return {"ok": True}


# ── WebSocket ─────────────────────────────────────────────────────────────────

@router.websocket("/api/survival/ws/{room_id}")
async def survival_ws(websocket: WebSocket, room_id: str, token: str = Query(...)):
    # Authenticate
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        jti: str   = payload.get("jti")
        if not email or not jti:
            await websocket.close(code=1008)
            return
        if await database.db.revoked_tokens.find_one({"jti": jti}):
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    room = survival_rooms.get(room_id)
    if not room:
        await websocket.close(code=1008)
        return

    player_emails = [p["email"] for p in room["players"]]
    if email not in player_emails:
        await websocket.close(code=1008)
        return

    await websocket.accept()
    room["connections"][email] = websocket

    # Send current room state on connect
    if room["status"] == "in_game":
        await _send_to(websocket, {
            "type":         "game_started",
            "exercise":     _exercise_payload(room["exercise"]),
            "time_left":    room["time_left"],
            "exercise_num": room["exercise_num"],
        })
    elif room["status"] == "lobby":
        await _send_to(websocket, {
            "type":    "player_joined",
            "players": _room_players_payload(room),
        })

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue

            action = msg.get("action")

            if action == "submit":
                if room.get("status") != "in_game":
                    continue

                # Find the submitting player's username
                submitter_username = next(
                    (p["username"] for p in room["players"] if p["email"] == email),
                    email
                )

                # Advance game state
                config = SURVIVAL_CONFIG[room["difficulty"]]
                room["exercises_solved"] += 1
                room["time_left"] = min(room["time_left"] + config["bonus"], 300.0)
                room["exercise_num"] += 1

                # Pick next exercise
                next_exercise = await _pick_exercise()
                room["exercise"] = next_exercise

                await _broadcast(room, {
                    "type":         "exercise_solved",
                    "solved_by":    submitter_username,
                    "next_exercise": _exercise_payload(next_exercise),
                    "time_added":   config["bonus"],
                    "time_left":    room["time_left"],
                    "exercise_num": room["exercise_num"],
                })

    except WebSocketDisconnect:
        room["connections"].pop(email, None)
        # Notify others that player left (only if lobby; in-game they continue)
        if room.get("status") == "lobby":
            await _broadcast(room, {
                "type":    "player_left",
                "players": _room_players_payload(room),
            })
