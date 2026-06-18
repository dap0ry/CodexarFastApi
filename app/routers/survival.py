import asyncio
import json
import random
import string
import time
import uuid

from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect, Query
from jose import JWTError, jwt

import app.core.database as database
from app.core.config import JWT_SECRET, ALGORITHM
from app.core.security import get_current_user

router = APIRouter()

# ── In-memory stores ──────────────────────────────────────────────────────────
survival_rooms: dict = {}    # { room_id: room_data }
survival_invites: dict = {}  # { invite_id: invite_data }


def _generate_join_code() -> str:
    existing = {r.get("join_code") for r in survival_rooms.values()}
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=6))
        if code not in existing:
            return code

# ── Config ─────────────────────────────────────────────────────────────────────
SURVIVAL_START_TIME = 1800   # 30 minutes
SURVIVAL_BONUS      = 300    # +5 minutes per exercise solved

# Exercise difficulty progression by exercise number
def _target_difficulty(exercise_num: int) -> int:
    if exercise_num <= 3:
        return 800
    if exercise_num <= 6:
        return 1200
    return 1600


# ── Broadcast helpers ─────────────────────────────────────────────────────────

async def _broadcast(room: dict, msg: dict):
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


async def _broadcast_to_others(room: dict, sender_email: str, msg: dict):
    for em, ws in list(room["connections"].items()):
        if em != sender_email:
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
    return {
        "id":               ex.get("id", ""),
        "title":            ex.get("title", ""),
        "title_i18n":       ex.get("title_i18n", {}),
        "difficulty":       ex.get("difficulty", ""),
        "category":         ex.get("category", ""),
        "description":      ex.get("description", ""),
        "description_i18n": ex.get("description_i18n", {}),
        "test_cases":       ex.get("test_cases", []),
        "stub":             ex.get("stub", {}),
    }


# ── Exercise picker (progressive difficulty) ──────────────────────────────────

async def _pick_survival_exercise(exercise_num: int) -> dict:
    from app.exercises_data import EXERCISES_SEED
    target_diff = _target_difficulty(exercise_num)

    valid = [
        ex for ex in EXERCISES_SEED
        if "test_cases" in ex and len(ex["test_cases"]) > 0
        and ex.get("difficulty") == target_diff
    ]
    if not valid:
        valid = [ex for ex in EXERCISES_SEED if "test_cases" in ex and len(ex["test_cases"]) > 0]

    chosen_ex = dict(random.choice(valid))

    db_exercise = await database.db.exercises.find_one({"title": chosen_ex["title"]})
    if db_exercise:
        chosen_ex["id"] = str(db_exercise["_id"])
        if "title_i18n" in db_exercise:
            chosen_ex["title_i18n"] = db_exercise["title_i18n"]
        if "description_i18n" in db_exercise:
            chosen_ex["description_i18n"] = db_exercise["description_i18n"]
    else:
        db_exercise = await database.db.exercises.find_one({"test_cases": {"$exists": True, "$ne": []}})
        if db_exercise:
            chosen_ex = {
                "title":            db_exercise.get("title", chosen_ex["title"]),
                "title_i18n":       db_exercise.get("title_i18n", {}),
                "description":      db_exercise.get("description", chosen_ex["description"]),
                "description_i18n": db_exercise.get("description_i18n", {}),
                "difficulty":       db_exercise.get("difficulty", chosen_ex["difficulty"]),
                "category":         db_exercise.get("category", chosen_ex["category"]),
                "test_cases":       db_exercise.get("test_cases", []),
                "stub":             db_exercise.get("stub", {}),
                "id":               str(db_exercise["_id"]),
            }
    return chosen_ex


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

    exercises_solved  = room["exercises_solved"]
    time_survived     = int(time.time() - room.get("started_at", time.time()))
    mode_key          = "coop" if len(room["players"]) > 1 else "solo"

    for player in room["players"]:
        player_email = player["email"]
        new_record = False
        try:
            user_doc = await database.db.users.find_one(
                {"email": player_email},
                {"survival_stats": 1}
            )
            current_stats = {}
            if user_doc:
                current_stats = user_doc.get("survival_stats", {}).get("survival", {})

            await database.db.users.update_one(
                {"email": player_email},
                {"$inc": {
                    "survival_games": 1,
                    f"survival_stats.survival.{mode_key}_games": 1,
                }}
            )

            update_fields = {}
            # Overall max
            if exercises_solved > current_stats.get("max_exercises", 0):
                update_fields["survival_stats.survival.max_exercises"] = exercises_solved
                new_record = True
            if time_survived > current_stats.get("max_time_survived", 0):
                update_fields["survival_stats.survival.max_time_survived"] = time_survived
                new_record = True
            # Mode-specific max
            if exercises_solved > current_stats.get(f"{mode_key}_max_exercises", 0):
                update_fields[f"survival_stats.survival.{mode_key}_max_exercises"] = exercises_solved
            if time_survived > current_stats.get(f"{mode_key}_max_time_survived", 0):
                update_fields[f"survival_stats.survival.{mode_key}_max_time_survived"] = time_survived

            if update_fields:
                await database.db.users.update_one(
                    {"email": player_email},
                    {"$set": update_fields}
                )

            ws = room["connections"].get(player_email)
            if ws:
                try:
                    await ws.send_text(json.dumps({
                        "type":             "game_over",
                        "exercises_solved": exercises_solved,
                        "time_survived":    time_survived,
                        "new_record":       new_record,
                        "abandoned_by":     room.get("abandoned_by"),
                    }))
                except Exception:
                    pass
        except Exception:
            pass

    async def _cleanup():
        await asyncio.sleep(60)
        survival_rooms.pop(room_id, None)

    asyncio.create_task(_cleanup())


