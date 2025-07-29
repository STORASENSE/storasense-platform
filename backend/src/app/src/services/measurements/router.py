from uuid import UUID

from fastapi import Depends

from backend.src.app.src.main import app
from backend.src.app.src.services.measurements.service import (
    MeasurementService,
    inject_measurement_service,
)
from backend.src.app.src.services.sensors.schemas import (
    CreateMeasurementRequest,
)
from backend.src.app.src.shared.database.pagination import PageRequest


@app.get("/measurements/{sensor_id}")
def find_sensor_measurements(
    sensor_id: UUID,
    measurement_service: MeasurementService = Depends(
        inject_measurement_service
    ),
):
    page_request = PageRequest(0, 100)
    measurements = measurement_service.find_all_by_sensor_id(
        sensor_id, page_request
    )
    result = []
    for measurement in measurements:
        result.append(
            {"id": measurement.id, "created_at": measurement.created_at}
        )
    return result


@app.post("/measurements/{sensor_id}")
def create_measurement(
    sensor_id: UUID,
    request: CreateMeasurementRequest,
    measurement_service: MeasurementService = Depends(
        inject_measurement_service
    ),
):
    measurement_service.create_measurement(sensor_id, request)
