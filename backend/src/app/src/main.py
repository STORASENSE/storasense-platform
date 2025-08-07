import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from backend.src.app.shared import logging

# ... DB imports ...
from backend.src.app.src.shared.database.model_discovery import discover_models
from backend.src.app.src.db_init import initialize_database

# ... Router imports ...
# from .services.users.router import router as users_router
# from .services.storages.router import router as storages_router
from backend.src.app.src.services.measurements.router import (
    router as measurements_router,
)
from backend.src.app.src.services.sensors.router import (
    router as sensors_router,
)
from backend.src.app.src.services.auth.router import (
    router as auth_router,
)

discover_models()
load_dotenv()

_logger = logging.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for FastAPI.
    Initializes the database at startup and cleans up resources at shutdown.
    """
    _logger.info("Initializing database...")
    initialize_database()
    _logger.info("Database initialization completed successfully!")
    yield


app = FastAPI(
    title="STORASENSE-Platform-Backend API",
    version="1.0.0",
    description="STORASENSE-Platform-Backend API",
    lifespan=lifespan,
)

# app.include_router(users_router)
# app.include_router(storages_router)
app.include_router(measurements_router)
app.include_router(sensors_router)
app.include_router(auth_router)

app.add_middleware(SessionMiddleware, secret_key=os.environ.get("SECRET_KEY"))


@app.get("/health", tags=["Root"])
def read_root():
    """
    # checks if the API is running
    """
    return {
        "status": "ok",
        "message": "welcome to STORASENSE-Platform-Backend API!",
    }


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)
