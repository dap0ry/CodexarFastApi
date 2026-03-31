from fastapi import APIRouter, HTTPException, Depends

import app.core.database as database
from app.core.security import get_current_user

router = APIRouter()

# ── Store catalog ─────────────────────────────────────────────────────────────
STORE_CATALOG = [
    # ── Marcos (frames) ──
    {
        "id": "frame_silver",
        "name": "Marco Plateado",
        "description": "Borde plateado con brillo sutil",
        "type": "frame",
        "price": 150,
    },
    {
        "id": "frame_cyan",
        "name": "Marco Neón Cyan",
        "description": "Marco con resplandor ciberpunk",
        "type": "frame",
        "price": 300,
    },
    {
        "id": "frame_gold",
        "name": "Marco Dorado",
        "description": "Prestigioso marco para campeones",
        "type": "frame",
        "price": 500,
    },
    {
        "id": "frame_fire",
        "name": "Marco Fuego",
        "description": "Marco con efecto de llamas pulsantes",
        "type": "frame",
        "price": 800,
    },
    {
        "id": "frame_rainbow",
        "name": "Marco Arcoíris",
        "description": "Marco con gradiente animado multicolor",
        "type": "frame",
        "price": 1200,
    },
    # ── Fondos ──
    {
        "id": "bg_void",
        "name": "Fondo Vacío Oscuro",
        "description": "Fondo oscuro profundo para tu perfil",
        "type": "background",
        "price": 200,
    },
    {
        "id": "bg_matrix",
        "name": "Fondo Matrix",
        "description": "Lluvia de código verde al estilo Matrix",
        "type": "background",
        "price": 400,
    },
    {
        "id": "bg_aurora",
        "name": "Fondo Aurora Boreal",
        "description": "Auroras boreales animadas",
        "type": "background",
        "price": 600,
    },
    {
        "id": "bg_cyber",
        "name": "Fondo Cyberpunk",
        "description": "Gradiente morado/cyan de ciudad futurista",
        "type": "background",
        "price": 500,
    },
    # ── Mejoras ──
    {
        "id": "extra_badge_slot",
        "name": "Ranura Extra de Logro",
        "description": "Equipa hasta 4 logros en tu perfil (en vez de 3)",
        "type": "upgrade",
        "price": 1500,
    },
    {
        "id": "extended_bio",
        "name": "Biografía Extendida",
        "description": "Amplía tu bio hasta 60 caracteres",
        "type": "upgrade",
        "price": 500,
    },
]

CATALOG_BY_ID = {item["id"]: item for item in STORE_CATALOG}


@router.get("/api/store/items")
async def get_store_items(email: str = Depends(get_current_user)):
    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    purchased = set(user.get("purchased_items", []))
    equipped_frame = user.get("equipped_frame")
    profile_background = user.get("profile_background")
    coins = user.get("coins", 0)

    items = []
    for item in STORE_CATALOG:
        owned = item["id"] in purchased
        equipped = (
            (item["type"] == "frame" and equipped_frame == item["id"]) or
            (item["type"] == "background" and profile_background == item["id"]) or
            (item["type"] == "upgrade" and owned)
        )
        items.append({**item, "owned": owned, "equipped": equipped})

    return {"items": items, "coins": coins}


@router.post("/api/store/buy/{item_id}")
async def buy_item(item_id: str, email: str = Depends(get_current_user)):
    item = CATALOG_BY_ID.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    purchased = set(user.get("purchased_items", []))
    if item_id in purchased:
        raise HTTPException(status_code=400, detail="Ya tienes este artículo")

    coins = user.get("coins", 0)
    if coins < item["price"]:
        raise HTTPException(status_code=400, detail="Monedas insuficientes")

    await database.db.users.update_one(
        {"email": email},
        {
            "$inc": {"coins": -item["price"]},
            "$addToSet": {"purchased_items": item_id},
        }
    )
    return {"status": "success", "message": f"¡{item['name']} comprado!", "coins_left": coins - item["price"]}


@router.post("/api/store/equip/{item_id}")
async def equip_item(item_id: str, email: str = Depends(get_current_user)):
    item = CATALOG_BY_ID.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")

    user = await database.db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    purchased = set(user.get("purchased_items", []))
    if item_id not in purchased:
        raise HTTPException(status_code=403, detail="No tienes este artículo")

    if item["type"] == "frame":
        await database.db.users.update_one({"email": email}, {"$set": {"equipped_frame": item_id}})
    elif item["type"] == "background":
        await database.db.users.update_one({"email": email}, {"$set": {"profile_background": item_id}})

    return {"status": "success", "message": f"¡{item['name']} equipado!"}


@router.post("/api/store/unequip/{item_type}")
async def unequip_item(item_type: str, email: str = Depends(get_current_user)):
    if item_type not in ("frame", "background"):
        raise HTTPException(status_code=400, detail="Tipo inválido")

    field = "equipped_frame" if item_type == "frame" else "profile_background"
    await database.db.users.update_one({"email": email}, {"$unset": {field: ""}})
    return {"status": "success"}
