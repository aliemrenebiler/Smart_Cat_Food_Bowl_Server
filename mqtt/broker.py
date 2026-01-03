import asyncio
import os
from amqtt.broker import Broker

MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

config = {
    "listeners": {
        "default": {
            "type": "tcp",
            "bind": f"0.0.0.0:{MQTT_PORT}",
        }
    },
}


async def start_mqtt_broker():
    broker = Broker(config)
    try:
        await broker.start()
        print(f"MQTT Broker started on port {MQTT_PORT}")
        # Keep the broker running
        while True:
            await asyncio.sleep(1)
    except Exception as exc:  # pylint: disable=broad-except
        print(f"Error starting MQTT Broker: {exc}")
