# src/api/routes/lidar.py
from fastapi import APIRouter
from paho.mqtt.publish import single as mqtt_publish
import json

router = APIRouter()

@router.post("/")
async def post_lidar(data: dict):
    payload = json.dumps(data)
    mqtt_publish('turtlebot3/lidar', payload, hostname='127.0.0.1')
    return {"status": "Lidar data published to MQTT"}
