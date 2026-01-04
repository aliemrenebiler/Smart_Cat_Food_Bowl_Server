# Smart Cat Food Bowl Server

This project provides a FastAPI-based API and an MQTT client that share a local SQLite database.

## Features

-   **Built-in MQTT Broker**: Runs its own MQTT server using `amqtt`.
-   **FastAPI API**: Serves data from the database.
-   **MQTT Client**: Listens for messages on the local broker and saves them to the database.
-   **Shared Database**: Uses SQLAlchemy with SQLite for local storage.

## Setup

1. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Configure environment variables (optional, defaults are used):

    - `DATABASE_URL`: SQLite database URL (default: `sqlite:///./sql_app.db`).
    - `MQTT_TCP_PORT`: TCP Port for the built-in MQTT broker (default: `1883`).
    - `MQTT_WS_PORT`: WS Port for the built-in MQTT broker (default: `8001`).
    - `API_HOST`: Host for the FastAPI API (default: `localhost`).
    - `API_PORT`: Port for the FastAPI API (default: `8000`).

3. Run the application:
    ```bash
    python main.py
    ```

## API Endpoints

-   `GET /`: Welcome message.
-   `POST /devices`: Register a new device (JSON: `{"name": "...", "model": "..."}`).
-   `GET /devices`: Get all registered devices.
-   `DELETE /devices/{unique_id}`: Remove a device.
-   `GET /devices/{unique_id}`: Get data logs for a specific device.
-   `GET /devices/{unique_id}/latest`: Get latest data log for a specific device.
-   `POST /devices/{unique_id}/control`: Send an MQTT message to a device.
