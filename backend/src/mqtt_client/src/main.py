import threading

from database import init_db
from dotenv import load_dotenv
from mqtt_client import start_mqtt_client
from rest_client import start_rest_client


def main():
    load_dotenv(dotenv_path="../../../../.env")
    init_db()
    stop_event = threading.Event()
    threading.Thread(target=start_rest_client, args=(stop_event,)).start()
    start_mqtt_client()
    stop_event.set()


if __name__ == "__main__":
    main()
