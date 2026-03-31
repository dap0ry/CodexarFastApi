from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends

import app.core.database as database
from app.core.security import get_current_user

router = APIRouter()


@router.get("/api/friends/search")
async def search_friends(q: str, email: str = Depends(get_current_user)):
    if not q or len(q) < 1:
        return []
    current_user = await database.db.users.find_one({"email": email})
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    friends = current_user.get("friends", [])
    sent = current_user.get("friend_requests_sent", [])
    received = current_user.get("friend_requests_received", [])

    exclude_emails = [email] + friends + sent + received

    cursor = database.db.users.find({
        "username": {"$regex": q, "$options": "i"},
        "email": {"$nin": exclude_emails}
    }).limit(5)

    results = []
    async for user in cursor:
        results.append({
            "username": user.get("username"),
            "avatar": user.get("avatar"),
            "level": user.get("level"),
            "languages": user.get("languages", []),
            "description": user.get("description", "")
        })
    return results


@router.post("/api/friends/request/{target_username}")
async def send_friend_request(target_username: str, email: str = Depends(get_current_user)):
    target_user = await database.db.users.find_one({"username": target_username})
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario objetivo no encontrado")
    target_email = target_user["email"]
    if target_email == email:
        raise HTTPException(status_code=400, detail="No puedes enviarte una solicitud a ti mismo")

    await database.db.users.update_one(
        {"email": email},
        {"$addToSet": {"friend_requests_sent": target_email}}
    )
    await database.db.users.update_one(
        {"email": target_email},
        {"$addToSet": {"friend_requests_received": email}}
    )
    return {"status": "success", "message": "Solicitud enviada"}


@router.post("/api/friends/accept/{target_username}")
async def accept_friend_request(target_username: str, email: str = Depends(get_current_user)):
    target_user = await database.db.users.find_one({"username": target_username})
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario objetivo no encontrado")
    target_email = target_user["email"]

    current_user = await database.db.users.find_one({"email": email})
    if target_email not in current_user.get("friend_requests_received", []):
        raise HTTPException(status_code=400, detail="No hay solicitud pendiente del usuario")

    await database.db.users.update_one(
        {"email": email},
        {
            "$addToSet": {"friends": target_email},
            "$pull": {"friend_requests_received": target_email}
        }
    )
    await database.db.users.update_one(
        {"email": target_email},
        {
            "$addToSet": {"friends": email},
            "$pull": {"friend_requests_sent": email}
        }
    )
    return {"status": "success", "message": "Solicitud aceptada"}


@router.post("/api/friends/reject/{target_username}")
async def reject_friend_request(target_username: str, email: str = Depends(get_current_user)):
    target_user = await database.db.users.find_one({"username": target_username})
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario objetivo no encontrado")
    target_email = target_user["email"]

    await database.db.users.update_one(
        {"email": email},
        {"$pull": {"friend_requests_received": target_email}}
    )
    await database.db.users.update_one(
        {"email": target_email},
        {"$pull": {"friend_requests_sent": email}}
    )
    return {"status": "success", "message": "Solicitud rechazada"}


@router.post("/api/friends/cancel/{target_username}")
async def cancel_friend_request(target_username: str, email: str = Depends(get_current_user)):
    target_user = await database.db.users.find_one({"username": target_username})
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario objetivo no encontrado")
    target_email = target_user["email"]

    await database.db.users.update_one(
        {"email": email},
        {"$pull": {"friend_requests_sent": target_email}}
    )
    await database.db.users.update_one(
        {"email": target_email},
        {"$pull": {"friend_requests_received": email}}
    )
    return {"status": "success", "message": "Solicitud cancelada"}


@router.get("/api/friends")
async def get_friends_lists(email: str = Depends(get_current_user)):
    current_user = await database.db.users.find_one({"email": email})
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    friends_emails = current_user.get("friends", [])
    sent_emails = current_user.get("friend_requests_sent", [])
    received_emails = current_user.get("friend_requests_received", [])

    def relative_time(dt):
        if dt is None:
            return "Nunca conectado"
        diff = (datetime.utcnow() - dt).total_seconds()
        if diff < 120:      return "En línea"
        if diff < 3600:     return f"hace {int(diff // 60)} min"
        if diff < 86400:    return f"hace {int(diff // 3600)} h"
        if diff < 604800:   return f"hace {int(diff // 86400)} días"
        if diff < 2592000:  return f"hace {int(diff // 604800)} semanas"
        return f"hace {int(diff // 2592000)} meses"

    async def get_users_info(email_list):
        if not email_list:
            return []
        cursor = database.db.users.find({"email": {"$in": email_list}})
        users_arr = []
        async for u in cursor:
            last_seen = u.get("last_seen")
            is_online = last_seen is not None and (datetime.utcnow() - last_seen).total_seconds() < 120
            users_arr.append({
                "username": u.get("username"),
                "avatar": u.get("avatar"),
                "level": u.get("level"),
                "languages": u.get("languages", []),
                "description": u.get("description", ""),
                "is_online": is_online,
                "last_seen_text": relative_time(last_seen)
            })
        return users_arr

    return {
        "friends": await get_users_info(friends_emails),
        "sent": await get_users_info(sent_emails),
        "received": await get_users_info(received_emails)
    }


@router.delete("/api/friends/{target_username}")
async def remove_friend(target_username: str, email: str = Depends(get_current_user)):
    target_user = await database.db.users.find_one({"username": target_username})
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    target_email = target_user["email"]

    current_user = await database.db.users.find_one({"email": email})
    if target_email not in current_user.get("friends", []):
        raise HTTPException(status_code=400, detail="Este usuario no es tu amigo")

    await database.db.users.update_one(
        {"email": email},
        {"$pull": {"friends": target_email}}
    )
    await database.db.users.update_one(
        {"email": target_email},
        {"$pull": {"friends": email}}
    )
    return {"status": "success", "message": "Amistad eliminada"}


@router.get("/api/friends/activity")
async def get_activity_feed(email: str = Depends(get_current_user)):
    # Currently no activity data
    return []
