from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import *  # noqa: F401,F403 — loads env vars and cloudinary config
from app.core.config import ALLOWED_ORIGINS
from app.core.database import startup_db_client, shutdown_db_client
from app.routers import auth, users, friends, exercises, matchmaking, achievements, survival, news, admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_db_client()
    yield
    await shutdown_db_client()


app = FastAPI(title="Codexar Auth API", lifespan=lifespan)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response: Response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    return response


@app.api_route("/", methods=["GET", "HEAD"])
def health_check():
    return {"status": "ok"}


@app.get("/api/health")
async def api_health_check():
    return {"status": "ok", "message": "Codexar API is running"}


# Setup CORS — en local: ALLOWED_ORIGINS=* / en prod: ALLOWED_ORIGINS=https://tudominio.vercel.app
if ALLOWED_ORIGINS == "*":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    origins = [o.strip() for o in ALLOWED_ORIGINS.split(",")]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
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
app.include_router(survival.router)
app.include_router(news.router)
app.include_router(admin.router)
