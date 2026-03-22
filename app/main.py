import os
import ast
import sys
import io
from datetime import datetime, timedelta
from typing import Optional, List, Any

from fastapi import FastAPI, HTTPException, status, Depends, Header, UploadFile, File, Form
import cloudinary
import cloudinary.uploader
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import bcrypt
from jose import JWTError, jwt
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
JWT_SECRET = os.getenv("JWT_SECRET", "default_secret_key_change_me")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

if CLOUDINARY_CLOUD_NAME and CLOUDINARY_API_KEY:
    cloudinary.config(
        cloud_name=CLOUDINARY_CLOUD_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET
    )

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
DB_NAME = "Codexar"

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not set in environment variables. Please check your .env file.")

app = FastAPI(title="Codexar Auth API")

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Codexar API is running"}

# Setup CORS to allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev only.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
client: AsyncIOMotorClient = None
db = None

@app.on_event("startup")
async def startup_db_client():
    global client, db
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    print(f"✅ Connected to MongoDB Atlas -> Database: {DB_NAME}")
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

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
    print("❌ Disconnected from MongoDB Atlas.")

# Models
class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    username: Optional[str] = None
    is_onboarded: bool

class OnboardData(BaseModel):
    username: str
    languages: List[str]
    level: str
    description: str

# Helper Functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(authorization: str = Header(...)):
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise ValueError()
        return email
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

# ====== Routes ======

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "Codexar API is running"}

@app.post("/api/auth/register", response_model=Token)
async def register_user(user: UserRegister):
    existing_user = await db.users.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error: El email ya está registrado."
        )
    
    hashed_password = get_password_hash(user.password)
    user_dict = {
        "email": user.email,
        "password": hashed_password,
        "created_at": datetime.utcnow(),
        "is_onboarded": False,
        "elo": 0,
        "win_streak": 0
    }
    
    await db.users.insert_one(user_dict)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer", "username": None, "is_onboarded": False}

@app.post("/api/auth/login", response_model=Token)
async def login_user(user: UserLogin):
    db_user = await db.users.find_one({"email": user.email})
    
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user["email"]}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "username": db_user.get("username"),
        "is_onboarded": db_user.get("is_onboarded", False)
    }

@app.get("/api/user/me")
async def get_user_profile(email: str = Depends(get_current_user)):
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    
    # Calculate global rank based on elo
    elo = user.get("elo", 0)
    # Count how many users have strictly higher elo, plus 1 for current user's rank
    higher_elo_count = await db.users.count_documents({"elo": {"$gt": elo}})
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

@app.get("/api/user/check-username/{username}")
async def check_username_availability(username: str):
    existing = await db.users.find_one({"username": username})
    return {"available": existing is None}

@app.post("/api/user/onboard")
async def onboard_user(
    username: str = Form(...),
    languages: List[str] = Form([]),
    level: str = Form(...),
    description: str = Form(""),
    pfp: UploadFile = File(None),
    email: str = Depends(get_current_user)
):
    # Check if username exists and doesn't belong to this exact user
    existing = await db.users.find_one({"username": username})
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

    await db.users.update_one(
        {"email": email},
        {"$set": update_data}
    )
    
    return {"status": "success", "username": username, "is_onboarded": True, "avatar": avatar_url}

# ====== Friends Routes ======

