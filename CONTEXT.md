# CodexarFastApi — Backend Context

## Entry point
`app/main.py` — FastAPI app, security headers middleware, CORS (configurable via `ALLOWED_ORIGINS` env), mounts all routers under `/api`.

## Directory map
```
app/
├── main.py                  # App init, CORS, security headers, router registration
├── exercises_data.py        # Seed data (injected on startup)
├── core/
│   ├── config.py            # Settings (MongoDB URI, JWT secret, Cloudinary creds, ALLOWED_ORIGINS)
│   ├── database.py          # Motor async client; seeds exercises on startup
│   ├── security.py          # bcrypt hashing, JWT create/verify, get_current_user()
│   ├── roles.py             # require_admin(), require_moderator() FastAPI Depends
│   └── compare.py           # Code comparison/diff utilities
├── models/
│   ├── user.py              # Pydantic schemas for user requests/responses
│   └── exercise.py          # Pydantic schemas for exercise requests
├── routers/
│   ├── auth.py              # Login, register, JWT
│   ├── users.py             # Profile, onboard, leaderboard, heartbeat, bot-result, public profile
│   ├── exercises.py         # List, detail, solve (sandboxed Python eval)
│   ├── friends.py           # Friend list, requests, search, activity
│   ├── matchmaking.py       # Ranked/friendly queue, long-poll, submit (in-memory)
│   ├── survival.py          # Co-op survival mode (WebSocket, in-memory rooms)
│   ├── teams.py             # Teams CRUD, invite/accept/decline/kick/leave
│   ├── tournaments.py       # Admin-created team tournaments, register, submit-solve
│   ├── achievements.py      # Achievement catalog, equip/unequip (max 3 equipped)
│   ├── news.py              # News feed with likes and @mentions
│   └── admin.py             # Admin panel: list users, ban/unban, set-role, delete exercise
└── services/
    └── email_service.py     # Email sending utilities
```

## Endpoints reference

### Auth — `/api/auth`
| Method | Path        | Description              |
|--------|-------------|--------------------------|
| POST   | /register   | Create account           |
| POST   | /login      | Returns JWT access_token |

### Users — `/api/user`
| Method | Path                      | Description                                              |
|--------|---------------------------|----------------------------------------------------------|
| GET    | /me                       | Full profile: ELO, rank, global_rank, wins, coins, etc. |
| GET    | /check-username/{username}| Availability check                                      |
| POST   | /onboard                  | Set username, languages, level, description, avatar     |
| POST   | /verify-password          | Verify current password (for settings)                  |
| POST   | /profile/update           | Update profile, password, avatar (multipart)            |
| GET    | /stats                    | Solved count by difficulty (easy/medium/hard)           |
| GET    | /profile/{username}       | Public profile: full stats, equipped achievements, friendship status, survival_stats |
| POST   | /heartbeat                | Update last_seen timestamp                              |
| POST   | /bot-result               | Record vs-CPU match result                              |
| POST   | /upload-background        | Upload profile background image (Cloudinary)            |

### Leaderboard — `/api/leaderboard`
| Method | Path | Description            |
|--------|------|------------------------|
| GET    | /    | Top 5 users by ELO     |

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
| POST   | /join                     | Join queue (ranked/friendly)                |
| GET    | /match/{id}/poll          | Long-poll (25 s) for match updates          |
| POST   | /match/{id}/submit        | Submit test results; backend picks winner   |
| POST   | /leave                    | Leave queue                                 |

### Survival — `/api/survival`
| Method    | Path                              | Description                                          |
|-----------|-----------------------------------|------------------------------------------------------|
| POST      | /room                             | Create room (difficulty: normal/dificil/demencial)   |
| GET       | /room/{room_id}                   | Get room state                                       |
| POST      | /room/{room_id}/start             | Start game (host only)                               |
| POST      | /invite/{room_id}/{target_username}| Invite friend to room                               |
| GET       | /pending-invites                  | Get pending survival invites for current user        |
| POST      | /accept/{invite_id}               | Accept invite                                        |
| POST      | /reject/{invite_id}               | Reject invite                                        |
| WebSocket | /ws/{room_id}?token=              | Real-time game: submit, code_sync, lang_sync, abandon|

### Teams — `/api/teams`
| Method | Path                         | Description                                    |
|--------|------------------------------|------------------------------------------------|
| POST   | /create                      | Create team (1 per user, max name 20 chars)    |
| GET    | /                            | List all teams                                 |
| GET    | /mine                        | My team with enriched member info              |
| GET    | /invites/mine                | My pending team invites                        |
| GET    | /{team_id}                   | Team detail with member stats                  |
| POST   | /{team_id}/invite            | Invite user (owner only)                       |
| POST   | /{team_id}/accept            | Accept team invite                             |
| POST   | /{team_id}/decline           | Decline team invite                            |
| POST   | /{team_id}/leave             | Leave (owner leaving dissolves team)           |
| PATCH  | /{team_id}                   | Update team info (owner only)                  |
| DELETE | /{team_id}                   | Delete team (owner or admin)                   |
| DELETE | /{team_id}/members/{username}| Kick member (owner only)                       |

