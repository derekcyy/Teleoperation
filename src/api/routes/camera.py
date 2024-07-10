# src/api/routes/battery.py
from fastapi import APIRouter
from paho.mqtt.publish import single as mqtt_publish
import json

router = APIRouter()

@router.post("/")
async def post_battery(data: dict):
    payload = json.dumps(data)
    mqtt_publish('turtlebot3/battery', payload, hostname='127.0.0.1')
    return {"status": "Battery data published to MQTT"}
