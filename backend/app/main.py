import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.security import limiter, SECURITY_HEADERS
from app.routers import modules, files, search, auth, game

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("SecuAI API starting up")
    yield
    logger.info("SecuAI API shutting down")


app = FastAPI(
    title="SecuAI — Curso de Securización de IA",
    description=(
        "API del curso experto en securización de IA y uso de IA para securización. "
        "10 módulos + taller para charlas con parte práctica."
    ),
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS — only allow the frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8090",
        "http://frontend",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Accept"],
)

# Routers
app.include_router(modules.router)
app.include_router(files.router)
app.include_router(search.router)
app.include_router(auth.router)
app.include_router(game.router)


@app.get("/api/health", tags=["health"])
async def health_check():
    return JSONResponse(
        content={"status": "ok", "service": "secuai-api"},
        headers=SECURITY_HEADERS,
    )


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Not found"},
        headers=SECURITY_HEADERS,
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    logger.error("Internal server error: %s", exc)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
        headers=SECURITY_HEADERS,
    )