### Tournaments — `/api/tournaments`
| Method | Path                              | Description                                          |
|--------|-----------------------------------|------------------------------------------------------|
| POST   | /                                 | Create tournament (admin only)                       |
| GET    | /                                 | List all tournaments                                 |
| GET    | /active                           | List upcoming + active tournaments                   |
| GET    | /{tournament_id}                  | Tournament detail with team progress                 |
| POST   | /{tournament_id}/register         | Register my team (captain only)                      |
| POST   | /{tournament_id}/submit-solve     | Mark exercise as solved for my team                  |
| PATCH  | /{tournament_id}/status           | Update status (admin only): upcoming/active/finished |
| DELETE | /{tournament_id}                  | Delete tournament (admin only)                       |

### Achievements — `/api/achievements`
| Method | Path      | Description                              |
|--------|-----------|------------------------------------------|
| GET    | /         | Full catalog with unlock + progress info |
| GET    | /equipped | Currently equipped achievements (max 3)  |
| POST   | /equip    | Equip an achievement                     |
| POST   | /unequip  | Unequip an achievement                   |

### News — `/api/news`
| Method | Path          | Description                               |
|--------|---------------|-------------------------------------------|
| GET    | /             | News feed (newest first, with like status)|
| POST   | /             | Create news post (any user)               |
| POST   | /{id}/like    | Toggle like on a news post                |

### Admin — `/api/admin`
| Method | Path                    | Description                        |
|--------|-------------------------|------------------------------------|
| GET    | /users                  | List all onboarded users           |
| POST   | /ban/{username}         | Ban user                           |
| POST   | /unban/{username}       | Unban user                         |
| POST   | /set-role/{username}    | Set role: user/moderator/admin     |
| DELETE | /exercises/{exercise_id}| Delete exercise                    |

## Database — MongoDB Atlas (`DB_NAME = "Codexar"`)
Collections:
- `users` — email, username, hashed_password, elo, max_elo, wins, losses, win_streak, matches_played, ranked_wins, solved_exercises[], friends[], friend_requests_sent[], friend_requests_received[], is_onboarded, avatar, languages, level, description, role (user/moderator/admin), is_banned, last_seen, coins, equipped_frame, profile_background, purchased_items[], equipped_achievements[], lang_stats{}, survival_stats{}, bot_wins, bot_matches, bot_wins_by_diff{}, bot_matches_by_diff{}
- `exercises` — title, description, difficulty, category, test_cases[], solved_by[], stub{}
- `teams` — name, description, photo_url, owner, members[], invites[], created_at
- `tournaments` — name, description, prize, start_time, exercise_ids[], status (upcoming/active/finished), participants[], progress{}, winner_team, ended_at
- `news` — title, subtitle, body, creator, mentions[], likes[], created_at
- `revoked_tokens` — jti (for JWT revocation)

## Auth middleware
`security.py → get_current_user(token)` — FastAPI `Depends()` on all protected routes.
Extracts `Authorization: Bearer <token>` header → verifies JWT → returns user email from MongoDB.
JWT tokens have `jti` field; revoked tokens stored in `revoked_tokens` collection.

## Role system
Three roles: `user` (default), `moderator`, `admin`.
- `require_admin` — used by admin panel, tournament CRUD, exercise delete
- `require_moderator` — moderators + admins can create exercises
- `roleNav.js` (frontend) injects admin/moderator nav links dynamically

## Survival mode internals
- In-memory `survival_rooms` and `survival_invites` dicts (reset on restart)
- WebSocket per room at `/api/survival/ws/{room_id}?token=<JWT>`
- Difficulty configs: normal (60s start, +10s bonus), dificil (45s, +7s), demencial (30s, +5s)
- Timer runs server-side; syncs every 5s via `time_sync` WS message
- Co-op: up to 4 players, shared code editor (`code_sync` action)
- Room cleanup 60s after game ends

## Matchmaking internals
- `waiting_players` — in-memory list (not Redis); resets on server restart
- `active_matches` — in-memory dict keyed by UUID match_id
- Ranked matching: tier-based ±2 tiers
- Long-polling timeout: 25 seconds per poll request
- Uses WebSocket for real-time queue state (matchmakingGlobal.js on frontend)

## Code execution (exercises.py)
- Python-only sandboxing via `ast` module parse + restricted `eval`
- No external judge; runs inline in the FastAPI process
- If all test cases pass → marks exercise solved + awards ELO + updates lang_stats

## Deployment
- Platform: Render.com
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Python: 3.11.0
- Live URL: `https://codexarapi.onrender.com`

## Key config values (core/config.py)
```python
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
DB_NAME = "Codexar"
```
