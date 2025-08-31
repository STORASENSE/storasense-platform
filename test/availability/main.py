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


def main():
    start_time = time.time()
    end_time = start_time + int(os.getenv("AVAILABILITY_TEST_DURATION"))
    init_db()

    while time.time() < end_time:
        try:
            time.sleep(int(os.getenv("AVAILABILITY_TEST_INTERVAL")))
            driver = login()
            check_backend(driver)
            driver.quit()
        except WebDriverException:
            with get_db_connection() as connection:
                connection.execute(
                    "INSERT INTO test_data (FRONTEND_ALIVE, BACKEND_ALIVE) VALUES (0, 0)"
                )

    evaluate_results(start_time, end_time)
    with open(os.getenv("AVAILABILITY_REPORT_FILE"), "a") as file:
        file.write("\nMQTT Availability Report\n")

    check_mqtt(start_time, end_time)


if __name__ == "__main__":
    load_dotenv(dotenv_path="../../.env")
    start = time.time()
    main()
    print(time.time() - start)
