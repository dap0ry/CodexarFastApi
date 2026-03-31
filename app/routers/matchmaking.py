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
from app.models.exercise import SubmitBatchRequest

router = APIRouter()

# In-memory stores for matchmaking
waiting_players: dict = {}   # { email: { "ws": WebSocket, "data": player_data, "unranked": bool } }
active_matches: dict = {}    # { match_id: match_data }


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


async def _ws_handle_join(websocket: WebSocket, email: str, user: dict, unranked: bool):
    player_data = await _build_player_data(email, user)
    my_tier = player_data["tier"]

    # Look for an eligible opponent
    opponent_email = None
    for opp_email, opp in list(waiting_players.items()):
        if opp_email == email:
            continue
        if opp.get("unranked", False) != unranked:
            continue
        if not unranked and abs(opp["data"]["tier"] - my_tier) > 2:
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
            "unranked": unranked,
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
            "unranked": unranked
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
                await _ws_handle_join(websocket, email, user, bool(msg.get("unranked", False)))
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
async def submit_match_solution(match_id: str, body: SubmitBatchRequest, email: str = Depends(get_current_user)):
    match = active_matches.get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partida no encontrada")

    if match["status"] != "ongoing":
        return {"status": match["status"], "winner": match["winner"]}

    is_p1 = match["player1"]["email"] == email

    passed_count = sum(1 for r in body.results if r.get("passed", False))
    total_cases = len(match["exercise"]["test_cases"])
    progress_pct = (passed_count / total_cases) * 100 if total_cases > 0 else 0

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

        is_ranked = not match.get("unranked", False)
        winner_inc = {"elo": 25, "win_streak": 1, "wins": 1, "matches_played": 1}
        if is_ranked:
            winner_inc["ranked_wins"] = 1
        await database.db.users.update_one({"email": winner_email}, {"$inc": winner_inc})
        await database.db.users.update_one(
            {"email": loser_email},
            {"$inc": {"elo": -15, "matches_played": 1}, "$set": {"win_streak": 0}}
        )

        await database.db.matches.insert_one({
            "match_id": match_id,
            "player1_email": match["player1"]["email"],
            "player2_email": match["player2"]["email"],
            "winner_email": winner_email,
            "loser_email": loser_email,
            "exercise_id": match["exercise"].get("id"),
            "unranked": match.get("unranked", False),
            "created_at": datetime.utcnow()
        })

        match["event"].set()

        return {"status": "finished", "winner": email, "is_winner": True}

    return {"status": "ongoing", "progress": progress_pct}
