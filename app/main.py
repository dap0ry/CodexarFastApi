from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import *  # noqa: F401,F403 — loads env vars and cloudinary config
from app.core.database import startup_db_client, shutdown_db_client
from app.routers import auth, users, friends, exercises, matchmaking, achievements, store


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client()
    yield
    await shutdown_db_client()


app = FastAPI(title="Codexar Auth API", lifespan=lifespan)


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

# Routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(friends.router)
app.include_router(exercises.router)
app.include_router(matchmaking.router)
app.include_router(achievements.router)
app.include_router(store.router)
