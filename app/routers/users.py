import logging
import re
from datetime import datetime
from typing import Optional, List

import cloudinary.uploader
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form

import app.core.database as database
from app.core.security import get_current_user, verify_password, get_password_hash

logger = logging.getLogger(__name__)
router = APIRouter()

_USERNAME_RE = re.compile(r'^[a-zA-Z0-9_\-]{3,20}$')
_ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
_MAX_UPLOAD_BYTES = 1 * 1024 * 1024  # 1 MB


def _validate_username(username: str):
    if not _USERNAME_RE.match(username):
        raise HTTPException(
            status_code=400,
            detail="El username solo puede contener letras, números, guiones y guiones bajos (3-20 caracteres)."
        )


async def _validate_image(pfp: UploadFile):
    if pfp.content_type not in _ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG, PNG, WEBP o GIF.")
    contents = await pfp.read()
    if len(contents) > _MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="La imagen no puede superar los 5 MB.")
    # Reset file pointer for subsequent read by cloudinary
    import io
    pfp.file = io.BytesIO(contents)


@router.get("/api/user/me")
async def get_user_profile(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Calculate global rank based on elo
    elo = user.get("elo", 0)
    # Count how many users have strictly higher elo, plus 1 for current user's rank
    higher_elo_count = await database.db.users.count_documents({"elo": {"$gt": elo}})
    global_rank = higher_elo_count + 1

    def get_rank_info(e):
        if e <= 75:
            sub = min(3, max(1, (e // 26) + 1))
            return f"Bronce {['I', 'II', 'III'][sub-1]}", sub
        elif e <= 200:
            sub = min(3, max(1, ((e - 76) // 75) + 1))
            return f"Plata {['I', 'II', 'III'][sub-1]}", 3 + sub
        elif e <= 500:
            sub = min(3, max(1, ((e - 301) // 167) + 1))
            return f"Oro {['I', 'II', 'III'][sub-1]}", 6 + sub
        elif e <= 900:
            sub = min(3, max(1, ((e - 801) // 167) + 1))
            return f"Platino {['I', 'II', 'III'][sub-1]}", 9 + sub
        elif e <= 1400:
            sub = min(3, max(1, ((e - 1301) // 234) + 1))
            return f"Diamante {['I', 'II', 'III'][sub-1]}", 12 + sub
        elif e <= 2000:
            sub = min(3, max(1, ((e - 1301) // 234) + 1))
            return f"Elite {['I', 'II', 'III'][sub-1]}", 12 + sub
        elif e <= 3000:
            sub = min(3, max(1, ((e - 1301) // 234) + 1))
            return f"Campeon {['I', 'II', 'III'][sub-1]}", 12 + sub
        else:
            return "Voidborn", 16

    rank_name, tier = get_rank_info(elo)

    return {
        "email": user["email"],
        "username": user.get("username"),
        "avatar": user.get("avatar"),
        "is_onboarded": user.get("is_onboarded", False),
        "level": user.get("level"),
        "languages": user.get("languages", []),
        "description": user.get("description", ""),
        "elo": elo,
        "rank_name": rank_name,
        "tier": tier,
        "win_streak": user.get("win_streak", 0),
        "global_rank": global_rank,
        "wins": user.get("wins", 0),
        "matches_played": user.get("matches_played", 0),
        "coins": user.get("coins", 0),
        "equipped_frame": user.get("equipped_frame"),
        "profile_background": user.get("profile_background"),
        "purchased_items": user.get("purchased_items", []),
        "solved_count": len(user.get("solved_exercises", [])),
        "lang_stats": user.get("lang_stats", {}),
    }


@router.get("/api/user/check-username/{username}")
async def check_username_availability(username: str, email: str = Depends(get_current_user)):
    existing = await database.db.users.find_one({"username": username})
    return {"available": existing is None}


@router.post("/api/user/onboard")
async def onboard_user(
    username: str = Form(...),
    languages: List[str] = Form([]),
    level: str = Form(...),
    description: str = Form(""),
    pfp: UploadFile = File(None),
    email: str = Depends(get_current_user)
):
    _validate_username(username)

    # Check if username exists and doesn't belong to this exact user
    existing = await database.db.users.find_one({"username": username})
    if existing and existing.get("email") != email:
        raise HTTPException(status_code=400, detail="Este nombre de usuario ya está en uso.")

    avatar_url = None
    if pfp and pfp.filename:
        await _validate_image(pfp)
        try:
            # Clean string directly substituting @ and . to make it Cloudinary safe url
            safe_id = email.replace("@", "_at_").replace(".", "_")
            result = cloudinary.uploader.upload(
                pfp.file,
                folder="Codexar/ProfilePictures",
                public_id=safe_id,
                overwrite=True
            )
            avatar_url = result.get("secure_url")
        except Exception as e:
            logger.warning("Error uploading to Cloudinary: %s", str(e))
            raise HTTPException(status_code=500, detail="Error subiendo tu foto de perfil a The Matrix.")

    update_data = {
        "username": username,
        "languages": languages,
        "level": level,
        "description": description,
        "is_onboarded": True,
        "updated_at": datetime.utcnow()
    }

    if avatar_url:
        update_data["avatar"] = avatar_url
    else:
        # Avoid creating blank avatar logic if user doesn't update,
        # or we could keep the old one (which already happens automatically through set).
        pass

    await database.db.users.update_one(
        {"email": email},
        {"$set": update_data}
    )

    return {"status": "success", "username": username, "is_onboarded": True, "avatar": avatar_url}


@router.post("/api/user/verify-password")
async def verify_user_password(
    password: str = Form(...),
    email: str = Depends(get_current_user)
):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404)
    if verify_password(password, user["password"]):
        return {"valid": True}
    return {"valid": False}


@router.post("/api/user/profile/update")
async def update_user_profile(
    username: Optional[str] = Form(None),
    old_password: Optional[str] = Form(None),
    new_password: Optional[str] = Form(None),
    languages: List[str] = Form([]),
    description: Optional[str] = Form(None),
    pfp: UploadFile = File(None),
    email: str = Depends(get_current_user)
):
    current_user = await database.db.users.find_one({"email": email})
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    update_data = {"updated_at": datetime.utcnow()}

    # 1. Alias Validation
    if username is not None and username != current_user.get("username"):
        _validate_username(username)
        existing_username = await database.db.users.find_one({"username": username})
        if existing_username:
            raise HTTPException(status_code=400, detail="Este nombre de usuario ya está en uso.")
        update_data["username"] = username

    # 2. Cryptographic Mutator Validation
    if new_password:
        if not old_password:
            raise HTTPException(status_code=400, detail="Debes escribir tu contraseña actual para cambiarla.")
        if not verify_password(old_password, current_user["password"]):
            raise HTTPException(status_code=400, detail="La contraseña actual es incorrecta.")

        # Salt & Hash the mutation
        update_data["password"] = get_password_hash(new_password)

    # 3. Size constraints validation natively
    if description is not None:
        if len(description) > 30:
            raise HTTPException(status_code=400, detail="La biografía no puede superar los 30 caracteres.")
        update_data["description"] = description

    # 4. Array overwrites
    if languages:
        update_data["languages"] = languages

    # 5. Network Matrix Cloudinary Uplink
    if pfp and pfp.filename:
        await _validate_image(pfp)
        try:
            safe_id = email.replace("@", "_at_").replace(".", "_")
            result = cloudinary.uploader.upload(
                pfp.file,
                folder="Codexar/ProfilePictures",
                public_id=safe_id,
                overwrite=True
            )
            update_data["avatar"] = result.get("secure_url")
        except Exception as e:
            logger.warning("Cloudinary Overwrite Reject: %s", str(e))
            raise HTTPException(status_code=500, detail="Error transmitiendo la imagen al CDN global.")

    # Execute DB State Mutation
    await database.db.users.update_one(
        {"email": email},
        {"$set": update_data}
    )

    return {"status": "success", "message": "Perfil actualizado orbitalmente.", "avatar_updated": "avatar" in update_data}


@router.get("/api/user/stats")
async def get_user_stats(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    solved_ids = user.get("solved_exercises", [])
    if not solved_ids:
        return {"easy": 0, "medium": 0, "hard": 0, "total": 0}

    from bson import ObjectId
    valid_ids = []
    for sid in solved_ids:
        try:
            valid_ids.append(ObjectId(sid))
        except Exception:
            pass

    stats = {"easy": 0, "medium": 0, "hard": 0}

    # Pre-count total based purely on user array length (preserves history across re-seeds)
    stats["total"] = len(solved_ids)

    found_count = 0
    cursor = database.db.exercises.find({"_id": {"$in": valid_ids}}, {"difficulty": 1})
    async for ex in cursor:
        found_count += 1
        diff = ex.get("difficulty", "")
        if diff == "Fácil":
            stats["easy"] += 1
        elif diff == "Normal":
            stats["medium"] += 1
        elif diff == "Difícil":
            stats["hard"] += 1

    # Assign any missing ones to 'easy' so the pie chart adds up to total
    missing = stats["total"] - found_count
    if missing > 0:
        stats["easy"] += missing

    return stats


@router.get("/api/leaderboard")
async def get_leaderboard(email: str = Depends(get_current_user)):
    # Get top 5 users sorted by ELO descending
    cursor = database.db.users.find(
        {"elo": {"$exists": True}, "is_onboarded": True},
        {"username": 1, "avatar": 1, "languages": 1, "description": 1, "elo": 1, "solved_exercises": 1}
    ).sort("elo", -1).limit(5)

    users_list = []
    async for u in cursor:
        elo = u.get("elo", 0)

        # Calculate rank name for leaderboard
        if elo <= 75: sub = min(3, max(1, (elo // 26) + 1)); rank_name = f"Bronce {['I', 'II', 'III'][sub-1]}"
        elif elo <= 200: sub = min(3, max(1, ((elo - 76) // 75) + 1)); rank_name = f"Plata {['I', 'II', 'III'][sub-1]}"
        elif elo <= 500: sub = min(3, max(1, ((elo - 301) // 167) + 1)); rank_name = f"Oro {['I', 'II', 'III'][sub-1]}"
        elif elo <= 900: sub = min(3, max(1, ((elo - 801) // 167) + 1)); rank_name = f"Platino {['I', 'II', 'III'][sub-1]}"
        elif elo <= 1400: sub = min(3, max(1, ((elo - 801) // 167) + 1)); rank_name = f"Diamante {['I', 'II', 'III'][sub-1]}"
        elif elo <= 2000: sub = min(3, max(1, ((elo - 1301) // 234) + 1)); rank_name = f"Elite {['I', 'II', 'III'][sub-1]}"
        elif elo <= 3000: sub = min(3, max(1, ((elo - 801) // 167) + 1)); rank_name = f"Campeon {['I', 'II', 'III'][sub-1]}"
        else: rank_name = "Voidborn"

        users_list.append({
            "username": u.get("username", "?"),
            "avatar": u.get("avatar"),
            "languages": u.get("languages", []),
            "description": u.get("description", ""),
            "score": elo,
            "rank_name": rank_name,
            "solved": len(u.get("solved_exercises", []))
        })

    return users_list


@router.post("/api/user/heartbeat")
async def heartbeat(email: str = Depends(get_current_user)):
    await database.db.users.update_one(
        {"email": email},
        {"$set": {"last_seen": datetime.utcnow()}}
    )
    return {"ok": True}


@router.get("/api/user/profile/{username}")
async def get_public_profile(username: str, email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"username": username, "is_onboarded": True})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    elo = user.get("elo", 0)
    higher_elo_count = await database.db.users.count_documents({"elo": {"$gt": elo}})
    global_rank = higher_elo_count + 1

    def get_rank_info(e):
        if e <= 75:
            sub = min(3, max(1, (e // 26) + 1))
            return f"Bronce {['I', 'II', 'III'][sub-1]}", sub
        elif e <= 200:
            sub = min(3, max(1, ((e - 76) // 75) + 1))
            return f"Plata {['I', 'II', 'III'][sub-1]}", 3 + sub
        elif e <= 500:
            sub = min(3, max(1, ((e - 301) // 167) + 1))
            return f"Oro {['I', 'II', 'III'][sub-1]}", 6 + sub
        elif e <= 900:
            sub = min(3, max(1, ((e - 801) // 167) + 1))
            return f"Platino {['I', 'II', 'III'][sub-1]}", 9 + sub
        elif e <= 1400:
            sub = min(3, max(1, ((e - 1301) // 234) + 1))
            return f"Diamante {['I', 'II', 'III'][sub-1]}", 12 + sub
        elif e <= 2000:
            sub = min(3, max(1, ((e - 1301) // 234) + 1))
            return f"Elite {['I', 'II', 'III'][sub-1]}", 12 + sub
        elif e <= 3000:
            sub = min(3, max(1, ((e - 1301) // 234) + 1))
            return f"Campeon {['I', 'II', 'III'][sub-1]}", 12 + sub
        else:
            return "Voidborn", 16

    rank_name, tier = get_rank_info(elo)

    # Max ELO and max rank
    max_elo = user.get("max_elo", elo)
    max_rank_name, _ = get_rank_info(max_elo)

    # Win rate
    wins = user.get("wins", 0)
    matches_played = user.get("matches_played", 0)
    win_rate = round(wins / matches_played * 100) if matches_played > 0 else 0

    # Bot stats
    bot_wins = user.get("bot_wins", 0)
    bot_matches = user.get("bot_matches", 0)
    bot_winrate = round(bot_wins / bot_matches * 100) if bot_matches > 0 else 0

    # Solved by difficulty
    from bson import ObjectId
    DIFF_ORDER = ["Fácil", "Normal", "Difícil", "Muy Difícil", "Insane", "Abyssal"]
    solved_by_diff = {d: 0 for d in DIFF_ORDER}
    hardest_exercise = None
    solved_ids = user.get("solved_exercises", [])
    if solved_ids:
        oids = [ObjectId(i) for i in solved_ids if ObjectId.is_valid(i)]
        async for ex in database.db.exercises.find({"_id": {"$in": oids}}, {"title": 1, "difficulty": 1}):
            d = ex.get("difficulty", "Normal")
            if d in solved_by_diff:
                solved_by_diff[d] += 1
            if hardest_exercise is None or DIFF_ORDER.index(d) > DIFF_ORDER.index(hardest_exercise["difficulty"]):
                hardest_exercise = {"title": ex["title"], "difficulty": d}

    # Equipped achievements as full objects
    from app.routers.achievements import _CATALOG_MAP
    equipped_keys = user.get("equipped_achievements", [])
    equipped_details = [_CATALOG_MAP[k] for k in equipped_keys if k in _CATALOG_MAP]

    # Friendship status
    viewer = await database.db.users.find_one({"email": email})
    is_self = viewer["email"] == user["email"]
    is_friend = user["email"] in viewer.get("friends", [])
    request_sent = user["email"] in viewer.get("friend_requests_sent", [])
    request_received = user["email"] in viewer.get("friend_requests_received", [])

    return {
        "username": user.get("username"),
        "avatar": user.get("avatar"),
        "description": user.get("description", ""),
        "languages": user.get("languages", []),
        "elo": elo,
        "rank_name": rank_name,
        "tier": tier,
        "global_rank": global_rank,
        "wins": wins,
        "matches_played": matches_played,
        "win_rate": win_rate,
        "win_streak": user.get("win_streak", 0),
        "max_elo": max_elo,
        "max_rank_name": max_rank_name,
        "bot_wins": bot_wins,
        "bot_matches": bot_matches,
        "bot_winrate": bot_winrate,
        "bot_wins_by_diff": user.get("bot_wins_by_diff", {}),
        "bot_matches_by_diff": user.get("bot_matches_by_diff", {}),
        "solved_count": len(solved_ids),
        "solved_by_difficulty": solved_by_diff,
        "hardest_exercise": hardest_exercise,
        "equipped_achievements": equipped_details,
        "equipped_frame": user.get("equipped_frame"),
        "profile_background": user.get("profile_background"),
        "lang_stats": user.get("lang_stats", {}),
        "friendship_status": {
            "is_self": is_self,
            "is_friend": is_friend,
            "request_sent": request_sent,
            "request_received": request_received,
        },
    }


@router.post("/api/user/bot-result")
async def record_bot_result(body: dict, email: str = Depends(get_current_user)):
    won  = body.get("won", False)
    diff = body.get("difficulty", "normal")
    inc  = {"bot_matches": 1, f"bot_matches_by_diff.{diff}": 1}
    if won:
        inc["bot_wins"] = 1
        inc[f"bot_wins_by_diff.{diff}"] = 1
    await database.db.users.update_one({"email": email}, {"$inc": inc})
    return {"ok": True}


@router.post("/api/user/upload-background")
async def upload_profile_background(
    bg: UploadFile = File(...),
    email: str = Depends(get_current_user)
):
    await _validate_image(bg)
    try:
        safe_id = email.replace("@", "_at_").replace(".", "_") + "_bg"
        result = cloudinary.uploader.upload(
            bg.file,
            folder="Codexar/ProfileBackgrounds",
            public_id=safe_id,
            overwrite=True,
            resource_type="auto"
        )
        bg_url = result.get("secure_url")
        await database.db.users.update_one(
            {"email": email},
            {"$set": {"profile_background": bg_url}}
        )
        return {"status": "success", "url": bg_url}
    except Exception as e:
        logger.warning("Background upload error: %s", str(e))
        raise HTTPException(status_code=500, detail="Error subiendo el fondo de perfil")
