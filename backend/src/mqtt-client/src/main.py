import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv


def main():
    def on_subscribe(client, userdata, mid, reason_code_list, properties):
        print("Subscribed")

    def on_message(client, userdata, message):
        print(str(message.payload.decode("utf-8")))

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}.")
        else:
            client.subscribe("sensor/temperature")

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


if __name__ == "__main__":
    load_dotenv(dotenv_path="../../../../.env")
    main()
