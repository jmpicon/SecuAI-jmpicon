# Guía de despliegue

## Requisitos

- Docker ≥ 24 + docker-compose v2.
- 8 GB RAM (la terminal Kali pesa).
- ~6 GB disco (imágenes + content).
- Puertos libres: **8090** (dashboard), opcionalmente **5001-5003** (labs vulnerables).

---

## Despliegue local — desarrollo / clase

### 1. Clonar y configurar

```bash
git clone <repo> secu_IA
cd secu_IA
cp .env.example .env
```

Edita `.env` para personalizar:
```env
ACCESS_CODE=tu-codigo-clase    # el código que reparts a estudiantes
SECRET_KEY=$(openssl rand -hex 32)
PORT=8090
```

### 2. Construir y arrancar

```bash
make build       # tarda ~3-5 min la primera vez (Kali pesa)
make up
make logs        # comprobar que todos los services están up
```

### 3. Verificar

```bash
curl http://localhost:8090/health         # ok
curl http://localhost:8090/api/health     # {"status":"ok"}
curl http://localhost:5001/health         # lab prompt-injection (si expuesto)
```

Abre http://localhost:8090. Login con el `ACCESS_CODE`.

### 4. Operar

```bash
make down        # parar todo
make logs        # streaming logs
make status      # ver containers
make clean       # borrar imágenes + node_modules
```

---

## Exponer labs vulnerables al host (opcional)

Crea `docker-compose.override.yml`:

```yaml
services:
  lab-prompt-injection:
    ports: ["5001:5001"]
  lab-rag-poisoning:
    ports: ["5002:5002"]
  lab-model-extraction:
    ports: ["5003:5003"]
```

`make up` los re-leerá.

⚠ Sólo si vas a probar desde el host. **Nunca** expongas a internet.

---

## Despliegue en máquina compartida (aula)

Si quieres servir el dashboard a estudiantes en una red local:

1. Identifica IP del host: `ip addr show | grep inet`.
2. Verifica que el firewall permite 8090.
3. Comparte URL: `http://<ip-host>:8090`.
4. Pasa código `ACCESS_CODE`.

Para Kahoot multijugador (los estudiantes se conectan a la partida):
- Asegúrate de que el host es alcanzable desde los dispositivos de los estudiantes.
- El QR del juego apunta a `http://<ip-host>:8090/jugar?code=ABCDEF`.

---

## Despliegue en VPS / cloud

⚠ **Sólo el dashboard**, NO los labs vulnerables.

### Mínimo

```bash
# En el VPS
git clone <repo>
cd secu_IA
docker compose up -d backend frontend tools    # NO los labs
```

### Con HTTPS (recomendado para uso público del dashboard)

Usa un reverse proxy delante (Caddy / Traefik / Nginx con Let's Encrypt):

```yaml
# Caddyfile
secuai.tudominio.com {
  reverse_proxy localhost:8090
}
```

### Considera seguridad básica
- Cambia `ACCESS_CODE` por algo robusto.
- `SECRET_KEY` real (no el de ejemplo).
- Limita IPs si es para grupo cerrado (con firewall o auth previa).
- Pon rate limiting agresivo en el reverse proxy.

---

## Railway / Render / similares

El repo trae `railway.toml` heredado de CursoPPS. Adáptalo:
- Sólo desplegar backend + frontend.
- NO desplegar los labs (no tiene sentido en cloud público).
- Configurar env vars `SECRET_KEY`, `ACCESS_CODE`.

---

## Backups y persistencia

Este proyecto es **stateless**:
- Sin base de datos.
- Sin uploads persistentes.
- Sesiones en JWT (sin servidor de sesiones).

Lo único que cambias entre despliegues:
- Contenido en `Modulo*/` (PDFs/PPTX que añadas).
- Adaptaciones de teoría/ejercicios.

→ Backup = `git push`.

---

## Troubleshooting

### El dashboard carga pero `/api/modules` devuelve vacío
Los volúmenes `Modulo*/` no están montados. Verifica que los directorios existen y que docker-compose puede leerlos.

```bash
docker compose exec backend ls /content/Modulo1
```

### La terminal web no conecta
ttyd usa WebSocket en `/terminal/ws`. Verifica:
- `tools` container está `healthy`.
- Nginx config en `frontend/nginx.conf` tiene el bloque `/terminal/`.
- No hay proxy intermedio que rompa WS.

### Kahoot no funciona
WebSocket en `/api/game/`. Mismo principio. Asegúrate de que el reverse proxy (si lo tienes) hace upgrade WS.

### Lab vulnerable no responde
```bash
docker compose ps                    # ¿está running?
docker compose logs lab-prompt-injection
docker compose restart lab-prompt-injection
```

### Performance baja en aula
- Reduce workers backend: `--workers 1` en Dockerfile.
- Cambia container `tools` por imagen más ligera si no necesitas Kali completo.

---

## Actualizar el material

Para añadir un módulo o ejercicio nuevo:
1. Edita el markdown en `ModuloN/` o `taller/`.
2. Sin rebuild necesario — el backend sirve los ficheros del volumen.
3. Refresca el frontend (Ctrl+Shift+R).

Para añadir un nuevo lab:
1. Crea `labs/mi-lab/{Dockerfile,app.py,requirements.txt}`.
2. Añade el service en `docker-compose.yml`.
3. Añade entrada en `frontend/src/pages/LabsPage.tsx`.
4. `make build` + `make up`.
