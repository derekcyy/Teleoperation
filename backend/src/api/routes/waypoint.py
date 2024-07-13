# src/api/routes/waypoint.py
from fastapi import APIRouter
from paho.mqtt.publish import single as mqtt_publish
import json

router = APIRouter()

@router.post("/waypoint", tags=["turtlebot3"])
async def post_waypoint(data: dict):
    payload = json.dumps(data)
    mqtt_publish('turtlebot3/waypoint', payload, hostname='127.0.0.1')
    return {"status": "Waypoint data published to MQTT"}
