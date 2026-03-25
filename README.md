# Codexar API

Backend REST API para **Codexar** — una plataforma de programación competitiva donde los usuarios resuelven ejercicios, suben su ELO y se enfrentan a otros desarrolladores en duelos en tiempo real.

Construida con **FastAPI** + **MongoDB Atlas** + **Cloudinary**, desplegada en **Render**.

---

## 🚀 Stack Tecnológico

| Capa | Tecnología |
|---|---|
| Framework | FastAPI (Python) |
| Base de datos | MongoDB Atlas (Motor async) |
| Autenticación | JWT (HS256, tokens de 7 días) |
| Almacenamiento | Cloudinary (fotos de perfil) |
| Despliegue | Render |

---

## 📦 Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto con lo siguiente:

```env
MONGODB_URI=tu_cadena_de_conexion_mongodb_atlas
JWT_SECRET=tu_clave_secreta
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
```

---

## 🛠️ Instalación Local

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-org/codexar-api.git
cd codexar-api

# 2. Crea y activa un entorno virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Configura tu archivo .env (ver sección anterior)

# 5. Arranca el servidor de desarrollo
uvicorn main:app --reload
```

La API estará disponible en `http://localhost:8000`.  
Documentación interactiva en `http://localhost:8000/docs`.

---

## 📡 Endpoints

### Health
| Método | Ruta | Descripción |
|---|---|---|
| GET / HEAD | `/` | Health check (usado por UptimeRobot) |
| GET | `/api/health` | Health check extendido |

### Autenticación
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/auth/register` | Registrar un nuevo usuario |
| POST | `/api/auth/login` | Iniciar sesión y obtener token JWT |

### Usuario y Perfil
| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/api/user/me` | ✅ | Obtener perfil, ELO y rango del usuario actual |
| GET | `/api/user/check-username/{username}` | ❌ | Comprobar si un nombre de usuario está disponible |
| POST | `/api/user/onboard` | ✅ | Completar el onboarding (username, idiomas, avatar) |
| POST | `/api/user/profile/update` | ✅ | Actualizar perfil, contraseña o avatar |
| POST | `/api/user/verify-password` | ✅ | Verificar la contraseña actual |

### Ejercicios
| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/api/exercises` | ✅ | Listar todos los ejercicios con estado de resolución |
| GET | `/api/exercises/solved` | ✅ | Obtener IDs de ejercicios resueltos |
| GET | `/api/exercises/{id}` | ✅ | Obtener un ejercicio con sus casos de prueba |
| POST | `/api/exercises/{id}/solve` | ✅ | Enviar y ejecutar una solución contra los tests |

### Amigos
| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| GET | `/api/friends` | ✅ | Obtener amigos, solicitudes enviadas y recibidas |
| GET | `/api/friends/search?q=` | ✅ | Buscar usuarios por nombre |
| GET | `/api/friends/activity` | ✅ | Obtener feed de actividad |
| POST | `/api/friends/request/{username}` | ✅ | Enviar solicitud de amistad |
| POST | `/api/friends/accept/{username}` | ✅ | Aceptar solicitud de amistad |
| POST | `/api/friends/reject/{username}` | ✅ | Rechazar solicitud de amistad |
| POST | `/api/friends/cancel/{username}` | ✅ | Cancelar una solicitud enviada |

### Matchmaking
| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| POST | `/api/matchmaking/join` | ✅ | Unirse a la cola de emparejamiento (long-poll, 25s) |
| DELETE | `/api/matchmaking/leave` | ✅ | Salir de la cola de emparejamiento |
| GET | `/api/matchmaking/match/{id}` | ✅ | Obtener el estado actual de la partida |
| GET | `/api/matchmaking/match/{id}/poll` | ✅ | Long-poll para actualizaciones de la partida (25s) |
| POST | `/api/matchmaking/match/{id}/submit` | ✅ | Enviar resultados de tests durante una partida |

### Autenticación de rutas protegidas

Todas las rutas protegidas requieren un token Bearer en la cabecera `Authorization`:

```
Authorization: Bearer <tu_token_jwt>
```

---

## 🏆 Sistema de ELO y Rangos

La plataforma usa un sistema de ranking basado en ELO. Completar ejercicios o ganar partidas otorga puntos.

| Rango | ELO |
|---|---|
| Bronce I–III | 0 – 75 |
| Plata I–III | 76 – 300 |
| Oro I–III | 301 – 800 |
| Platino I–III | 801 – 1300 |
| Diamante I–III | 1301 – 2000 |
| Campeón | 2001+ |

Resultado de partida: **+25 ELO** al ganador, **-15 ELO** al perdedor.

---

## 🤝 Contribuir

**¡Los forks y las Pull Requests están abiertos y son bienvenidos!** Ya sea un bug, una nueva feature o una mejora en la documentación — toda contribución se agradece.

### Reglas de Ramas

> ⚠️ **NUNCA hagas push directamente a `main`.** Todos los cambios deben ir a través de `develop`.

```
main      ← estable, solo producción
develop   ← rama de desarrollo activo — apunta siempre aquí
```

### Convención de Commits

Usa los siguientes prefijos para mantener el historial limpio:

| Prefijo | Cuándo usarlo |
|---|---|
| `feat:` | Nueva funcionalidad o endpoint |
| `fix:` | Corrección de un bug |
| `refactor:` | Reestructuración de código sin cambios de comportamiento |
| `docs:` | Cambios en el README u otra documentación |
| `chore:` | Dependencias, configuración, herramientas |
| `test:` | Añadir o actualizar tests |

**Ejemplos:**
```bash
git commit -m "feat: añadir endpoint de leaderboard"
git commit -m "fix: método HEAD devolvía 405 en el health check"
git commit -m "docs: actualizar sección de variables de entorno"
```

### Flujo de Trabajo

```bash
# 1. Haz fork del repositorio y clónalo
git clone https://github.com/tu-usuario/codexar-api.git

# 2. Crea una rama desde develop — NUNCA desde main
git checkout develop
git checkout -b feat/nombre-de-tu-feature

# 3. Haz tus cambios y confírmalos
git add .
git commit -m "feat: descripción de tu cambio"

# 4. Haz push a tu fork
git push origin feat/nombre-de-tu-feature

# 5. Abre una Pull Request apuntando a la rama develop del repo principal
```

### Checklist antes de abrir una PR

- [ ] La rama está basada en `develop`, no en `main`
- [ ] Los commits siguen la convención de prefijos
- [ ] No se ha subido ningún archivo `.env` ni credenciales
- [ ] La API sigue devolviendo `{"status": "ok"}` en `/`

---

## 📄 Licencia

MIT — libre de usar, forkear y modificar.
