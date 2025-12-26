import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from paho.mqtt import publish
from sqlalchemy.orm import Session

from api.models.device_models import (
    CreateDeviceRequest,
    GetDeviceResponse,
)
from db.database import get_db
from db.models import Device, DeviceData

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=GetDeviceResponse)
def create_device(device: CreateDeviceRequest, db: Session = Depends(get_db)):
    new_device = Device(name=device.name)
    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device


@router.get("/", response_model=List[GetDeviceResponse])
def list_devices(db: Session = Depends(get_db)):
    return db.query(Device).all()


@router.delete("/{device_id}")
def delete_device(device_id: str, db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(db_device)
    db.commit()
    return {"message": "Device deleted"}


@router.get("/{device_id}")
def get_device_data(device_id: str, db: Session = Depends(get_db)):
    return db.query(DeviceData).filter(DeviceData.device_id == device_id).all()


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
