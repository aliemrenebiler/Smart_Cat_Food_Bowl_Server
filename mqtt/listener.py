import asyncio
import os
import paho.mqtt.client as mqtt
from db.database import SessionLocal
from db.services.device_service import DeviceService


def on_message(client, userdata, msg):  # pylint: disable=unused-argument
    # Topic format: devices/<device_id>/info
    parts = msg.topic.split("/")
    if len(parts) >= 2:
        device_id = parts[1]
        db = SessionLocal()
        try:
            device_service = DeviceService(db)
            device_service.create_device_data(
                device_id, msg.topic, msg.payload.decode()
            )
        except Exception as e:  # pylint: disable=broad-except
            print(f"Error saving MQTT data: {e}", flush=True)
        finally:
            db.close()


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
