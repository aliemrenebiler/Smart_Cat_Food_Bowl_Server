import asyncio
import os
import paho.mqtt.client as mqtt
from db.database import SessionLocal
from db.services.device_service import DeviceService


def on_device_info_message(device_id: str, topic: str, payload: str):
    db = SessionLocal()
    try:
        device_service = DeviceService(db)
        device_service.create_device_data(device_id, topic, payload)
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error saving MQTT data: {e}", flush=True)
    finally:
        db.close()


def on_message(_client, _userdata, msg: mqtt.MQTTMessage):
    topic_parts = msg.topic.split("/")

    if (
        len(topic_parts) == 3
        and topic_parts[0] == "devices"
        and topic_parts[2] == "info"
    ):
        device_id = topic_parts[1]
        on_device_info_message(device_id, msg.topic, msg.payload.decode())


async def start_mqtt_listener():
    mqtt_host = os.getenv("MQTT_HOST", "localhost")
    mqtt_port = int(os.getenv("MQTT_PORT", "1883"))

    client = mqtt.Client()
    client.on_message = on_message

    # Wait for broker to be ready
    connected = False
    while not connected:
        try:
            client.connect(mqtt_host, mqtt_port, 60)
            connected = True
        except Exception:  # pylint: disable=broad-except
            await asyncio.sleep(1)

    client.subscribe("devices/+/info")

    # Run paho-mqtt loop in a non-blocking way for asyncio
    while True:
        client.loop(0.1)
        await asyncio.sleep(0.1)
