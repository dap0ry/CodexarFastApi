from datetime import datetime
from typing import Optional, List

import cloudinary.uploader
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form

import app.core.database as database
from app.core.security import get_current_user, verify_password, get_password_hash

router = APIRouter()


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
        elif e <= 300:
            sub = min(3, max(1, ((e - 76) // 75) + 1))
            return f"Plata {['I', 'II', 'III'][sub-1]}", 3 + sub
        elif e <= 800:
            sub = min(3, max(1, ((e - 301) // 167) + 1))
            return f"Oro {['I', 'II', 'III'][sub-1]}", 6 + sub
        elif e <= 1300:
            sub = min(3, max(1, ((e - 801) // 167) + 1))
            return f"Platino {['I', 'II', 'III'][sub-1]}", 9 + sub
        elif e <= 2000:
            sub = min(3, max(1, ((e - 1301) // 234) + 1))
            return f"Diamante {['I', 'II', 'III'][sub-1]}", 12 + sub
        else:
            return "Campeón", 16

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
        "matches_played": user.get("matches_played", 0)
    }


@router.get("/api/user/check-username/{username}")
async def check_username_availability(username: str):
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
    # Check if username exists and doesn't belong to this exact user
    existing = await database.db.users.find_one({"username": username})
    if existing and existing.get("email") != email:
        raise HTTPException(status_code=400, detail="Este nombre de usuario ya está en uso.")

    avatar_url = None
    if pfp and pfp.filename:
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
            print("Error uploading to Cloudinary:", str(e))
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
            print("Cloudinary Overwrite Reject:", str(e))
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
        elif elo <= 300: sub = min(3, max(1, ((elo - 76) // 75) + 1)); rank_name = f"Plata {['I', 'II', 'III'][sub-1]}"
        elif elo <= 800: sub = min(3, max(1, ((elo - 301) // 167) + 1)); rank_name = f"Oro {['I', 'II', 'III'][sub-1]}"
        elif elo <= 1300: sub = min(3, max(1, ((elo - 801) // 167) + 1)); rank_name = f"Platino {['I', 'II', 'III'][sub-1]}"
        elif elo <= 2000: sub = min(3, max(1, ((elo - 1301) // 234) + 1)); rank_name = f"Diamante {['I', 'II', 'III'][sub-1]}"
        else: rank_name = "Campeón"

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


@router.get("/api/story/chapters")
async def get_story_chapters(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    solved_ids = set(user.get("solved_exercises", [])) if user else set()

    # Fetch all exercises to get their true ObjectIds
    cursor = database.db.exercises.find({}, {"title": 1, "difficulty": 1, "category": 1})
    db_exercises = {}
    async for ex in cursor:
        db_exercises[ex["title"]] = {
            "id": str(ex["_id"]),
            "title": ex["title"],
            "difficulty": ex.get("difficulty", "Normal"),
            "category": ex.get("category", "")
        }

    from app.exercises_data import EXERCISES_SEED

    chapter_meta = [
        {"title": "Capítulo 1: Fundamentos de Arrays", "desc": "Estructuras contiguas en memoria."},
        {"title": "Capítulo 2: Algoritmos con Arrays", "desc": "Problemas de nivel competitivo."},
        {"title": "Capítulo 3: Tratamiento de Strings", "desc": "Manipulación de cadenas y texto."},
        {"title": "Capítulo 4: Strings Avanzados", "desc": "Algoritmos complejos sobre cadenas."},
        {"title": "Capítulo 5: Matemáticas Básicas", "desc": "Fibonacci, Primos y Factoriales."},
        {"title": "Capítulo 6: Teoría de Números", "desc": "Rompecabezas matemáticos extremos."}
    ]

    chapters = []
    chunk_size = 5
    previous_unlocked = True  # Chapter 1 is always unlocked

    for i in range(6):
        start_idx = i * chunk_size
        chunk = EXERCISES_SEED[start_idx: start_idx + chunk_size]

        ex_list = []
        solved_count = 0

        for seed_ex in chunk:
            # Match with DB data to get real ID
            db_ex = db_exercises.get(seed_ex["title"])
            if not db_ex: continue

            is_solved = db_ex["id"] in solved_ids
            if is_solved:
                solved_count += 1

            ex_list.append({
                "id": db_ex["id"],
                "title": db_ex["title"],
                "difficulty": db_ex["difficulty"],
                "solved": is_solved
            })

        is_unlocked = previous_unlocked
        # Next chapter is unlocked only if this chapter has 5/5
        previous_unlocked = (solved_count == chunk_size)

        chapters.append({
            "id": i + 1,
            "title": chapter_meta[i]["title"],
            "description": chapter_meta[i]["desc"],
            "is_unlocked": is_unlocked,
            "progress": solved_count,
            "total": chunk_size,
            "exercises": ex_list
        })

    return chapters
