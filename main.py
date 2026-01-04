import asyncio
import os
import uvicorn

from api.app import app
from mqtt.broker import start_mqtt_broker
from mqtt.listener import start_mqtt_listener
from utils.logging_utils import configure_logging


async def main():
    configure_logging()

    # Start MQTT Broker
    _ = asyncio.create_task(start_mqtt_broker())

    # Start MQTT Listener (to save data to DB)
    _ = asyncio.create_task(start_mqtt_listener())

    # API Configuration from environment variables
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))

    # Start FastAPI API
    config = uvicorn.Config(app, host=API_HOST, port=API_PORT, log_level="info")
    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
