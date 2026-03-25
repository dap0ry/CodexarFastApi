from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import *  # noqa: F401,F403 — loads env vars and cloudinary config
from app.core.database import startup_db_client, shutdown_db_client
from app.routers import auth, users, friends, exercises, matchmaking, achievements, store

app = FastAPI(title="Codexar Auth API")


@app.api_route("/", methods=["GET", "HEAD"])
def health_check():
    return {"status": "ok"}


@app.get("/api/health")
async def api_health_check():
    return {"status": "ok", "message": "Codexar API is running"}


# Setup CORS to allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For dev only.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB lifecycle
app.add_event_handler("startup", startup_db_client)
app.add_event_handler("shutdown", shutdown_db_client)

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(friends.router)
app.include_router(exercises.router)
app.include_router(matchmaking.router)
app.include_router(achievements.router)
app.include_router(store.router)