@app.get("/api/friends/search")
async def search_friends(q: str, email: str = Depends(get_current_user)):
    if not q or len(q) < 1:
        return []
    current_user = await db.users.find_one({"email": email})
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    friends = current_user.get("friends", [])
    sent = current_user.get("friend_requests_sent", [])
    received = current_user.get("friend_requests_received", [])
    
    exclude_emails = [email] + friends + sent + received
    
    cursor = db.users.find({
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

@app.post("/api/friends/request/{target_username}")
async def send_friend_request(target_username: str, email: str = Depends(get_current_user)):
    target_user = await db.users.find_one({"username": target_username})
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario objetivo no encontrado")
    target_email = target_user["email"]
    if target_email == email:
        raise HTTPException(status_code=400, detail="No puedes enviarte una solicitud a ti mismo")
        
    await db.users.update_one(
        {"email": email},
        {"$addToSet": {"friend_requests_sent": target_email}}
    )
    await db.users.update_one(
        {"email": target_email},
        {"$addToSet": {"friend_requests_received": email}}
    )
    return {"status": "success", "message": "Solicitud enviada"}

@app.post("/api/friends/accept/{target_username}")
async def accept_friend_request(target_username: str, email: str = Depends(get_current_user)):
    target_user = await db.users.find_one({"username": target_username})
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario objetivo no encontrado")
    target_email = target_user["email"]
    
    current_user = await db.users.find_one({"email": email})
    if target_email not in current_user.get("friend_requests_received", []):
        raise HTTPException(status_code=400, detail="No hay solicitud pendiente del usuario")
        
    await db.users.update_one(
        {"email": email},
        {
            "$addToSet": {"friends": target_email},
            "$pull": {"friend_requests_received": target_email}
        }
    )
    await db.users.update_one(
        {"email": target_email},
        {
            "$addToSet": {"friends": email},
            "$pull": {"friend_requests_sent": email}
        }
    )
    return {"status": "success", "message": "Solicitud aceptada"}

@app.post("/api/friends/reject/{target_username}")
async def reject_friend_request(target_username: str, email: str = Depends(get_current_user)):
    target_user = await db.users.find_one({"username": target_username})
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario objetivo no encontrado")
    target_email = target_user["email"]
    
    await db.users.update_one(
        {"email": email},
        {"$pull": {"friend_requests_received": target_email}}
    )
    await db.users.update_one(
        {"email": target_email},
        {"$pull": {"friend_requests_sent": email}}
    )
    return {"status": "success", "message": "Solicitud rechazada"}

@app.post("/api/friends/cancel/{target_username}")
async def cancel_friend_request(target_username: str, email: str = Depends(get_current_user)):
    target_user = await db.users.find_one({"username": target_username})
    if not target_user:
        raise HTTPException(status_code=404, detail="Usuario objetivo no encontrado")
    target_email = target_user["email"]
    
    await db.users.update_one(
        {"email": email},
        {"$pull": {"friend_requests_sent": target_email}}
    )
    await db.users.update_one(
        {"email": target_email},
        {"$pull": {"friend_requests_received": email}}
    )
    return {"status": "success", "message": "Solicitud cancelada"}

@app.get("/api/friends")
async def get_friends_lists(email: str = Depends(get_current_user)):
    current_user = await db.users.find_one({"email": email})
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    friends_emails = current_user.get("friends", [])
    sent_emails = current_user.get("friend_requests_sent", [])
    received_emails = current_user.get("friend_requests_received", [])
    
    async def get_users_info(email_list):
        if not email_list:
            return []
        cursor = db.users.find({"email": {"$in": email_list}})
        users_arr = []
        async for u in cursor:
            users_arr.append({
                "username": u.get("username"),
                "avatar": u.get("avatar"),
                "level": u.get("level"),
                "languages": u.get("languages", []),
                "description": u.get("description", ""),
                "is_online": True # Mock connection status
            })
        return users_arr
        
    return {
        "friends": await get_users_info(friends_emails),
        "sent": await get_users_info(sent_emails),
        "received": await get_users_info(received_emails)
    }

@app.get("/api/friends/activity")
async def get_activity_feed(email: str = Depends(get_current_user)):
    # Currently no activity data
    return []

# ====== Profile Management Route ======

@app.post("/api/user/verify-password")
async def verify_user_password(
    password: str = Form(...),
    email: str = Depends(get_current_user)
):
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404)
    if verify_password(password, user["password"]):
        return {"valid": True}
    return {"valid": False}

@app.post("/api/user/profile/update")
async def update_user_profile(
    username: Optional[str] = Form(None),
    old_password: Optional[str] = Form(None),
    new_password: Optional[str] = Form(None),
    languages: List[str] = Form([]),
    description: Optional[str] = Form(None),
    pfp: UploadFile = File(None),
    email: str = Depends(get_current_user)
):
    current_user = await db.users.find_one({"email": email})
    if not current_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado.")

    update_data = {"updated_at": datetime.utcnow()}

    # 1. Alias Validation
    if username is not None and username != current_user.get("username"):
        existing_username = await db.users.find_one({"username": username})
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
    await db.users.update_one(
        {"email": email},
        {"$set": update_data}
    )

    return {"status": "success", "message": "Perfil actualizado orbitalmente.", "avatar_updated": "avatar" in update_data}

# --- EXERCISES ---

class SolveRequest(BaseModel):
    code: str
    language: str
    save: bool = False

@app.get("/api/exercises")
async def get_exercises(email: str = Depends(get_current_user)):
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    solved_ids = set(user.get("solved_exercises", []))
    friends_emails = set(user.get("friends", []))

    exercises_cursor = db.exercises.find()
    exercises = []
    async for ex in exercises_cursor:
        ex_id = str(ex["_id"])
        ex["id"] = ex_id
        del ex["_id"]
        ex["solved"] = ex_id in solved_ids
        ex.pop("test_cases", None)
        ex.pop("stub", None)

        # First solver info
        first_solver_email = ex.pop("first_solver_email", None)
        if first_solver_email:
            fs_user = await db.users.find_one({"email": first_solver_email}, {"username": 1, "avatar": 1})
            ex["first_solver"] = {"username": fs_user.get("username") if fs_user else "?", "avatar": fs_user.get("avatar") if fs_user else None}
        else:
            ex["first_solver"] = None

        # Friends who solved
        solvers_list = ex.pop("solvers", [])
        if friends_emails and solvers_list:
            friends_solved_emails = [e for e in solvers_list if e in friends_emails]
            if friends_solved_emails:
                friends_solved = []
                cursor = db.users.find({"email": {"$in": friends_solved_emails}}, {"username": 1, "avatar": 1})
                async for fu in cursor:
                    friends_solved.append({"username": fu.get("username"), "avatar": fu.get("avatar")})
                ex["friends_solved"] = friends_solved
            else:
                ex["friends_solved"] = []
        else:
            ex["friends_solved"] = []

        exercises.append(ex)
    return exercises

@app.get("/api/exercises/solved")
async def get_solved_exercises(email: str = Depends(get_current_user)):
    user = await db.users.find_one({"email": email})
    if not user:
        return []
    return user.get("solved_exercises", [])

@app.get("/api/exercises/{exercise_id}")
async def get_exercise(exercise_id: str, email: str = Depends(get_current_user)):
    from bson import ObjectId
    try:
        oid = ObjectId(exercise_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de ejercicio inválido")
    ex = await db.exercises.find_one({"_id": oid})
    if not ex:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")
    
    user = await db.users.find_one({"email": email})
    solved_ids = set(user.get("solved_exercises", [])) if user else set()
    
    ex["id"] = str(ex["_id"])
    del ex["_id"]
    ex["solved"] = ex["id"] in solved_ids
    return ex

@app.post("/api/exercises/{exercise_id}/solve")
async def solve_exercise(exercise_id: str, body: SolveRequest, email: str = Depends(get_current_user)):
    from bson import ObjectId
    try:
        oid = ObjectId(exercise_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de ejercicio inválido")
    ex = await db.exercises.find_one({"_id": oid})
    if not ex:
        raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

    test_cases = ex.get("test_cases", [])
    if not test_cases:
        raise HTTPException(status_code=400, detail="Este ejercicio no tiene casos de prueba configurados")

    # Only Python execution supported for now
    if body.language != "Python":
        if body.save:
            user = await db.users.find_one({"email": email})
            solved_ids = user.get("solved_exercises", []) if user else []
            if exercise_id not in solved_ids:
                difficulty = ex.get("difficulty", "Normal")
                elo_gain = 1 if difficulty == "Fácil" else (5 if difficulty == "Difícil" else 2)
                
                await db.users.update_one(
                    {"email": email},
                    {
                        "$addToSet": {"solved_exercises": exercise_id},
                        "$inc": {"elo": elo_gain}
                    }
                )
                # Record solver in exercise
                ex_has_first = ex.get("first_solver_email")
                update_ex = {"$addToSet": {"solvers": email}}
                if not ex_has_first:
                    update_ex["$set"] = {"first_solver_email": email}
                await db.exercises.update_one({"_id": oid}, update_ex)
            return {"correct": True, "message": "¡Ejercicio guardado correctamente!"}
        return {"correct": True, "message": f"Verificación manual para {body.language}. Haz clic en Guardar si tu solución es correcta."}

    # Python execution: run each test case
    user_code = body.code
    for i, tc in enumerate(test_cases):
        test_input_str = tc["input"]
        expected_str = str(tc["expected_output"]).strip()

        # Build execution environment
        exec_globals = {}
        try:
            exec(compile(user_code, "<solution>", "exec"), exec_globals)
        except Exception as e:
            return {"correct": False, "message": f"Error de compilación: {str(e)}", "failed_case": i + 1}

        solve_fn = exec_globals.get("solve")
        if not solve_fn or not callable(solve_fn):
            return {"correct": False, "message": "No se encontró la función `solve` en tu código.", "failed_case": 0}

        # Parse arguments from test_input_str
        try:
            args_raw = f"({test_input_str},)"
            parsed_args = ast.literal_eval(args_raw)
            if not isinstance(parsed_args, tuple):
                parsed_args = (parsed_args,)
        except Exception as e:
            return {"correct": False, "message": f"Error procesando caso de prueba {i+1}: {str(e)}", "failed_case": i + 1}

        # Execute solution
        try:
            result = solve_fn(*parsed_args)
        except Exception as e:
            return {
                "correct": False,
                "message": f"Error en caso {i+1}: {str(e)}",
                "failed_case": i + 1,
                "input": test_input_str,
                "expected": expected_str
            }

        # Compare output
        actual_str = str(result).strip()
        # Normalize booleans
        if actual_str.lower() == "true": actual_str = "True"
        if actual_str.lower() == "false": actual_str = "False"
        if actual_str.replace(" ", "") == expected_str.replace(" ", ""):
            continue  # Pass
        else:
            return {
                "correct": False,
                "message": f"Caso {i+1} fallido",
                "failed_case": i + 1,
                "input": test_input_str,
                "expected": expected_str,
                "got": actual_str
            }

    # All test cases passed!
    if body.save:
        user = await db.users.find_one({"email": email})
        solved_ids = user.get("solved_exercises", []) if user else []
        if exercise_id not in solved_ids:
            ex_fresh = await db.exercises.find_one({"_id": oid})
            difficulty = ex_fresh.get("difficulty", "Normal") if ex_fresh else "Normal"
            elo_gain = 1 if difficulty == "Fácil" else (5 if difficulty == "Difícil" else 2)
            
            await db.users.update_one(
                {"email": email},
                {
                    "$addToSet": {"solved_exercises": exercise_id},
                    "$inc": {"elo": elo_gain}
                }
            )
            # Record solver in exercise + first_solver if first
            has_first = ex_fresh.get("first_solver_email") if ex_fresh else None
            update_ex = {"$addToSet": {"solvers": email}}
            if not has_first:
                update_ex["$set"] = {"first_solver_email": email}
            await db.exercises.update_one({"_id": oid}, update_ex)
        return {"correct": True, "message": "¡Ejercicio guardado correctamente! ✓"}

    return {"correct": True, "message": "¡Todos los casos de prueba superados! Puedes guardar tu solución."}

@app.get("/api/user/stats")
async def get_user_stats(email: str = Depends(get_current_user)):
    user = await db.users.find_one({"email": email})
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
    cursor = db.exercises.find({"_id": {"$in": valid_ids}}, {"difficulty": 1})
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

@app.get("/api/leaderboard")
async def get_leaderboard(email: str = Depends(get_current_user)):
    # Get top 5 users sorted by ELO descending
    cursor = db.users.find(
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

@app.get("/api/story/chapters")
async def get_story_chapters(email: str = Depends(get_current_user)):
    user = await db.users.find_one({"email": email})
    solved_ids = set(user.get("solved_exercises", [])) if user else set()
    
    # Fetch all exercises to get their true ObjectIds
    cursor = db.exercises.find({}, {"title": 1, "difficulty": 1, "category": 1})
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
    previous_unlocked = True # Chapter 1 is always unlocked
    
    for i in range(6):
        start_idx = i * chunk_size
        chunk = EXERCISES_SEED[start_idx : start_idx + chunk_size]
        
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

# ================= MATCHMAKING (LONG POLLING) =================
import asyncio
import uuid
import random

# In-memory stores for matchmaking
waiting_players = []  # List of dicts
active_matches = {}   # dict of match_id -> match data

@app.post("/api/matchmaking/join")
async def join_matchmaking(unranked: bool = False, email: str = Depends(get_current_user)):
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    global waiting_players
    
    # Remove if already in queue
    waiting_players = [p for p in waiting_players if p["email"] != email]
    
    elo = user.get("elo", 0)
    higher_elo_count = await db.users.count_documents({"elo": {"$gt": elo}})
    rank = higher_elo_count + 1
    
    # Function from /api/user/me duplicated locally for quick matchmaking
    def get_rank_tier(e):
        if e <= 75: return min(3, max(1, (e // 26) + 1))
        elif e <= 300: return 3 + min(3, max(1, ((e - 76) // 75) + 1))
        elif e <= 800: return 6 + min(3, max(1, ((e - 301) // 167) + 1))
        elif e <= 1300: return 9 + min(3, max(1, ((e - 801) // 167) + 1))
        elif e <= 2000: return 12 + min(3, max(1, ((e - 1301) // 234) + 1))
        else: return 16
        
    my_tier = get_rank_tier(elo)
    
    player_data = {
        "email": email,
        "username": user.get("username", "Unknown"),
        "avatar": user.get("avatar", ""),
        "elo": elo,
        "rank": rank,
        "tier": my_tier
    }
    
    # Check for opponent
    opponent = None
    for i, p in enumerate(waiting_players):
        # Match only requests of the same type (ranked vs unranked)
        if p.get("unranked", False) == unranked:
            # If ranked, verify the tier difference is <= 2
            if unranked or abs(p["data"]["tier"] - my_tier) <= 2:
                opponent = waiting_players.pop(i)
                break
                
    if opponent:
        match_id = str(uuid.uuid4())
        from app.exercises_data import EXERCISES_SEED
        # Filter exercises that are not just empty stubs
        valid_exercises = [ex for ex in EXERCISES_SEED if "test_cases" in ex and len(ex["test_cases"]) > 0]
        chosen_ex = dict(random.choice(valid_exercises) if valid_exercises else EXERCISES_SEED[0])

        # Look up the exercise in MongoDB by title to get its real _id
        # so the frontend can call /api/exercises/{id}/solve correctly
        db_exercise = await db.exercises.find_one({"title": chosen_ex["title"]})
        if db_exercise:
            chosen_ex["id"] = str(db_exercise["_id"])
        else:
            # Fallback: try to find any exercise with test cases in MongoDB
            db_exercise = await db.exercises.find_one({"test_cases": {"$exists": True, "$ne": []}})
            if db_exercise:
                chosen_ex = {
                    "title": db_exercise.get("title", chosen_ex["title"]),
                    "description": db_exercise.get("description", chosen_ex["description"]),
                    "difficulty": db_exercise.get("difficulty", chosen_ex["difficulty"]),
                    "category": db_exercise.get("category", chosen_ex["category"]),
                    "test_cases": db_exercise.get("test_cases", chosen_ex["test_cases"]),
                    "stub": db_exercise.get("stub", chosen_ex.get("stub", {})),
                    "id": str(db_exercise["_id"])
                }
            # If still nothing from DB, leave id missing — solve endpoint will 400
        
        active_matches[match_id] = {
            "player1": opponent["data"],
            "player2": player_data,
            "p1_progress": 0,
            "p2_progress": 0,
            "exercise": chosen_ex,
            "status": "ongoing",
            "winner": None,
            "event": asyncio.Event()
        }
        
        opponent["match_id"] = match_id
        opponent["event"].set()  # Wake up opponent
        
        return {"status": "matched", "match_id": match_id}
        
    # No opponent, wait in queue
    my_event = asyncio.Event()
    my_entry = {
        "email": email,
        "data": player_data,
        "event": my_event,
        "match_id": None
    }
    waiting_players.append(my_entry)
    
    try:
        # Long poll for 25 seconds
        await asyncio.wait_for(my_event.wait(), timeout=25.0)
        return {"status": "matched", "match_id": my_entry["match_id"]}
    except asyncio.TimeoutError:
        # Remove from queue if timeout
        waiting_players = [p for p in waiting_players if p["email"] != email]
        return {"status": "timeout"}

@app.delete("/api/matchmaking/leave")
async def leave_matchmaking(email: str = Depends(get_current_user)):
    global waiting_players
    waiting_players = [p for p in waiting_players if p["email"] != email]
    return {"status": "left"}

@app.get("/api/matchmaking/match/{match_id}")
async def get_match_state(match_id: str, email: str = Depends(get_current_user)):
    match = active_matches.get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
        
    # Which player is asking?
    is_p1 = match["player1"]["email"] == email
    opponent_data = match["player2"] if is_p1 else match["player1"]
    my_data = match["player1"] if is_p1 else match["player2"]
    
    my_progress = match["p1_progress"] if is_p1 else match["p2_progress"]
    op_progress = match["p2_progress"] if is_p1 else match["p1_progress"]
    
    return {
        "me": my_data,
        "my_progress": my_progress,
        "opponent": opponent_data,
        "op_progress": op_progress,
        "exercise": match["exercise"],
        "status": match["status"],
        "winner": match["winner"]
    }

@app.get("/api/matchmaking/match/{match_id}/poll")
async def poll_match_state(match_id: str, email: str = Depends(get_current_user)):
    match = active_matches.get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
        
    try:
        # Wait up to 25s for an event (progress update or win)
        await asyncio.wait_for(match["event"].wait(), timeout=25.0)
        
        # Determine who won or what the state is
        is_p1 = match["player1"]["email"] == email
        op_progress = match["p2_progress"] if is_p1 else match["p1_progress"]
        
        return {
            "status": "updated", 
            "op_progress": op_progress, 
            "match_status": match["status"], 
            "winner": match["winner"]
        }
    except asyncio.TimeoutError:
        return {"status": "timeout"}

class SubmitBatchRequest(BaseModel):
    results: List[dict] # { passed: bool, error: str }

@app.post("/api/matchmaking/match/{match_id}/submit")
async def submit_match_solution(match_id: str, body: SubmitBatchRequest, email: str = Depends(get_current_user)):
    match = active_matches.get(match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Partida no encontrada")
        
    if match["status"] != "ongoing":
        return {"status": match["status"], "winner": match["winner"]}
        
    is_p1 = match["player1"]["email"] == email
    
    passed_count = sum(1 for r in body.results if r.get("passed", False))
    total_cases = len(match["exercise"]["test_cases"])
    progress_pct = (passed_count / total_cases) * 100 if total_cases > 0 else 0
    
    # Update progress
    if is_p1:
        match["p1_progress"] = progress_pct
    else:
        match["p2_progress"] = progress_pct
        
    match["event"].set()
    await asyncio.sleep(0.1) # Let pollers wake up
    match["event"].clear()
    
    if progress_pct == 100:
        # Match ends
        match["status"] = "finished"
        match["winner"] = email
        
        # Assign ELO and win streak
        winner_email = email
        loser_email = match["player2"]["email"] if is_p1 else match["player1"]["email"]
        
        # Simple ELO update logic (+25 won, -15 lost) and track real win/match stats
        await db.users.update_one({"email": winner_email}, {"$inc": {"elo": 25, "win_streak": 1, "wins": 1, "matches_played": 1}})
        await db.users.update_one({"email": loser_email}, {"$inc": {"elo": -15, "matches_played": 1}, "$set": {"win_streak": 0}})
        
        # Save Match to Database
        await db.matches.insert_one({
            "match_id": match_id,
            "player1_email": match["player1"]["email"],
            "player2_email": match["player2"]["email"],
            "winner_email": winner_email,
            "loser_email": loser_email,
            "exercise_id": match["exercise"].get("id"),
            "unranked": match.get("unranked", False),
            "created_at": datetime.utcnow()
        })
        
        match["event"].set()
        
        return {"status": "finished", "winner": email, "is_winner": True}
        
    return {"status": "ongoing", "progress": progress_pct}
