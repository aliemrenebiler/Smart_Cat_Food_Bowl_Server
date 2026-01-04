import asyncio
import os

from amqtt.broker import Broker

from utils.logging_utils import get_logger

logger = get_logger(__name__)

MQTT_HOST = os.getenv("MQTT_HOST", "0.0.0.0")
MQTT_TCP_PORT = int(os.getenv("MQTT_TCP_PORT", "1883"))
MQTT_WS_PORT = int(os.getenv("MQTT_WS_PORT", "8001"))

config = {
    "listeners": {
        "default": {
            "type": "tcp",
            "bind": f"{MQTT_HOST}:{MQTT_TCP_PORT}",
        },
        "ws": {
            "type": "ws",
            "bind": f"{MQTT_HOST}:{MQTT_WS_PORT}",
        },
    },
    "timeout_disconnect_delay": 2,
    "plugins": {
        "amqtt.plugins.authentication.AnonymousAuthPlugin": {
            "allow_anonymous": True,
        },
    },
}


async def start_mqtt_broker():
    broker = Broker(config)
    try:
        await broker.start()
        logger.info("MQTT (TSP) running on **%s:%s**", MQTT_HOST, MQTT_TCP_PORT)
        logger.info("MQTT (WS) running on **%s:%s**", MQTT_HOST, MQTT_WS_PORT)

        while True:
            await asyncio.sleep(1)
    except Exception as exc:  # pylint: disable=broad-except
        logger.error("Error in MQTT Broker: %s", exc)
