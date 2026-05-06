import asyncio
import json
import uuid
import random
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, WebSocket, WebSocketDisconnect, Query
from jose import JWTError, jwt

import app.core.database as database
from app.core.config import JWT_SECRET, ALGORITHM
from app.core.security import get_current_user
from app.models.exercise import MatchSubmitRequest

router = APIRouter()

# In-memory stores for matchmaking
waiting_players: dict = {}   # { email: { "ws": WebSocket, "data": player_data } }
active_matches: dict = {}    # { match_id: match_data }
pending_invites: dict = {}   # { invite_id: { "from": email, "to": email, "from_username": str, "status": "pending"|"accepted"|"rejected", "match_id": None } }


def _get_rank_tier(e: int) -> int:
    if e <= 75:    return min(3, max(1, (e // 26) + 1))
    elif e <= 300:  return 3 + min(3, max(1, ((e - 76) // 75) + 1))
    elif e <= 800:  return 6 + min(3, max(1, ((e - 301) // 167) + 1))
    elif e <= 1300: return 9 + min(3, max(1, ((e - 801) // 167) + 1))
    elif e <= 2000: return 12 + min(3, max(1, ((e - 1301) // 234) + 1))
    else:           return 16


async def _build_player_data(email: str, user: dict) -> dict:
    elo = user.get("elo", 0)
    higher_elo_count = await database.db.users.count_documents({"elo": {"$gt": elo}})
    rank = higher_elo_count + 1
    return {
        "email": email,
        "username": user.get("username", "Unknown"),
        "avatar": user.get("avatar", ""),
        "elo": elo,
        "rank": rank,
        "tier": _get_rank_tier(elo)
    }


async def _pick_exercise() -> dict:
    from app.exercises_data import EXERCISES_SEED
    valid_exercises = [ex for ex in EXERCISES_SEED if "test_cases" in ex and len(ex["test_cases"]) > 0]
    chosen_ex = dict(random.choice(valid_exercises) if valid_exercises else EXERCISES_SEED[0])

    db_exercise = await database.db.exercises.find_one({"title": chosen_ex["title"]})
    if db_exercise:
        chosen_ex["id"] = str(db_exercise["_id"])
    else:
        db_exercise = await database.db.exercises.find_one({"test_cases": {"$exists": True, "$ne": []}})
        if db_exercise:
            chosen_ex = {
                "title": db_exercise.get("title", chosen_ex["title"]),
                "description": db_exercise.get("description", chosen_ex["description"]),
                "difficulty": db_exercise.get("difficulty", chosen_ex["difficulty"]),
                "category": db_exercise.get("category", chosen_ex["category"]),
                "test_cases": db_exercise.get("test_cases", chosen_ex["test_cases"]),
                "stub": db_exercise.get("stub", chosen_ex.get("stub", {})),
                "id": str(db_exercise["_id"])
            }
    return chosen_ex


async def _ws_handle_join(websocket: WebSocket, email: str, user: dict):
    player_data = await _build_player_data(email, user)
    my_tier = player_data["tier"]

    # Look for an eligible opponent (SBMM: max 2 tier difference)
    opponent_email = None
    for opp_email, opp in list(waiting_players.items()):
        if opp_email == email:
            continue
        if abs(opp["data"]["tier"] - my_tier) > 2:
            continue
        opponent_email = opp_email
        break

    if opponent_email:
        opp = waiting_players.pop(opponent_email)
        match_id = str(uuid.uuid4())
        chosen_ex = await _pick_exercise()

        active_matches[match_id] = {
            "player1": opp["data"],
            "player2": player_data,
            "p1_progress": 0,
            "p2_progress": 0,
            "exercise": chosen_ex,
            "status": "ongoing",
            "winner": None,
            "event": asyncio.Event()
        }

        matched_msg = json.dumps({"status": "matched", "match_id": match_id})
        try:
            await opp["ws"].send_text(matched_msg)
        except Exception:
            pass  # Opponent disconnected mid-match-creation; match still valid for current player
        await websocket.send_text(matched_msg)
    else:
        # No opponent found — add to queue and wait (server will push when another player joins)
        waiting_players[email] = {
            "email": email,
            "data": player_data,
            "ws": websocket,
        }
        await websocket.send_text(json.dumps({"status": "queued"}))


@router.websocket("/api/matchmaking/ws")
async def matchmaking_ws(websocket: WebSocket, token: str = Query(...)):
    # Authenticate via token query param (WebSocket cannot use Bearer header)
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        jti: str = payload.get("jti")
        if not email or not jti:
            await websocket.close(code=1008)
            return
        if await database.db.revoked_tokens.find_one({"jti": jti}):
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    user = await database.db.users.find_one({"email": email})
    if not user:
        await websocket.close(code=1008)
        return

    await websocket.accept()

    # Remove any stale queue entry (reconnect after page navigation)
    waiting_players.pop(email, None)

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                continue

            action = msg.get("action")
            if action == "join":
                await _ws_handle_join(websocket, email, user)
            elif action == "leave":
                waiting_players.pop(email, None)
                await websocket.send_text(json.dumps({"status": "left"}))
    except WebSocketDisconnect:
        waiting_players.pop(email, None)


@router.get("/api/matchmaking/match/{match_id}")
async def get_match_state(match_id: str, email: str = Depends(get_current_user)):
    match = active_matches.get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partida no encontrada")

    if match["player1"]["email"] != email and match["player2"]["email"] != email:
        raise HTTPException(status_code=403, detail="No eres participante de esta partida")

    is_p1 = match["player1"]["email"] == email
    opponent_data = match["player2"] if is_p1 else match["player1"]
    my_data = match["player1"] if is_p1 else match["player2"]

    my_progress = match["p1_progress"] if is_p1 else match["p2_progress"]
    op_progress = match["p2_progress"] if is_p1 else match["p1_progress"]

    return {
        "me": my_data,
        "my_progress": my_progress,
        "opponent": opponent_data,
        "op_progress": op_progress,
        "exercise": match["exercise"],
        "status": match["status"],
        "winner": match["winner"]
    }


@router.get("/api/matchmaking/match/{match_id}/poll")
async def poll_match_state(match_id: str, email: str = Depends(get_current_user)):
    match = active_matches.get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partida no encontrada")

    if match["player1"]["email"] != email and match["player2"]["email"] != email:
        raise HTTPException(status_code=403, detail="No eres participante de esta partida")

    try:
        await asyncio.wait_for(match["event"].wait(), timeout=25.0)

        is_p1 = match["player1"]["email"] == email
        op_progress = match["p2_progress"] if is_p1 else match["p1_progress"]

        return {
            "status": "updated",
            "op_progress": op_progress,
            "match_status": match["status"],
            "winner": match["winner"]
        }
    except asyncio.TimeoutError:
        return {"status": "timeout"}


@router.post("/api/matchmaking/match/{match_id}/submit")
async def submit_match_solution(match_id: str, body: MatchSubmitRequest, email: str = Depends(get_current_user)):
    from app.routers.exercises import _run_with_judge0, JUDGE0_LANG

    match = active_matches.get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partida no encontrada")

    if match["player1"]["email"] != email and match["player2"]["email"] != email:
        raise HTTPException(status_code=403, detail="No eres participante de esta partida")

    if match["status"] != "ongoing":
        return {"status": match["status"], "winner": match["winner"]}

    if body.language not in JUDGE0_LANG:
        return {"status": "ongoing", "correct": False, "message": f"Lenguaje no soportado: {body.language}"}

    is_p1 = match["player1"]["email"] == email

    test_cases = match["exercise"].get("test_cases", [])
    if not test_cases:
        return {"status": "ongoing", "correct": False, "message": "El ejercicio no tiene casos de prueba"}

    result = await _run_with_judge0(body.language, body.code, test_cases)
    if not result["correct"]:
        return {"status": "ongoing", "correct": False, **{k: v for k, v in result.items() if k != "correct"}}

    progress_pct = 100

    if is_p1:
        match["p1_progress"] = progress_pct
    else:
        match["p2_progress"] = progress_pct

    match["event"].set()
    await asyncio.sleep(0.1)
    match["event"].clear()

    if progress_pct == 100:
        match["status"] = "finished"
        match["winner"] = email

        winner_email = email
        loser_email = match["player2"]["email"] if is_p1 else match["player1"]["email"]
        match_type = match.get("match_type")
        is_friendly = match_type == "friendly"
        is_tournament = match_type == "tournament"

        if is_tournament:
            # Tournament: no ELO, only tournament-specific stats
            await database.db.users.update_one(
                {"email": winner_email},
                {"$inc": {"tournament_match_wins": 1, "coins": 20, "matches_played": 1}}
            )
            await database.db.users.update_one(
                {"email": loser_email},
                {"$inc": {"tournament_match_losses": 1, "matches_played": 1}}
            )
            # Advance the bracket
            t_id = match.get("tournament_id")
            s_id = match.get("slot_id")
            if t_id and s_id:
                from app.routers.tournaments import advance_bracket
                asyncio.create_task(advance_bracket(t_id, s_id, winner_email))
        elif not is_friendly:
            winner_inc = {"elo": 25, "win_streak": 1, "wins": 1, "matches_played": 1, "coins": 30, "ranked_wins": 1}
            await database.db.users.update_one({"email": winner_email}, {"$inc": winner_inc})

            # Track max_elo
            winner_doc = await database.db.users.find_one({"email": winner_email}, {"elo": 1, "max_elo": 1})
            new_elo = winner_doc.get("elo", 0)
            if new_elo > winner_doc.get("max_elo", 0):
                await database.db.users.update_one({"email": winner_email}, {"$set": {"max_elo": new_elo}})

            await database.db.users.update_one(
                {"email": loser_email},
                {"$inc": {"elo": -15, "matches_played": 1}, "$set": {"win_streak": 0}}
            )
        else:
            # Friendly: solo coins simbólicas, sin ELO ni stats ranked
            await database.db.users.update_one({"email": winner_email}, {"$inc": {"coins": 10}})

        await database.db.matches.insert_one({
            "match_id": match_id,
            "player1_email": match["player1"]["email"],
            "player2_email": match["player2"]["email"],
            "winner_email": winner_email,
            "loser_email": loser_email,
            "exercise_id": match["exercise"].get("id"),
            "created_at": datetime.utcnow()
        })

        match["event"].set()

        return {"status": "finished", "winner": email, "is_winner": True}

    return {"status": "ongoing", "progress": progress_pct}


# ── Friendly battle invite endpoints ─────────────────────────────────────────

@router.post("/api/friendly/invite/{target_username}")
async def friendly_invite(target_username: str, email: str = Depends(get_current_user)):
    target = await database.db.users.find_one({"username": target_username})
    if not target:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    sender = await database.db.users.find_one({"email": email})
    if not sender:
        raise HTTPException(status_code=401, detail="No autorizado")

    if target["email"] not in sender.get("friends", []):
        raise HTTPException(status_code=403, detail="Solo puedes retar a tus amigos")

    invite_id = str(uuid.uuid4())
    pending_invites[invite_id] = {
        "from": email,
        "to": target["email"],
        "from_username": sender.get("username", email),
        "status": "pending",
        "match_id": None,
    }
    return {"invite_id": invite_id}


@router.get("/api/friendly/pending")
async def friendly_pending(email: str = Depends(get_current_user)):
    result = [
        {"invite_id": iid, "from_username": inv["from_username"]}
        for iid, inv in pending_invites.items()
        if inv["to"] == email and inv["status"] == "pending"
    ]
    return result


@router.post("/api/friendly/accept/{invite_id}")
async def friendly_accept(invite_id: str, email: str = Depends(get_current_user)):
    inv = pending_invites.get(invite_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invitación no encontrada")
    if inv["to"] != email:
        raise HTTPException(status_code=403, detail="No eres el destinatario")
    if inv["status"] != "pending":
        raise HTTPException(status_code=400, detail="Invitación ya procesada")

    # Build player data for both participants
    sender_user = await database.db.users.find_one({"email": inv["from"]})
    receiver_user = await database.db.users.find_one({"email": email})

    if not sender_user or not receiver_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    p1_data = await _build_player_data(inv["from"], sender_user)
    p2_data = await _build_player_data(email, receiver_user)
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
        "match_type": "friendly",
        "event": asyncio.Event()
    }

    inv["status"] = "accepted"
    inv["match_id"] = match_id
    return {"match_id": match_id}


@router.post("/api/friendly/reject/{invite_id}")
async def friendly_reject(invite_id: str, email: str = Depends(get_current_user)):
    inv = pending_invites.get(invite_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invitación no encontrada")
    if inv["to"] != email:
        raise HTTPException(status_code=403, detail="No eres el destinatario")
    inv["status"] = "rejected"
    return {"ok": True}


@router.post("/api/friendly/cancel/{invite_id}")
async def friendly_cancel(invite_id: str, email: str = Depends(get_current_user)):
    inv = pending_invites.get(invite_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invitación no encontrada")
    if inv["from"] != email:
        raise HTTPException(status_code=403, detail="No eres el emisor")
    if inv["status"] != "pending":
        raise HTTPException(status_code=400, detail="Invitación ya procesada")
    inv["status"] = "cancelled"
    return {"ok": True}


@router.get("/api/friendly/invite-status/{invite_id}")
async def friendly_invite_status(invite_id: str, email: str = Depends(get_current_user)):
    inv = pending_invites.get(invite_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invitación no encontrada")
    if inv["from"] != email:
        raise HTTPException(status_code=403, detail="No eres el emisor")
    return {"status": inv["status"], "match_id": inv["match_id"]}
