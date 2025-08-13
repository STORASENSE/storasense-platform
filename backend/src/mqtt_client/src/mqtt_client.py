import json
import os

import paho.mqtt.client as mqtt
from database import get_db_connection

from logger import get_logger

_logger = get_logger(__name__)


def get_topics():
    topics = os.getenv("MQTT_TOPICS", "").split(",")

    topic_tuples = []
    for topic in topics:
        topic_tuples.append((topic, int(os.getenv("MQTT_QOS", "0"))))
    return topic_tuples


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    _logger.info("Subscribed")


def on_message(client, userdata, message):
    sensor_id = message.topic.split("/")[-1]
    message_data = json.loads(message.payload.decode("utf-8"))

    value = message_data["value"][0]
    timestamp = message_data["timestamp"]
    unit = message_data["meta"]["unit"]
    _logger.info(f"received {value}")
    with get_db_connection() as connection:
        connection.execute(
            """
        INSERT INTO sensor_data (sensor_id, value,timestamp,unit) values (?,?,?,?)""",
            (sensor_id, value, timestamp, unit),
        )
    connection.close()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        _logger.error(f"Failed to connect: {reason_code}.")
    else:
        client.subscribe(get_topics())


def start_mqtt_client():
    mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    mqtt_client.on_subscribe = on_subscribe
    mqtt_client.on_message = on_message
    mqtt_client.on_connect = on_connect
    mqtt_client.username_pw_set(
        os.getenv("MQTT_USER_NAME"), password=os.getenv("MQTT_USER_PASSWORD")
    )
    mqtt_client.connect(
        os.getenv("MQTT_BROKER_ADRESS"),
        port=int(os.getenv("MQTT_BROKER_PORT")),
    )
    mqtt_client.loop_forever()
