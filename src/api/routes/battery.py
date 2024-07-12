# src/api/routes/battery.py
from fastapi import APIRouter
from paho.mqtt.publish import single as mqtt_publish
from database import db
import json

router = APIRouter()

@router.get("/turtlebot3/battery", tags=["turtlebot3"])
async def get_battery():
    battery = await db.battery.findFirst() # gets most recently created entry for battery
    return {"status": battery}
