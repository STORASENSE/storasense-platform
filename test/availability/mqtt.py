from datetime import datetime, timedelta, timezone
from test.rest_functionality.rest_methods import get_request
import os


def write_sensor_report(sensor_id: str, outages: list, test_length: timedelta):
    with open(os.getenv("AVAILABILITY_REPORT_FILE"), "a") as file:
        outages.reverse()
        file.write(f"\nSensor ID: {sensor_id}\n")
        if len(outages) == 0:
            file.write("No outages detected\n")
        else:
            if len(outages) == 1:
                file.write("Detected 1 outage:\n")
            else:
                file.write(f"Detected {len(outages)} outages:\n")
            for outage in outages:
                file.write(
                    f"Start: {datetime.fromtimestamp(outage[0]).isoformat()} "
                )
                file.write(
                    f"End: {datetime.fromtimestamp(outage[1]).isoformat()} "
                )
                file.write(f"Duration: {str(timedelta(seconds=outage[2]))}\n")
            outage_duration = sum([outage[2] for outage in outages])
            outage_quota = outage_duration / test_length.total_seconds()
            file.write(
                f"Total outage duration: {str(timedelta(seconds=outage_duration))}\n"
            )
            file.write(f"Availability: {(1 - outage_quota) * 100}%\n")


def check_for_outage(first: float, second: float, outage: list):
    if second - first > int(os.getenv("AVAILABILITY_TEST_MAX_INTERVAL")):
        outage.append((first, second, second - first))
    return outage


def check_sensor(sensor_id: str, start_time: float, end_time: float):  #
    measurements = get_request(
        f"measurements/{sensor_id}/filter?max_date={start_time}"
    )["measurements"]
    if len(measurements) == 0:
        write_sensor_report(
            sensor_id,
            [(start_time, end_time, int(end_time - start_time))],
            timedelta(end_time - start_time),
        )

    creation_dates = [
        measurements["created_at"] for measurements in measurements
    ]
    creation_dates = [
        datetime.fromisoformat(creation_date)
        .replace(tzinfo=timezone.utc)
        .timestamp()
        for creation_date in creation_dates
    ]
    print(f"creation_dates: {creation_dates}")
    outages = []
    for index, creation_date in enumerate(creation_dates):
        if index == 0:
            outages = check_for_outage(creation_date, end_time, outages)
        else:
            outages = check_for_outage(
                creation_date, creation_dates[index - 1], outages
            )
    write_sensor_report(
        sensor_id, outages, timedelta(seconds=end_time - start_time)
    )


def check_mqtt(start_time: float, end_time: float):
    """
    Checks if the MQTT client sent the correct data
    """

    storage_ids = [
        storage["id"] for storage in get_request("storages/myStorages")
    ]

    sensor_ids = []
    for storage_id in storage_ids:
        sensor_ids += [
            sensor["id"]
            for sensor in get_request(f"sensors/byStorageId/{storage_id}")
        ]
    sensor_id = sensor_ids[0]
    check_sensor(sensor_id, start_time, end_time)
