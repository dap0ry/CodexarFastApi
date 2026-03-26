# Codexar API

Backend REST API para **Codexar** — plataforma de programación competitiva con duelos 1v1 en tiempo real, sistema de ELO y modo ejercicios.

**Stack:** FastAPI · Python 3.11 · MongoDB Atlas (Motor async) · Cloudinary · Brevo (email) · Render.com

---

## Estado del proyecto

### Implementado
- [x] Autenticación JWT (HS256, 7 días)
- [x] Registro con **verificación de email** (código 6 dígitos, TTL 5 min, Brevo API)
- [x] Login
- [x] Onboarding de usuario (username, avatar, lenguajes, nivel, descripción)
- [x] Perfil: editar datos, cambiar contraseña, subir avatar (Cloudinary)
- [x] Sistema de ELO y rangos (Bronce → Campeón)
- [x] Ejercicios: listar, resolver, ejecución sandboxed en Python
- [x] Matchmaking: cola ranked/unranked, long-poll 25s, batallas 1v1
- [x] Amigos: solicitudes, aceptar/rechazar, búsqueda, activity feed
- [x] Entorno local: venv + .env configurado

### Pendiente / Por hacer
- [ ] Logros (`achievements.py` — placeholder vacío)
- [ ] Tienda (`store.py` — placeholder vacío)
- [ ] Story mode / capítulos (`/api/story/chapters`)
- [ ] Leaderboard endpoint (actualmente calculado en `users.py`)
- [ ] Rate limiting en endpoints de auth
- [ ] Tests automatizados

---

## Configuración local

### 1. Entorno virtual
```bash
cd CodexarFastApi
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Variables de entorno
El `.env` ya existe en el repo local con los valores reales. Estructura:
```env
MONGODB_URI=
JWT_SECRET=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
BREVO_API_KEY=
BREVO_SENDER_EMAIL=onedrivexservice@gmail.com
```

### 3. Arrancar
```bash
uvicorn app.main:app --reload
```
API disponible en `http://localhost:8000`
Swagger docs en `http://localhost:8000/docs`

---

## Arquitectura de archivos

```
app/
├── main.py                  # FastAPI app, lifespan, CORS, routers
├── exercises_data.py        # Seed de ejercicios (inyectado en startup)
├── core/
│   ├── config.py            # Variables de entorno (MONGODB_URI, JWT, Cloudinary, Brevo)
│   ├── database.py          # Motor async client, TTL index email_verifications, seed
│   └── security.py          # bcrypt, JWT create/verify, get_current_user()
├── models/
│   ├── user.py              # UserRegister, UserLogin, Token, EmailVerifyRequest, ResendVerificationRequest, OnboardData
│   └── exercise.py          # ExerciseRequest
├── routers/
│   ├── auth.py              # /api/auth/* — register, verify-email, resend-verification, login
│   ├── users.py             # /api/user/* — me, onboard, profile/update, check-username
│   ├── exercises.py         # /api/exercises/*
│   ├── friends.py           # /api/friends/*
│   ├── matchmaking.py       # /api/matchmaking/*
│   ├── achievements.py      # placeholder
│   └── store.py             # placeholder
└── services/
    └── email_service.py     # Brevo HTTP API + template HTML cyberpunk
```

---

## Endpoints

### Auth — `/api/auth`
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/register` | ❌ | Envía código 6 dígitos al email, NO crea usuario aún |
| POST | `/verify-email` | ❌ | Valida código → crea usuario → devuelve JWT |
| POST | `/resend-verification` | ❌ | Regenera código y reenvía email |
| POST | `/login` | ❌ | Email + password → JWT |

### Usuario — `/api/user`
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/me` | ✅ | Perfil completo: ELO, rango, global_rank, wins, streak |
| POST | `/onboard` | ✅ | Primera configuración de perfil |
| POST | `/profile/update` | ✅ | Actualizar perfil / contraseña / avatar |
| POST | `/verify-password` | ✅ | Comprobar contraseña actual |
| GET | `/check-username/{u}` | ❌ | Disponibilidad de username |

### Ejercicios — `/api/exercises`
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/` | ✅ | Listar todos con estado de resolución del usuario |
| GET | `/{id}` | ✅ | Detalle + casos de prueba |
| POST | `/{id}/solve` | ✅ | Ejecutar solución Python (sandboxed con AST) |

### Amigos — `/api/friends`
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| GET | `/` | ✅ | Lista de amigos + solicitudes |
| GET | `/search?q=` | ✅ | Buscar usuarios |
| GET | `/activity` | ✅ | Feed de actividad |
| POST | `/request/{username}` | ✅ | Enviar solicitud |
| POST | `/accept/{username}` | ✅ | Aceptar solicitud |
| POST | `/reject/{username}` | ✅ | Rechazar solicitud |
| POST | `/cancel/{username}` | ✅ | Cancelar solicitud enviada |

### Matchmaking — `/api/matchmaking`
| Método | Ruta | Auth | Descripción |
|--------|------|------|-------------|
| POST | `/join` | ✅ | Unirse a la cola (ranked/unranked) |
| DELETE | `/leave` | ✅ | Salir de la cola |
| GET | `/match/{id}` | ✅ | Estado de la partida |
| GET | `/match/{id}/poll` | ✅ | Long-poll 25s para actualizaciones |
| POST | `/match/{id}/submit` | ✅ | Enviar resultados → backend decide ganador |

---

## Base de datos — MongoDB (DB: `Codexar`)

| Colección | Campos clave |
|-----------|-------------|
| `users` | email, password (bcrypt), username, is_onboarded, elo, wins, win_streak, languages, avatar, solved_exercises[] |
| `exercises` | title, difficulty, category, description, test_cases[], stub |
| `email_verifications` | email, code_hash (bcrypt), hashed_password, expires_at (TTL 5 min), created_at |

> `email_verifications` tiene un índice TTL en `expires_at` — MongoDB borra los docs automáticamente al expirar.

---

## Sistema de ELO y rangos

| Rango | ELO |
|-------|-----|
| Bronce I–III | 0–75 |
| Plata I–III | 76–300 |
| Oro I–III | 301–800 |
| Platino I–III | 801–1300 |
| Diamante I–III | 1301–2000 |
| Campeón | 2001+ |

Resultado de partida: **+25 ELO** ganador · **-15 ELO** perdedor

---

## Notas importantes

- **Lifespan:** Se usa el patrón `@asynccontextmanager lifespan` de FastAPI moderno (el `add_event_handler` fue eliminado en Starlette 1.x).
- **Email:** El sender verificado en Brevo es `onedrivexservice@gmail.com`. Cambiar con `BREVO_SENDER_EMAIL` en `.env`.
- **Matchmaking:** El estado de partidas es **in-memory** (dict + list). Se resetea si el servidor reinicia — para producción habría que migrar a Redis.
- **URL producción:** `https://codexarapi.onrender.com`

---

## Convención de ramas y commits

```
main     ← producción (no tocar directamente)
develop  ← desarrollo activo
```

Prefijos de commits: `feat:` `fix:` `refactor:` `docs:` `chore:` `test:`
