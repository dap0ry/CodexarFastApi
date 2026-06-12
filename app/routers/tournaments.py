"""
tournaments.py — Codexar Tournaments · Exercise Scoring System
Score-based tournaments with up to 6 exercises, configurable duration.
Desktop app required to play. Web shows info + leaderboard only.
"""

from datetime import datetime, timedelta
from typing import Optional

import cloudinary.uploader
from bson import ObjectId
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from pydantic import BaseModel

import app.core.database as database
from app.core.security import get_current_user
from app.core.roles import require_admin

router = APIRouter()


# ── Helpers ───────────────────────────────────────────────────────────────────

def _oid(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


def _compute_leaderboard(submissions: list, participants_info: list) -> list:
    """Rank participants by total_score DESC, then total_time ASC (tiebreaker)."""
    user_map = {p["email"]: p for p in participants_info}
    scores: dict = {}
    for sub in submissions:
        if not sub.get("passed"):
            continue
        email = sub["email"]
        ex_id = sub["exercise_id"]
        if email not in scores:
            scores[email] = {"total_score": 0, "total_time": 0, "solved": set()}
        if ex_id not in scores[email]["solved"]:
            scores[email]["total_score"] += sub.get("score", 0)
            scores[email]["total_time"] += sub.get("time_seconds", 0)
            scores[email]["solved"].add(ex_id)

    board = []
    seen = set()
    for email, data in scores.items():
        seen.add(email)
        info = user_map.get(email, {"email": email, "username": email, "avatar": None})
        board.append({
            "email": email,
            "username": info.get("username", email),
            "avatar": info.get("avatar"),
            "total_score": data["total_score"],
            "total_time": data["total_time"],
            "exercises_solved": len(data["solved"]),
        })

    for p in participants_info:
        if p["email"] not in seen:
            board.append({
                "email": p["email"],
                "username": p.get("username", p["email"]),
                "avatar": p.get("avatar"),
                "total_score": 0,
                "total_time": 0,
                "exercises_solved": 0,
            })

    board.sort(key=lambda x: (-x["total_score"], x["total_time"]))
    return board[:10]


async def _check_auto_finish(tournament: dict, oid: ObjectId) -> dict:
    """If the tournament duration has elapsed, mark it as finished."""
    if tournament.get("status") != "active":
        return tournament
    started = tournament.get("started_at")
    duration = tournament.get("duration_minutes", 240)
    if not started:
        return tournament
    if isinstance(started, str):
        started = datetime.fromisoformat(started.replace("Z", ""))
    if datetime.utcnow() > started + timedelta(minutes=duration):
        await database.db.tournaments.update_one(
            {"_id": oid},
            {"$set": {"status": "finished", "ended_at": datetime.utcnow()}}
        )
        tournament["status"] = "finished"
        tournament["ended_at"] = datetime.utcnow()
    return tournament


# ── Schemas ───────────────────────────────────────────────────────────────────

class SubmitExerciseRequest(BaseModel):
    code: str
    language: str


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/api/tournaments")
async def create_tournament(
    name: str = Form(...),
    description: str = Form(""),
    start_time: str = Form(...),
    duration_minutes: int = Form(240),
    exercise_ids: str = Form(""),
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

    ex_ids = [e.strip() for e in exercise_ids.split(",") if e.strip()][:6]
    duration_minutes = max(60, min(duration_minutes, 600))

    doc = {
        "name": name.strip(),
        "description": description.strip(),
        "banner_url": banner_url,
        "created_by": admin["email"],
        "created_by_username": admin.get("username", ""),
        "status": "upcoming",
        "created_at": datetime.utcnow(),
        "start_time": start_dt,
        "duration_minutes": duration_minutes,
        "exercises": ex_ids,
        "participants": [],
        "submissions": [],
        "finished_participants": [],
        "winner_email": None,
        "ended_at": None,
        "started_at": None,
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
        doc.pop("submissions", None)
        doc.pop("finished_participants", None)
        oid = ObjectId(doc["id"])
        doc = await _check_auto_finish(doc, oid)

        we = doc.get("winner_email")
        if not we and doc.get("status") == "finished":
            # Compute winner lazily
            t_full = await database.db.tournaments.find_one({"_id": oid})
            if t_full:
                subs = t_full.get("submissions", [])
                pts = t_full.get("participants", [])
                if pts:
                    p_info = []
                    async for u in database.db.users.find(
                        {"email": {"$in": pts}}, {"email": 1, "username": 1, "avatar": 1}
                    ):
                        p_info.append({"email": u["email"], "username": u.get("username", u["email"]), "avatar": u.get("avatar")})
                    board = _compute_leaderboard(subs, p_info)
                    if board:
                        we = board[0]["email"]
                        await database.db.tournaments.update_one(
                            {"_id": oid}, {"$set": {"winner_email": we}}
                        )
                        doc["winner_email"] = we

        if we:
            wu = await database.db.users.find_one({"email": we}, {"username": 1, "avatar": 1})
            doc["winner"] = {
                "email": we,
                "username": wu.get("username", we) if wu else we,
                "avatar": wu.get("avatar") if wu else None,
            }
        result.append(doc)
    return result


@router.get("/api/tournaments/{tournament_id}")
async def get_tournament(tournament_id: str, email: str = Depends(get_current_user)):
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    tournament = _oid(tournament)
    tournament = await _check_auto_finish(tournament, oid)

    # Participants info
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

    # Exercises info
    exercises_info = []
    for ex_id in tournament.get("exercises", []):
        try:
            ex = await database.db.exercises.find_one(
                {"_id": ObjectId(ex_id)},
                {"title": 1, "difficulty": 1, "category": 1, "description": 1, "title_i18n": 1, "stub": 1, "description_i18n": 1}
            )
            if ex:
                exercises_info.append({
                    "id": ex_id,
                    "title": ex.get("title", ""),
                    "title_i18n": ex.get("title_i18n"),
                    "description": ex.get("description", ""),
                    "description_i18n": ex.get("description_i18n"),
                    "difficulty": ex.get("difficulty", 800),
                    "category": ex.get("category", ""),
                    "stub": ex.get("stub", {}),
                })
        except Exception:
            pass
    tournament["exercises_info"] = exercises_info

    # Leaderboard
    submissions = tournament.get("submissions", [])
    tournament["leaderboard"] = _compute_leaderboard(submissions, participants_info)

    # My solved exercises (for the app)
    my_solved = {s["exercise_id"] for s in submissions if s.get("email") == email and s.get("passed")}
    tournament["my_solved_exercises"] = list(my_solved)

    # Has user finished
    tournament["i_finished"] = email in tournament.get("finished_participants", [])

    # Winner
    we = tournament.get("winner_email")
    if not we and tournament.get("status") == "finished" and tournament["leaderboard"]:
        we = tournament["leaderboard"][0]["email"]
        await database.db.tournaments.update_one({"_id": oid}, {"$set": {"winner_email": we}})
        tournament["winner_email"] = we
    if we:
        wu = await database.db.users.find_one({"email": we}, {"username": 1, "avatar": 1})
        tournament["winner"] = {
            "email": we,
            "username": wu.get("username", we) if wu else we,
            "avatar": wu.get("avatar") if wu else None,
        }

    return tournament


@router.post("/api/tournaments/{tournament_id}/join")
async def join_tournament(tournament_id: str, email: str = Depends(get_current_user)):
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
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    if tournament.get("status") != "upcoming":
        raise HTTPException(status_code=400, detail="El torneo ya está activo o ha terminado")
    if not tournament.get("exercises"):
        raise HTTPException(status_code=400, detail="Configura al menos un ejercicio antes de iniciar")

    participants = tournament.get("participants", [])
    now = datetime.utcnow()

    if participants:
        await database.db.users.update_many(
            {"email": {"$in": participants}},
            {"$inc": {"tournaments_joined": 1}}
        )

    await database.db.tournaments.update_one(
        {"_id": oid},
        {"$set": {"status": "active", "started_at": now}}
    )
    return {"message": "Torneo iniciado.", "participants": len(participants)}


@router.post("/api/tournaments/{tournament_id}/submit/{exercise_id}")
async def submit_exercise(
    tournament_id: str,
    exercise_id: str,
    body: SubmitExerciseRequest,
    email: str = Depends(get_current_user),
):
    """Submit a solution for a tournament exercise (desktop app only)."""
    try:
        oid = ObjectId(tournament_id)
        ex_oid = ObjectId(exercise_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")

    tournament_doc = dict(tournament)
    tournament_doc = await _check_auto_finish(tournament_doc, oid)
    if tournament_doc.get("status") != "active":
        raise HTTPException(status_code=400, detail="El torneo no está activo")
    if email not in tournament_doc.get("participants", []):
        raise HTTPException(status_code=403, detail="No estás inscrito en este torneo")
    if email in tournament_doc.get("finished_participants", []):
        raise HTTPException(status_code=400, detail="Ya has entregado el torneo")
    if exercise_id not in tournament_doc.get("exercises", []):
        raise HTTPException(status_code=400, detail="Este ejercicio no pertenece al torneo")

    already_solved = any(
        s["email"] == email and s["exercise_id"] == exercise_id and s.get("passed")
        for s in tournament_doc.get("submissions", [])
    )
    if already_solved:
        raise HTTPException(status_code=400, detail="Ya has resuelto este ejercicio")

    started_at = tournament_doc.get("started_at")
    if started_at:
        if isinstance(started_at, str):
            started_at = datetime.fromisoformat(started_at.replace("Z", ""))
        duration = tournament_doc.get("duration_minutes", 240)
        if datetime.utcnow() > started_at + timedelta(minutes=duration):
            raise HTTPException(status_code=400, detail="El tiempo del torneo ha terminado")

    exercise = await database.db.exercises.find_one({"_id": ex_oid})
    if not exercise:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    test_cases = exercise.get("test_cases", [])
    if not test_cases:
        raise HTTPException(status_code=400, detail="El ejercicio no tiene casos de prueba")

    from app.routers.exercises import _run_with_judge0
    run_result = await _run_with_judge0(body.language, body.code, test_cases, exercise.get("compare_config"))

    passed = run_result.get("correct", False)
    elapsed = int((datetime.utcnow() - started_at).total_seconds()) if started_at else 0

    submission = {
        "email": email,
        "exercise_id": exercise_id,
        "score": exercise.get("difficulty", 800) if passed else 0,
        "time_seconds": elapsed,
        "submitted_at": datetime.utcnow(),
        "language": body.language,
        "passed": passed,
    }
    await database.db.tournaments.update_one(
        {"_id": oid},
        {"$push": {"submissions": submission}}
    )

    return {
        "passed": passed,
        "score": submission["score"],
        "message": run_result.get("message", ""),
        "failed_case": run_result.get("failed_case"),
        "time_seconds": elapsed,
    }


@router.post("/api/tournaments/{tournament_id}/finish")
async def finish_participation(
    tournament_id: str,
    email: str = Depends(get_current_user),
):
    """Mark the user as done (voluntary or anti-cheat on window blur)."""
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    tournament = await database.db.tournaments.find_one({"_id": oid})
    if not tournament:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    if tournament.get("status") != "active":
        raise HTTPException(status_code=400, detail="El torneo no está activo")
    if email not in tournament.get("participants", []):
        raise HTTPException(status_code=403, detail="No estás inscrito en este torneo")

    await database.db.tournaments.update_one(
        {"_id": oid},
        {"$addToSet": {"finished_participants": email}}
    )
    return {"message": "Torneo entregado. Tu puntuación ha sido registrada."}


@router.delete("/api/tournaments/{tournament_id}")
async def delete_tournament(tournament_id: str, admin: dict = Depends(require_admin)):
    try:
        oid = ObjectId(tournament_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    result = await database.db.tournaments.delete_one({"_id": oid})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Torneo no encontrado")
    return {"message": "Torneo eliminado."}
