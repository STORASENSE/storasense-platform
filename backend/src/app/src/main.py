from fastapi import FastAPI

from backend.src.app.src.shared.database.model_discovery import discover_models

# from .services.users.router import router as users_router
# from .services.storages.router import router as storages_router
# from backend.src.app.src.services.measurements.router import \
#   router as measurements_router


discover_models()

app = FastAPI(
    title="STORASENSE-Platform-Backend API",
    version="1.0.0",
    description="STORASENSE-Platform-Backend API for IoT-Datamanagement",
)

# app.include_router(users_router)
# app.include_router(storages_router)
# app.include_router(measurements_router)


@app.get("/health", tags=["Root"])
def read_root():
    """
    # checks if the API is running
    """
    return {
        "status": "ok",
        "message": "welcome to STORASENSE-Platform-Backend API!",
    }
