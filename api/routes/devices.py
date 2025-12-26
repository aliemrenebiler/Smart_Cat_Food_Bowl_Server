import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from paho.mqtt import publish
from sqlalchemy.orm import Session

from api.models.device_models import (
    CreateDeviceRequest,
    GetDeviceResponse,
)
from db.services.device_service import DeviceService
from db.database import get_db


def get_device_service(db: Session = Depends(get_db)) -> DeviceService:
    return DeviceService(db)


router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=GetDeviceResponse)
def create_device(
    device: CreateDeviceRequest,
    device_service: DeviceService = Depends(get_device_service),
):
    return device_service.create_device(device.name)


@router.get("/", response_model=List[GetDeviceResponse])
def list_devices(device_service: DeviceService = Depends(get_device_service)):
    return device_service.get_all_devices()


@router.delete("/{device_id}")
def delete_device(
    device_id: str, device_service: DeviceService = Depends(get_device_service)
):
    try:
        return device_service.delete_device(device_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("/{device_id}")
def get_device_data(
    device_id: str, device_service: DeviceService = Depends(get_device_service)
):
    return device_service.get_device_data(device_id)


@router.post("/{device_id}/control")
def control_device(device_id: str, command: str):
    mqtt_host = os.getenv("MQTT_HOST", "localhost")
    mqtt_port = int(os.getenv("MQTT_PORT", "1883"))

    full_topic = f"devices/{device_id}/control"

    try:
        publish.single(full_topic, command, hostname=mqtt_host, port=mqtt_port)
        return {"message": f"Command sent to {full_topic}", "command": command}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
