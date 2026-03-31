import asyncio
import uuid
import random
from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends

import app.core.database as database
from app.core.security import get_current_user
from app.models.exercise import SubmitBatchRequest

router = APIRouter()

# In-memory stores for matchmaking
waiting_players = []  # List of dicts
active_matches = {}   # dict of match_id -> match data


@router.post("/api/matchmaking/join")
async def join_matchmaking(unranked: bool = False, email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    global waiting_players

    # Remove if already in queue
    waiting_players = [p for p in waiting_players if p["email"] != email]

    elo = user.get("elo", 0)
    higher_elo_count = await database.db.users.count_documents({"elo": {"$gt": elo}})
    rank = higher_elo_count + 1

    # Function from /api/user/me duplicated locally for quick matchmaking
    def get_rank_tier(e):
        if e <= 75: return min(3, max(1, (e // 26) + 1))
        elif e <= 300: return 3 + min(3, max(1, ((e - 76) // 75) + 1))
        elif e <= 800: return 6 + min(3, max(1, ((e - 301) // 167) + 1))
        elif e <= 1300: return 9 + min(3, max(1, ((e - 801) // 167) + 1))
        elif e <= 2000: return 12 + min(3, max(1, ((e - 1301) // 234) + 1))
        else: return 16

    my_tier = get_rank_tier(elo)

    player_data = {
        "email": email,
        "username": user.get("username", "Unknown"),
        "avatar": user.get("avatar", ""),
        "elo": elo,
        "rank": rank,
        "tier": my_tier
    }

    # Check for opponent
    opponent = None
    for i, p in enumerate(waiting_players):
        # Match only requests of the same type (ranked vs unranked)
        if p.get("unranked", False) == unranked:
            # If ranked, verify the tier difference is <= 2
            if unranked or abs(p["data"]["tier"] - my_tier) <= 2:
                opponent = waiting_players.pop(i)
                break

    if opponent:
        match_id = str(uuid.uuid4())
        from app.exercises_data import EXERCISES_SEED
        # Filter exercises that are not just empty stubs
        valid_exercises = [ex for ex in EXERCISES_SEED if "test_cases" in ex and len(ex["test_cases"]) > 0]
        chosen_ex = dict(random.choice(valid_exercises) if valid_exercises else EXERCISES_SEED[0])

        # Look up the exercise in MongoDB by title to get its real _id
        # so the frontend can call /api/exercises/{id}/solve correctly
        db_exercise = await database.db.exercises.find_one({"title": chosen_ex["title"]})
        if db_exercise:
            chosen_ex["id"] = str(db_exercise["_id"])
        else:
            # Fallback: try to find any exercise with test cases in MongoDB
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
            # If still nothing from DB, leave id missing — solve endpoint will 400

        active_matches[match_id] = {
            "player1": opponent["data"],
            "player2": player_data,
            "p1_progress": 0,
            "p2_progress": 0,
            "exercise": chosen_ex,
            "status": "ongoing",
            "winner": None,
            "unranked": unranked,
            "event": asyncio.Event()
        }

        opponent["match_id"] = match_id
        opponent["event"].set()  # Wake up opponent

        return {"status": "matched", "match_id": match_id}

    # No opponent, wait in queue
    my_event = asyncio.Event()
    my_entry = {
        "email": email,
        "data": player_data,
        "event": my_event,
        "match_id": None
    }
    waiting_players.append(my_entry)

    try:
        # Long poll for 25 seconds
        await asyncio.wait_for(my_event.wait(), timeout=25.0)
        return {"status": "matched", "match_id": my_entry["match_id"]}
    except asyncio.TimeoutError:
        # Remove from queue if timeout
        waiting_players = [p for p in waiting_players if p["email"] != email]
        return {"status": "timeout"}


@router.delete("/api/matchmaking/leave")
async def leave_matchmaking(email: str = Depends(get_current_user)):
    global waiting_players
    waiting_players = [p for p in waiting_players if p["email"] != email]
    return {"status": "left"}


@router.get("/api/matchmaking/match/{match_id}")
async def get_match_state(match_id: str, email: str = Depends(get_current_user)):
    match = active_matches.get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partida no encontrada")

    # Which player is asking?
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
        # Wait up to 25s for an event (progress update or win)
        await asyncio.wait_for(match["event"].wait(), timeout=25.0)

        # Determine who won or what the state is
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

    # Update progress
    if is_p1:
        match["p1_progress"] = progress_pct
    else:
        match["p2_progress"] = progress_pct

    match["event"].set()
    await asyncio.sleep(0.1)  # Let pollers wake up
    match["event"].clear()

    if progress_pct == 100:
        # Match ends
        match["status"] = "finished"
        match["winner"] = email

        # Assign ELO and win streak
        winner_email = email
        loser_email = match["player2"]["email"] if is_p1 else match["player1"]["email"]

        # Simple ELO update logic (+25 won, -15 lost) and track real win/match stats
        is_ranked = not match.get("unranked", False)
        coins_reward = 30 if is_ranked else 15
        winner_inc = {"elo": 25, "win_streak": 1, "wins": 1, "matches_played": 1, "coins": coins_reward}
        if is_ranked:
            winner_inc["ranked_wins"] = 1
        await database.db.users.update_one({"email": winner_email}, {"$inc": winner_inc})
        await database.db.users.update_one({"email": loser_email}, {"$inc": {"elo": -15, "matches_played": 1}, "$set": {"win_streak": 0}})

        # Save Match to Database
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
