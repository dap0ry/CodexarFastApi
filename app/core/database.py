from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGODB_URI, DB_NAME

client: AsyncIOMotorClient = None
db = None


async def startup_db_client():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    print(f"✅ Connected to MongoDB Atlas -> Database: {DB_NAME}")
    # TTL indexes: MongoDB auto-deletes expired docs
    await db.email_verifications.create_index("expires_at", expireAfterSeconds=0)
    await db.revoked_tokens.create_index("expires_at", expireAfterSeconds=0)
    # Sync exercises: upsert by title, remove stale titles not in seed
    from app.exercises_data import EXERCISES_SEED
    seed_titles = {ex["title"] for ex in EXERCISES_SEED}

    # Remove exercises whose title is no longer in the seed
    del_result = await db.exercises.delete_many({"title": {"$nin": list(seed_titles)}})
    if del_result.deleted_count:
        print(f"🗑  Removed {del_result.deleted_count} stale exercises.")

    # Upsert every seed exercise by title (preserves _id and solver stats for existing ones)
    updated = inserted = 0
    for seed_ex in EXERCISES_SEED:
        result = await db.exercises.update_one(
            {"title": seed_ex["title"]},
            {"$set": {
                "description":  seed_ex.get("description", ""),
                "difficulty":   seed_ex.get("difficulty", "Normal"),
                "category":     seed_ex.get("category", ""),
                "test_cases":   seed_ex.get("test_cases", []),
                "stub":         seed_ex.get("stub", {}),
            }},
            upsert=True
        )
        if result.upserted_id:
            inserted += 1
        else:
            updated += 1
    print(f"✅ Exercises synced: {inserted} inserted, {updated} updated.")


async def shutdown_db_client():
    client.close()
    print("❌ Disconnected from MongoDB Atlas.")
