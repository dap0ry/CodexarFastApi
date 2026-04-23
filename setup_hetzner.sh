#!/bin/bash
set -e

echo ""
echo "======================================================"
echo "   CODEXAR — Setup Hetzner VPS"
echo "======================================================"
echo ""

# ── 1. Dependencias del sistema ───────────────────────────
echo "==> Instalando Nginx y Certbot..."
apt-get update -y -q
apt-get install -y -q nginx certbot python3-certbot-nginx

# ── 2. Estructura de directorios ──────────────────────────
echo "==> Creando estructura /opt/codexar/..."
mkdir -p /opt/codexar/judge_tmp
mkdir -p /opt/codexar/worker

# ── 3. Clonar o actualizar la API ─────────────────────────
echo "==> Clonando API desde GitHub..."
if [ -d "/opt/codexar/api/.git" ]; then
    echo "   (repo ya existe, haciendo pull)"
    cd /opt/codexar/api && git pull
else
    git clone https://github.com/dap0ry/CodexarFastApi.git /opt/codexar/api
fi

# ── 4. Dockerfile de la API ───────────────────────────────
echo "==> Escribiendo Dockerfile de la API..."
cat > /opt/codexar/api/Dockerfile << 'APIEOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
APIEOF

# ── 5. Worker (judge) ─────────────────────────────────────
echo "==> Creando Worker (judge)..."

cat > /opt/codexar/worker/Dockerfile << 'WDEOF'
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir redis docker
COPY worker.py .
CMD ["python", "-u", "worker.py"]
WDEOF

cat > /opt/codexar/worker/worker.py << 'WPEOF'
import redis
import docker
import json
import os
import shutil
import time
import uuid

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379")
QUEUE_KEY = "judge:queue"
RESULT_PREFIX = "judge:result:"
TMP_BASE = "/opt/codexar/judge_tmp"

r = redis.from_url(REDIS_URL, decode_responses=True)
docker_client = docker.from_env()

LANGUAGES = {
    "python": {
        "image": "python:3.11-slim",
        "cmd": "python /code/solution.py < /code/input.txt",
        "filename": "solution.py",
    },
    "cpp": {
        "image": "gcc:12",
        "cmd": "g++ -O2 -o /tmp/sol /code/solution.cpp && /tmp/sol < /code/input.txt",
        "filename": "solution.cpp",
    },
    "javascript": {
        "image": "node:20-alpine",
        "cmd": "node /code/solution.js < /code/input.txt",
        "filename": "solution.js",
    },
}


def run_testcase(language, code, stdin_input, time_limit=5, memory_mb=256):
    cfg = LANGUAGES.get(language)
    if not cfg:
        return {"verdict": "CE", "output": f"Lenguaje no soportado: {language}"}

    job_dir = os.path.join(TMP_BASE, str(uuid.uuid4()))
    os.makedirs(job_dir, exist_ok=True)

    try:
        with open(os.path.join(job_dir, cfg["filename"]), "w") as f:
            f.write(code)
        with open(os.path.join(job_dir, "input.txt"), "w") as f:
            f.write(stdin_input or "")

        container = docker_client.containers.run(
            image=cfg["image"],
            command=["sh", "-c", cfg["cmd"]],
            volumes={job_dir: {"bind": "/code", "mode": "ro"}},
            network_mode="none",
            mem_limit=f"{memory_mb}m",
            nano_cpus=500_000_000,
            detach=True,
            remove=False,
        )

        try:
            result = container.wait(timeout=time_limit + 2)
            stdout = container.logs(stdout=True, stderr=False).decode("utf-8", errors="replace").strip()
            stderr = container.logs(stdout=False, stderr=True).decode("utf-8", errors="replace").strip()
            exit_code = result["StatusCode"]
        except Exception:
            container.kill()
            return {"verdict": "TLE", "output": ""}
        finally:
            try:
                container.remove(force=True)
            except Exception:
                pass

        if exit_code != 0:
            return {"verdict": "RE", "output": stderr or stdout}

        return {"verdict": "OK", "output": stdout}

    finally:
        shutil.rmtree(job_dir, ignore_errors=True)


