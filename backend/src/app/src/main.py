import uvicorn
from fastapi import FastAPI

# from .services.users.router import router as users_router
# from .services.storages.router import router as storages_router
from backend.src.app.src.services.measurements.router import (
    router as measurements_router,
)
from backend.src.app.src.services.sensors.router import (
    router as sensors_router,
)

app = FastAPI(
    title="STORASENSE-Platform-Backend API",
    version="1.0.0",
    description="STORASENSE-Platform-Backend API for IoT-Datamanagement",
)

# app.include_router(users_router)
# app.include_router(storages_router)
app.include_router(measurements_router)
app.include_router(sensors_router)


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
    uvicorn.run(app, host="localhost", port=8000)