# ── HTTP Endpoints ────────────────────────────────────────────────────────────

@router.post("/api/survival/room")
async def create_room(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")

    room_id   = str(uuid.uuid4())
    join_code = _generate_join_code()
    survival_rooms[room_id] = {
        "room_id":          room_id,
        "join_code":        join_code,
        "host_email":       email,
        "difficulty":       "survival",
        "status":           "lobby",
        "players":          [
            {
                "email":    email,
                "username": user.get("username", ""),
                "avatar":   user.get("avatar", ""),
            }
        ],
        "connections":      {},
        "exercise":         None,
        "exercise_num":     0,
        "exercises_solved": 0,
        "time_left":        float(SURVIVAL_START_TIME),
        "started_at":       None,
        "timer_task":       None,
    }
    return {"room_id": room_id, "join_code": join_code}


@router.get("/api/survival/room/by-code/{code}")
async def get_room_by_code(code: str, email: str = Depends(get_current_user)):
    code = code.strip().upper()
    for room_id, room in survival_rooms.items():
        if room.get("join_code") == code and room["status"] == "lobby":
            return {
                "room_id":   room_id,
                "join_code": code,
                "players":   _room_players_payload(room),
            }
    raise HTTPException(status_code=404, detail="Sala no encontrada o ya iniciada")


@router.post("/api/survival/room/{room_id}/join")
async def join_room(room_id: str, email: str = Depends(get_current_user)):
    room = survival_rooms.get(room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Sala no encontrada")
    if room["status"] != "lobby":
        raise HTTPException(status_code=400, detail="La partida ya fue iniciada")
    if len(room["players"]) >= 4:
        raise HTTPException(status_code=400, detail="La sala está llena")

    player_emails = [p["email"] for p in room["players"]]
    if email in player_emails:
        return {"room_id": room_id}

    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="No autorizado")

    room["players"].append({
        "email":    email,
        "username": user.get("username", ""),
        "avatar":   user.get("avatar", ""),
    })

    await _broadcast(room, {
        "type":    "player_joined",
        "players": _room_players_payload(room),
    })

    return {"room_id": room_id}


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

    exercise = await _pick_survival_exercise(1)
    room["exercise"]     = exercise
    room["exercise_num"] = 1
    room["status"]       = "in_game"
    room["time_left"]    = float(SURVIVAL_START_TIME)
    room["started_at"]   = time.time()

    await _broadcast(room, {
        "type":         "game_started",
        "exercise":     _exercise_payload(exercise),
        "time_left":    room["time_left"],
        "exercise_num": room["exercise_num"],
    })

    task = asyncio.create_task(_run_timer(room_id))
    room["timer_task"] = task

    return {"ok": True}


@router.get("/api/survival/my-record")
async def my_record(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one(
        {"email": email},
        {"survival_stats": 1, "survival_games": 1}
    )
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    stats = user.get("survival_stats", {}).get("survival", {})
    return {
        "max_exercises":     stats.get("max_exercises", 0),
        "max_time_survived": stats.get("max_time_survived", 0),
        "games_played":      user.get("survival_games", 0),
        "solo": {
            "games":             stats.get("solo_games", 0),
            "max_exercises":     stats.get("solo_max_exercises", 0),
            "max_time_survived": stats.get("solo_max_time_survived", 0),
        },
        "coop": {
            "games":             stats.get("coop_games", 0),
            "max_exercises":     stats.get("coop_max_exercises", 0),
            "max_time_survived": stats.get("coop_max_time_survived", 0),
        },
    }


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

    player_emails = [p["email"] for p in room["players"]]
    if target["email"] in player_emails:
        raise HTTPException(status_code=400, detail="El usuario ya está en la sala")

    invite_id = str(uuid.uuid4())
    survival_invites[invite_id] = {
        "invite_id":     invite_id,
        "from_email":    email,
        "from_username": sender.get("username", email),
        "to_email":      target["email"],
        "room_id":       room_id,
        "difficulty":    "survival",
        "status":        "pending",
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

    room["players"].append({
        "email":    email,
        "username": user.get("username", ""),
        "avatar":   user.get("avatar", ""),
    })
    inv["status"] = "accepted"

    await _broadcast(room, {
        "type":    "player_joined",
        "players": _room_players_payload(room),
    })

    return {"room_id": room_id, "difficulty": "survival"}


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

    if grace_task := room.get("disconnect_tasks", {}).pop(email, None):
        grace_task.cancel()

    if room["status"] == "in_game":
        await _send_to(websocket, {
            "type":         "game_started",
            "exercise":     _exercise_payload(room["exercise"]),
            "time_left":    room["time_left"],
            "exercise_num": room["exercise_num"],
            "current_code": room.get("current_code", ""),
        })
    elif room["status"] == "finished":
        # Player reconnected after game ended — send game_over so they see the result
        await _send_to(websocket, {
            "type":             "game_over",
            "exercises_solved": room["exercises_solved"],
            "time_survived":    int(time.time() - room.get("started_at", time.time())),
            "new_record":       False,
            "abandoned_by":     room.get("abandoned_by"),
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

                submitter_username = next(
                    (p["username"] for p in room["players"] if p["email"] == email),
                    email
                )

                room["exercises_solved"] += 1
                room["time_left"]        += SURVIVAL_BONUS
                room["exercise_num"]     += 1

                next_exercise = await _pick_survival_exercise(room["exercise_num"])
                room["exercise"]      = next_exercise
                room["current_code"]  = ""

                await _broadcast(room, {
                    "type":          "exercise_solved",
                    "solved_by":     submitter_username,
                    "next_exercise": _exercise_payload(next_exercise),
                    "time_added":    SURVIVAL_BONUS,
                    "time_left":     room["time_left"],
                    "exercise_num":  room["exercise_num"],
                })

            elif action == "code_sync":
                if room.get("status") != "in_game":
                    continue
                code = msg.get("code", "")
                lang = msg.get("lang", "Python")
                room["current_code"] = code
                sender_username = next(
                    (p["username"] for p in room["players"] if p["email"] == email),
                    email
                )
                await _broadcast_to_others(room, email, {
                    "type":     "code_sync",
                    "code":     code,
                    "lang":     lang,
                    "username": sender_username,
                })

            elif action == "lang_sync":
                if room.get("status") != "in_game":
                    continue
                lang = msg.get("lang", "Python")
                sender_username = next(
                    (p["username"] for p in room["players"] if p["email"] == email),
                    email
                )
                await _broadcast_to_others(room, email, {
                    "type":     "lang_sync",
                    "lang":     lang,
                    "username": sender_username,
                })

            elif action == "abandon":
                if room.get("status") != "in_game":
                    continue
                leaver = next(
                    (p["username"] for p in room["players"] if p["email"] == email),
                    email
                )
                room["abandoned_by"] = leaver
                await _end_game(room_id)

    except WebSocketDisconnect:
        room["connections"].pop(email, None)
        if room.get("status") == "lobby":
            await _broadcast(room, {
                "type":    "player_left",
                "players": _room_players_payload(room),
            })
        elif room.get("status") == "in_game":
            async def _grace_end(r_id=room_id, e=email):
                await asyncio.sleep(5)
                r = survival_rooms.get(r_id)
                if r and r.get("status") == "in_game" and e not in r.get("connections", {}):
                    leaver = next((p["username"] for p in r["players"] if p["email"] == e), e)
                    r["abandoned_by"] = leaver
                    await _end_game(r_id)
            grace_task = asyncio.create_task(_grace_end())
            room.setdefault("disconnect_tasks", {})[email] = grace_task
