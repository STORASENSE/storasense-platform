import os
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from backend.src.app.src.shared.logger import (
    get_logger,
    add_request_middleware,
)

# ... DB imports ...
from backend.src.app.src.shared.database.model_discovery import discover_models
from backend.src.app.src.db_init import initialize_database

# ... Router imports ...
from .services.users.router import router as users_router

from backend.src.app.src.services.measurements.router import (
    router as measurements_router,
)
from backend.src.app.src.services.sensors.router import (
    router as sensors_router,
)
from backend.src.app.src.services.storages.router import (
    router as storages_router,
)

discover_models()
load_dotenv()

_logger = get_logger(__name__)

CLIENT_ID = os.environ.get("KEYCLOAK_CLIENT_ID")
if not CLIENT_ID:
    raise RuntimeError(
        "Keycloak is not configured correctly. Please check environment variables."
    )


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
    _logger.info("Shutting down application...")


app = FastAPI(
    title="STORASENSE-Platform-Backend API",
    version="1.0.0",
    description="STORASENSE-Platform-Backend API",
    lifespan=lifespan,
    swagger_ui_init_oauth={"clientId": CLIENT_ID, "appName": "Storasense API"},
)

add_request_middleware(app)

app.include_router(users_router)
app.include_router(measurements_router)
app.include_router(sensors_router)
app.include_router(storages_router)

# configure CORS-middleware
origins = [
    "https://storasense.de",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
