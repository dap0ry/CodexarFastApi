import logging
from datetime import datetime

from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGODB_URI, DB_NAME

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient = None
db = None


async def startup_db_client():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    logger.info(f"Connected to MongoDB Atlas -> Database: {DB_NAME}")
    # TTL indexes: MongoDB auto-deletes expired docs
    await db.email_verifications.create_index("expires_at", expireAfterSeconds=0)
    await db.revoked_tokens.create_index("expires_at", expireAfterSeconds=0)
    # Sync exercises: upsert by title, remove stale titles not in seed
    from app.exercises_data import EXERCISES_SEED
    seed_titles = {ex["title"] for ex in EXERCISES_SEED}

    # Remove exercises whose title is no longer in the seed
    del_result = await db.exercises.delete_many({"title": {"$nin": list(seed_titles)}})
    if del_result.deleted_count:
        logger.info(f"Removed {del_result.deleted_count} stale exercises.")

    # Upsert every seed exercise by title (preserves _id and solver stats for existing ones)
    updated = inserted = 0
    for seed_ex in EXERCISES_SEED:
        set_doc = {
            "description":       seed_ex.get("description", ""),
            "difficulty":        seed_ex.get("difficulty", "Normal"),
            "category":          seed_ex.get("category", ""),
            "test_cases":        seed_ex.get("test_cases", []),
            "stub":              seed_ex.get("stub", {}),
        }
        if "title_i18n" in seed_ex:
            set_doc["title_i18n"] = seed_ex["title_i18n"]
        if "description_i18n" in seed_ex:
            set_doc["description_i18n"] = seed_ex["description_i18n"]
        result = await db.exercises.update_one(
            {"title": seed_ex["title"]},
            {"$set": set_doc},
            upsert=True
        )
        if result.upserted_id:
            inserted += 1
        else:
            updated += 1
    logger.info(f"Exercises synced: {inserted} inserted, {updated} updated.")

    # Seed example news (only once — skip if any news already exists)
    if await db.news.count_documents({}) == 0:
        example_news = {
            "title": "Los Equipos llegan a Codexar",
            "subtitle": "Una nueva era de competición colaborativa está por comenzar",
            "creator": "Codexar",
            "body": (
                "Desde el equipo de desarrollo de Codexar queremos anunciar que muy pronto "
                "estaremos lanzando el sistema de Equipos. Podrás crear o unirte a un equipo, "
                "competir de forma grupal, acumular puntos colectivos y escalar en una tabla de "
                "clasificación por equipos separada del ranking individual.\n\n"
                "Esto abre la puerta a torneos entre escuadras, estrategias coordinadas y una "
                "dimensión completamente nueva dentro de la plataforma.\n\n"
                "Shoutout especial a @ABGS, uno de los primeros en creer en este proyecto desde "
                "el día cero — ¡prepárate para liderar tu equipo cuando esto salga! "
                "¿Ya tienes nombre pensado? Déjalo en los comentarios... cuando los comentarios "
                "también lleguen 😄\n\n"
                "Estad atentos. El anuncio oficial está cerca."
            ),
            "mentions": ["ABGS"],
            "likes": [],
            "created_at": datetime.utcnow(),
        }
        await db.news.insert_one(example_news)
        logger.info("Seeded example news document.")


async def shutdown_db_client():
    client.close()
    logger.info("Disconnected from MongoDB Atlas.")
