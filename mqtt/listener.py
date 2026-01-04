import asyncio
import os

import paho.mqtt.client as mqtt

from db.database import SessionLocal
from db.services.device_service import DeviceService
from utils.logging_utils import get_logger


logger = get_logger(__name__)


def handle_device_info_message(msg: mqtt.MQTTMessage):
    topic_parts = msg.topic.split("/")
    if (
        len(topic_parts) == 3
        and topic_parts[0] == "devices"
        and topic_parts[2] == "info"
    ):
        # device_id = topic_parts[1] <--- ORIGINAL ----

        db = SessionLocal()
        try:
            device_service = DeviceService(db)

            # ---- REMOVE THESE LATER ----
            devices = device_service.get_all_devices()
            if not devices:
                raise ValueError("No devices found in the database.")
            device = devices[0]
            device_id = str(device.id)
            # ---- REMOVE THESE LATER ----

            device_service.create_device_data(
                device_id, msg.topic, msg.payload.decode()
            )
        except Exception as exc:  # pylint: disable=broad-except
            logger.error("Failed to handle device info message: %s", exc)
        finally:
            db.close()


def on_message(_client, _userdata, msg: mqtt.MQTTMessage):
    logger.info("Message from topic %s: %s", msg.topic, msg.payload.decode())
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
