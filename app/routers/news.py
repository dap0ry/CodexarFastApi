import re
from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

import app.core.database as database
from app.core.security import get_current_user

router = APIRouter(prefix="/api/news", tags=["news"])


# ── Helpers ────────────────────────────────────────────────────────────────────

def _oid(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    return doc


async def _get_user(email: str) -> dict:
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


async def _resolve_mentions(body: str) -> list[str]:
    """Return list of valid usernames mentioned with @ in body."""
    raw = re.findall(r"@(\w+)", body)
    if not raw:
        return []
    users = await database.db.users.find(
        {"username": {"$in": raw}},
        {"username": 1}
    ).to_list(length=None)
    return [u["username"] for u in users]


# ── Schemas ────────────────────────────────────────────────────────────────────

class NewsCreate(BaseModel):
    title: str
    subtitle: str
    body: str


# ── Endpoints ──────────────────────────────────────────────────────────────────

@router.get("/")
async def list_news(email: str = Depends(get_current_user)):
    user = await _get_user(email)
    cursor = database.db.news.find({}).sort("created_at", -1)
    docs = await cursor.to_list(length=50)
    result = []
    for doc in docs:
        doc = _oid(doc)
        doc["like_count"] = len(doc.get("likes", []))
        doc["liked_by_me"] = user["username"] in doc.get("likes", [])
        doc.pop("likes", None)
        result.append(doc)
    return result


@router.post("/")
async def create_news(payload: NewsCreate, email: str = Depends(get_current_user)):
    user = await _get_user(email)
    mentions = await _resolve_mentions(payload.body)
    doc = {
        "title": payload.title.strip(),
        "subtitle": payload.subtitle.strip(),
        "creator": user["username"],
        "body": payload.body.strip(),
        "mentions": mentions,
        "likes": [],
        "created_at": datetime.utcnow(),
    }
    result = await database.db.news.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    doc.pop("_id", None)
    doc["like_count"] = 0
    doc["liked_by_me"] = False
    doc.pop("likes", None)
    return doc


@router.post("/{news_id}/like")
async def toggle_like(news_id: str, email: str = Depends(get_current_user)):
    user = await _get_user(email)
    try:
        oid = ObjectId(news_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de noticia inválido")

    news = await database.db.news.find_one({"_id": oid})
    if not news:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    username = user["username"]
    likes: list = news.get("likes", [])

    if username in likes:
        likes.remove(username)
        liked = False
    else:
        likes.append(username)
        liked = True

    await database.db.news.update_one({"_id": oid}, {"$set": {"likes": likes}})
    return {"liked": liked, "like_count": len(likes)}
