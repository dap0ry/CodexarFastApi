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
    # Inject / update exercises without changing their _id values
    from app.exercises_data import EXERCISES_SEED
    existing_count = await db.exercises.count_documents({})

    if existing_count == 0:
        # Fresh start: insert all
        await db.exercises.insert_many(EXERCISES_SEED)
        print(f"\u2705 Injected {len(EXERCISES_SEED)} offline mode exercises into MongoDB.")
    else:
        # Update existing exercises in-place by title (preserves _id so user progress is kept)
        updated = 0
        inserted = 0
        sample = await db.exercises.find_one({})
        if sample and "test_cases" not in sample:
            # Missing test_cases on all docs: update each by title
            for seed_ex in EXERCISES_SEED:
                result = await db.exercises.update_one(
                    {"title": seed_ex["title"]},
                    {"$set": {
                        "description": seed_ex.get("description", ""),
                        "test_cases": seed_ex.get("test_cases", []),
                        "stub": seed_ex.get("stub", {})
                    }},
                    upsert=True
                )
                if result.upserted_id:
                    inserted += 1
                else:
                    updated += 1
            print(f"\u2705 Updated {updated} exercises with test cases, inserted {inserted} new.")
        else:
            print(f"\u2705 Exercises collection OK ({existing_count} exercises).")


async def shutdown_db_client():
    client.close()
    print("❌ Disconnected from MongoDB Atlas.")
