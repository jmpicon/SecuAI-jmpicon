.PHONY: dev build up down logs clean install

## Install frontend dependencies
install:
	cd frontend && npm install

## Run development servers (backend + frontend separately)
dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

## Build Docker images
build:
	docker compose build

## Start all services with Docker
up:
	docker compose up -d

## Stop all services
down:
	docker compose down

## View logs
logs:
	docker compose logs -f

## Type-check frontend
type-check:
	cd frontend && npm run type-check

## Lint backend
lint-backend:
	cd backend && ruff check app/ && ruff format --check app/

## Full clean
clean:
	docker compose down -v --rmi local
	cd frontend && rm -rf dist node_modules

## Quick status
status:
	docker compose ps

## Open app in browser (Linux)
open:
	xdg-open http://localhost:8090 2>/dev/null || open http://localhost:8090

## Lab: prompt injection (puerto 5001)
lab-pi:
	docker compose up -d lab-prompt-injection
	@echo "Lab disponible en http://localhost:5001 (necesitas exponer puerto manualmente)"

## Mostrar credenciales por defecto del curso
creds:
	@echo "Código de acceso por defecto: secuai2026"
	@echo "Cámbialo en .env (ACCESS_CODE)"
