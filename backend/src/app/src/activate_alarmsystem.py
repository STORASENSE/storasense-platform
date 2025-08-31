# import os
#
# from backend.src.app.src.services.sensors.repository import SensorRepository
# from backend.src.app.src.services.sensors.service import (
#     inject_sensor_service,
# )
# from backend.src.app.src.shared.database.engine import open_session
#
#
# def activate_alarmsystem_after_shutdown():
#     """
#     Script that activates the alarm system after the application shutdown.
#     """
#     _environment = os.getenv("ENVIRONMENT")  # TEST / DEV / PROD
#
#     if _environment == "TEST" or _environment == "DEV":
#         return
#
#     session = open_session()
#     sensor_repository = SensorRepository(session)
#     sensor_service = inject_sensor_service(session)
#     try:
#         sensor_service.push_all_sensors_to_kafka()
#     except Exception as e:
#         raise RuntimeError(
#             "Failed to activate alarm system after shutdown."
#         ) from e
