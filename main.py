import asyncio
import os
import uvicorn
from api.app import app
from mqtt.broker import start_mqtt_broker


async def main():
    # Start MQTT Broker
    _ = asyncio.create_task(start_mqtt_broker())

    # API Configuration from environment variables
    api_host = os.getenv("API_HOST", "0.0.0.0")
    api_port = int(os.getenv("API_PORT", "8000"))

    # Start FastAPI API
    config = uvicorn.Config(app, host=api_host, port=api_port, log_level="info")
    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())
