"""FastAPI application entry point."""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import create_tables
from app.middleware.rate_limit import RateLimitMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.routers import dashboard, ingest, projects, webhooks
from app.utils.logging_config import configure_logging

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup / shutdown lifecycle."""
    logger.info("Starting HookBox")
    create_tables()
    logger.info("Database tables ensured")
    yield
    logger.info("Shutting down HookBox")

app = FastAPI(
    title="HookBox",
    description="Webhook inbox and replay service",
    version="0.1.0",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(RequestIDMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static assets
app.mount("/static", StaticFiles(directory="static"), name="static")

# Routers
app.include_router(ingest.router, tags=["ingestion"])
app.include_router(projects.router, prefix="/api/v1", tags=["projects"])
app.include_router(webhooks.router, prefix="/api/v1", tags=["webhooks"])
app.include_router(dashboard.router, tags=["dashboard"])

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Simple health endpoint."""
    return {"status": "healthy", "version": "0.1.0"}

@app.get("/")
async def root() -> dict[str, str]:
    """Root redirects to dashboard."""
    return {"message": "HookBox API", "docs": "/docs"}
