import time
from dotenv import load_dotenv
from test.availability.mqtt import check_mqtt
from test.availability.frontend_test import (
    login,
    check_backend,
    get_db_connection,
    init_db,
    evaluate_results,
)
from selenium.common.exceptions import WebDriverException
import os
import logging


def main(logger):
    start_time = time.time()
    end_time = start_time + int(os.getenv("AVAILABILITY_TEST_DURATION"))
    init_db()

    while time.time() < end_time:
        try:
            time.sleep(int(os.getenv("AVAILABILITY_TEST_INTERVAL")))
            logger.info("Starting Frontend Check")
            driver = login()
            check_backend(driver)
            driver.quit()
            logger.info("Frontend Check completed")
        except WebDriverException as e:
            logger.error(f"WebDriverException occurred: {e}")
            with get_db_connection() as connection:
                connection.execute(
                    "INSERT INTO test_data (FRONTEND_ALIVE, BACKEND_ALIVE) VALUES (0, 0)"
                )

    evaluate_results(start_time, end_time)
    report_file = os.getenv("AVAILABILITY_REPORT_FILE")
    os.makedirs(os.path.dirname(report_file), exist_ok=True)
    with open(os.getenv("AVAILABILITY_REPORT_FILE"), "a") as file:
        file.write("\nMQTT Availability Report\n")

    check_mqtt(start_time, end_time)


if __name__ == "__main__":
    if __name__ == "__main__":
        load_dotenv(dotenv_path="../../.env")
        start = time.time()
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        main(logger)
        logger.info(time.time() - start)
