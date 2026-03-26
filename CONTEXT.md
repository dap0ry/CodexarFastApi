# CodexarFastApi — Backend Context

## Entry point
`app/main.py` — FastAPI app, CORS (allow all origins), mounts all routers under `/api`.

## Directory map
```
app/
├── main.py                  # App init, CORS, router registration
├── exercises_data.py        # Seed data (injected on startup)
├── core/
│   ├── config.py            # Settings (MongoDB URI, JWT secret, Cloudinary creds)
│   ├── database.py          # Motor async client; seeds exercises on startup
│   └── security.py          # bcrypt hashing, JWT create/verify, get_current_user()
├── models/
│   ├── user.py              # Pydantic schemas for user requests/responses
│   └── exercise.py          # Pydantic schemas for exercise requests
└── routers/
    ├── auth.py              # 64 lines
    ├── users.py             # 348 lines
    ├── exercises.py         # 206 lines
    ├── friends.py           # 160 lines
    ├── matchmaking.py       # 237 lines
    ├── achievements.py      # placeholder
    └── store.py             # placeholder
```

## Endpoints reference

### Auth — `/api/auth`
| Method | Path        | Description              |
|--------|-------------|--------------------------|
| POST   | /register   | Create account           |
| POST   | /login      | Returns JWT access_token |

### Users — `/api/user`
| Method | Path                | Description                          |
|--------|---------------------|--------------------------------------|
| GET    | /me                 | Full profile: ELO, rank, global_rank, wins, streak |
| POST   | /onboard            | Set username, languages, description |
| POST   | /profile/update     | Update profile, password, avatar (multipart) |

### Exercises — `/api/exercises`
| Method | Path           | Description                                     |
|--------|----------------|-------------------------------------------------|
| GET    | /              | List all with user's solve status               |
| GET    | /{id}          | Single exercise + test cases                    |
| POST   | /{id}/solve    | Submit code → sandboxed Python eval → pass/fail |

### Friends — `/api/friends`
| Method | Path               | Description             |
|--------|--------------------|-------------------------|
| GET    | /                  | Friend list             |
| GET    | /requests          | Pending requests        |
| GET    | /search?q=         | Search users            |
| POST   | /request/{user_id} | Send friend request     |
| POST   | /accept/{user_id}  | Accept request          |
| POST   | /reject/{user_id}  | Reject request          |
| GET    | /activity          | Friend activity feed    |

### Matchmaking — `/api/matchmaking`
| Method | Path                      | Description                                 |
|--------|---------------------------|---------------------------------------------|
| POST   | /join                     | Join queue (ranked/unranked)                |
| GET    | /match/{id}/poll          | Long-poll (25 s) for match updates          |
| POST   | /match/{id}/submit        | Submit test results; backend picks winner   |
| POST   | /leave                    | Leave queue                                 |

## Database — MongoDB Atlas (`DB_NAME = "Codexar"`)
Collections:
- `users` — email, username, hashed_password, elo, wins, losses, win_streak, solved_exercises[], friends[], friend_requests[], is_onboarded, avatar, languages, description
- `exercises` — title, description, difficulty, category, test_cases[], solved_by[]

## Auth middleware
`security.py → get_current_user(token)` — FastAPI `Depends()` used on all protected routes.
Extracts `Authorization: Bearer <token>` header → verifies JWT → returns user doc from MongoDB.

## Code execution (exercises.py)
- Python-only sandboxing via `ast` module parse + restricted `eval`
- No external judge; runs inline in the FastAPI process
- If all test cases pass → marks exercise solved in user doc + awards ELO

## Matchmaking internals (matchmaking.py)
- `waiting_players` — in-memory list (not Redis); resets on server restart
- `active_matches` — in-memory dict keyed by UUID match_id
- Ranked matching: tier-based ±2 tiers
- Long-polling timeout: 25 seconds per poll request
- ELO update happens on submit endpoint when both players' results are in

## Deployment
- Platform: Render.com
- Config: `render.yaml`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Python: 3.11.0
- Live URL: `https://codexarapi.onrender.com`

## Key config values (core/config.py)
```python
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
DB_NAME = "Codexar"
```
