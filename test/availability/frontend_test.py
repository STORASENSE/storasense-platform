import time
from datetime import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import sqlite3


def login():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(2)
    driver.get("https://storasense.de")
    time.sleep(0.5)
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()

    username_input = driver.find_element(By.ID, "username")
    username_input.send_keys(os.getenv("TEST_USER"))
    password_input = driver.find_element(By.ID, "password")
    password_input.send_keys(os.getenv("TEST_USER_PASSWORD"))
    password_input.send_keys(Keys.RETURN)
    return driver


def get_db_connection():
    return sqlite3.connect(os.getenv("TEST_DB_NAME"))


def init_db():
    if os.path.exists(os.getenv("TEST_DB_NAME")):
        os.remove(os.getenv("TEST_DB_NAME"))
    connection = get_db_connection()
    with connection:
        connection.execute(
            """
            CREATE TABLE test_data(
                FRONTEND_ALIVE INTEGER,
                BACKEND_ALIVE INTEGER,
                TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
            """
        )


def check_backend(driver):
    time.sleep(1)
    backend_online = driver.find_elements(By.ID, "Backend_Online")
    backend_offline = driver.find_elements(By.ID, "Backend_Offline")
    frontend_alive = 0
    backend_alive = 0
    if len(backend_online) + len(backend_offline) > 0:
        frontend_alive = 1
    if len(backend_online) > 0:
        backend_alive = 1
    with get_db_connection() as connection:
        connection.execute(
            "INSERT INTO test_data (FRONTEND_ALIVE, BACKEND_ALIVE) VALUES (?, ?)",
            (frontend_alive, backend_alive),
        )


def evaluate_results(start_time, end_time):
    start_time = datetime.fromtimestamp(start_time).isoformat()
    end_time = datetime.fromtimestamp(end_time).isoformat()

    with get_db_connection() as connection:
        frontend_alive = connection.execute(
            "SELECT COUNT(*) FROM test_data WHERE FRONTEND_ALIVE =1"
        ).fetchone()[0]
        backend_alive = connection.execute(
            "SELECT COUNT(*) FROM test_data WHERE BACKEND_ALIVE =1"
        ).fetchone()[0]
        total_checks = connection.execute(
            "SELECT COUNT(*) FROM test_data"
        ).fetchone()[0]
        with open(os.getenv("AVAILABILITY_REPORT_FILE"), "a") as file:
            file.write(f"Test run from {start_time} to {end_time}\n")
            file.write(
                f"Frontend able to login: {frontend_alive} out of {total_checks}  {frontend_alive / total_checks * 100}%\n"
            )
            file.write(
                f"Backend reachable through frontend: {backend_alive} out of {total_checks}  {backend_alive / total_checks * 100}%\n"
            )
            file.write("\n")
