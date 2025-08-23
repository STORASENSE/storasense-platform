import time
import os
from dotenv import load_dotenv
from frontend_test import login, check_backend, init_db
from mqtt import check_mqtt
from frontend_test import evaluate_results
from selenium.common.exceptions import WebDriverException

from frontend_test import get_db_connection


def main():
    start_time = time.time()
    end_time = start_time + int(os.getenv("TEST_DURATION", 60))
    init_db()

    while time.time() < end_time:
        try:
            time.sleep(int(os.getenv("TEST_INTERVAL")))
            driver = login()
            check_backend(driver)
            driver.quit()
        except WebDriverException:
            with get_db_connection() as connection:
                connection.execute(
                    "INSERT INTO test_data (FRONTEND_ALIVE, BACKEND_ALIVE) VALUES (0, 0)"
                )

    evaluate_results(start_time, end_time)

    check_mqtt()


if __name__ == "__main__":
    load_dotenv(dotenv_path="../../.env")
    start = time.time()
    main()
    print(time.time() - start)
