import asyncio
import os

import paho.mqtt.client as mqtt

from db.database import SessionLocal
from db.services.device_service import DeviceService


def handle_device_info_message(msg: mqtt.MQTTMessage):
    topic_parts = msg.topic.split("/")
    if (
        len(topic_parts) == 3
        and topic_parts[0] == "devices"
        and topic_parts[2] == "info"
    ):
        error = None
        device_id = topic_parts[1]

        db = SessionLocal()
        try:
            device_service = DeviceService(db)
            device_service.create_device_data(
                device_id, msg.topic, msg.payload.decode()
            )
        except Exception as exc:  # pylint: disable=broad-except
            error = exc
        finally:
            db.close()

        if error:
            raise error


def on_message(_client, _userdata, msg: mqtt.MQTTMessage):
    handle_device_info_message(msg)


async def start_mqtt_listener():
    MQTT_HOST = os.getenv("MQTT_HOST", "0.0.0.0")
    MQTT_TCP_PORT = int(os.getenv("MQTT_TCP_PORT", "1883"))

    client = mqtt.Client()
    client.on_message = on_message

    # Wait for broker to be ready
    connected = False
    while not connected:
        try:
            client.connect(MQTT_HOST, MQTT_TCP_PORT, 60)
            connected = True
        except Exception:  # pylint: disable=broad-except
            await asyncio.sleep(1)

    client.subscribe("devices/+/info")

    # Run paho-mqtt loop in a non-blocking way for asyncio
    while True:
        client.loop(0.1)
        await asyncio.sleep(0.1)