def evaluate(language, code, test_cases, time_limit=5, memory_mb=256):
    for i, tc in enumerate(test_cases):
        result = run_testcase(language, code, tc.get("input", ""), time_limit, memory_mb)

        if result["verdict"] != "OK":
            return {**result, "test_case": i + 1, "total": len(test_cases)}

        expected = tc.get("expected_output", "").strip()
        actual = result["output"].strip()

        if actual != expected:
            return {
                "verdict": "WA",
                "test_case": i + 1,
                "total": len(test_cases),
                "expected": expected,
                "got": actual,
            }

    return {"verdict": "AC", "test_cases_passed": len(test_cases), "total": len(test_cases)}


def main():
    print("==> Codexar Judge Worker arrancado, esperando jobs...", flush=True)
    while True:
        try:
            item = r.blpop(QUEUE_KEY, timeout=5)
            if not item:
                continue

            _, raw = item
            job = json.loads(raw)
            job_id = job["job_id"]
            print(f"[JOB] {job_id} | {job.get('language')} | {len(job.get('test_cases', []))} casos", flush=True)

            result = evaluate(
                language=job["language"],
                code=job["code"],
                test_cases=job.get("test_cases", []),
                time_limit=job.get("time_limit", 5),
                memory_mb=job.get("memory_mb", 256),
            )

            r.setex(f"{RESULT_PREFIX}{job_id}", 120, json.dumps(result))
            print(f"[DONE] {job_id} -> {result['verdict']}", flush=True)

        except Exception as e:
            print(f"[ERROR] Worker: {e}", flush=True)
            time.sleep(1)


if __name__ == "__main__":
    main()
WPEOF

# ── 6. docker-compose.yml ─────────────────────────────────
echo "==> Creando docker-compose.yml..."
cat > /opt/codexar/docker-compose.yml << 'DCEOF'
services:
  api:
    build: ./api
    restart: always
    ports:
      - "8000:8000"
    env_file:
      - ./api/.env
    depends_on:
      - redis

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data

  worker:
    build: ./worker
    restart: always
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - /opt/codexar/judge_tmp:/opt/codexar/judge_tmp
    environment:
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis

volumes:
  redis_data:
DCEOF

# ── 7. Nginx ──────────────────────────────────────────────
echo "==> Configurando Nginx..."
cat > /etc/nginx/sites-available/api.codexar.es << 'NGINXEOF'
server {
    listen 80;
    server_name api.codexar.es;

    client_max_body_size 20M;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 60s;
        proxy_connect_timeout 10s;
    }
}
NGINXEOF

ln -sf /etc/nginx/sites-available/api.codexar.es /etc/nginx/sites-enabled/api.codexar.es
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

# ── 8. Pre-descargar imagenes del judge ───────────────────
echo "==> Descargando imagenes Docker para el judge (esto tarda un poco)..."
docker pull python:3.11-slim
docker pull gcc:12
docker pull node:20-alpine

# ── 9. Verificar que el .env existe ───────────────────────
if [ ! -f "/opt/codexar/api/.env" ]; then
    echo ""
    echo "  ERROR: Falta el archivo /opt/codexar/api/.env"
    echo "  Crea el .env con tus credenciales y vuelve a ejecutar:"
    echo "    cd /opt/codexar && docker compose up -d --build"
    echo ""
    exit 1
fi

# ── 10. Levantar todo ─────────────────────────────────────
echo "==> Construyendo y levantando contenedores..."
cd /opt/codexar
docker compose up -d --build

# ── 11. SSL ───────────────────────────────────────────────
echo "==> Obteniendo certificado SSL para api.codexar.es..."
certbot --nginx -d api.codexar.es --non-interactive --agree-tos -m danielpozarivera123@gmail.com --redirect

echo ""
echo "======================================================"
echo "  LISTO"
echo "  API corriendo en: https://api.codexar.es"
echo "  Health check:     https://api.codexar.es/api/health"
echo "======================================================"
echo ""
echo "Comandos utiles:"
echo "  cd /opt/codexar"
echo "  docker compose logs -f api       # logs de la API"
echo "  docker compose logs -f worker    # logs del judge"
echo "  docker compose restart api       # reiniciar API"
echo "  docker compose ps                # estado de los servicios"
echo ""
