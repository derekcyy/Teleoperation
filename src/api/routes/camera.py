# src/api/routes/battery.py
from fastapi import APIRouter
from paho.mqtt.publish import single as mqtt_publish
from database import db
import json

router = APIRouter()

@router.get("/turtlebot3/camera", tags=["turtlebot3"])
async def get_camera():
    camera = await db.camera.findFirst() # gets most recently created entry for camera
    return {"camera": camera}
