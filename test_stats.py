import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def main():
    client = AsyncIOMotorClient("mongodb+srv://Codexar:Codexar@codexar.z924g.mongodb.net/?retryWrites=true&w=majority&appName=Codexar")
    db = client["Codexar"]
    user = await db.users.find_one({"email": "ejemplo5@gmail.com"})
    print("User DAPORY email:", user["email"])
    print("User DAPORY solved_exercises array size:", len(user.get("solved_exercises", [])))
    print("User DAPORY solved_exercises array:", user.get("solved_exercises", []))
    
    # check valid ids loop
    solved_ids = user.get("solved_exercises", [])
    from bson import ObjectId
    valid_ids = []
    for sid in solved_ids:
        try:
            valid_ids.append(ObjectId(sid))
            print(f"ID {sid} is valid ObjectId")
        except Exception as e:
            print(f"ID {sid} is INVALID: {e}")
            
    # count
    stats = {"easy": 0, "medium": 0, "hard": 0}
    stats["total"] = len(solved_ids)
    
    found_count = 0
    cursor = db.exercises.find({"_id": {"$in": valid_ids}}, {"difficulty": 1})
    async for ex in cursor:
        print("Found exercise:", ex)
        found_count += 1
        
    print("Found Count:", found_count)
    missing = stats["total"] - found_count
    print("Missing Count:", missing)

asyncio.run(main())
