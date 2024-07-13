import os
import json
import asyncio
from fastapi import FastAPI, HTTPException, Request
import paho.mqtt.client as mqtt
from prisma import Prisma
from pydantic import BaseModel, validator
from datetime import datetime
import logging
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import api_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
db = Prisma()

# CORS configuration
origins = [
    "http://localhost:3000",  # Adjust this according to your frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mqtt_broker = os.getenv('MQTT_BROKER', '127.0.0.1')
mqtt_port = int(os.getenv('MQTT_PORT', 1883))

mqtt_topics = {
    'telemetry': 'turtlebot3/telemetry',
    'battery': 'turtlebot3/battery',
    'camera': 'turtlebot3/camera',
    'lidar': 'turtlebot3/lidar',
    'recovery': 'turtlebot3/recovery',
    'waypoint': 'turtlebot3/waypoint',
    'map': 'turtlebot3/map'
}

class TelemetryCreate(BaseModel):
    turtleBotId: int
    timestamp: str
    x: float
    y: float
    heading: float

    @validator('timestamp')
    def validate_timestamp(cls, value):
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("Invalid timestamp format, should be ISO-8601")
        return value

class BatteryCreate(BaseModel):
    turtleBotId: int
    timestamp: str
    voltage: float
    current: float
    percentage: float

    @validator('timestamp')
    def validate_timestamp(cls, value):
        try:
            datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("Invalid timestamp format, should be ISO-8601")
        return value

async def insert_telemetry(data):
    try:
        await db.telemetry.create(data=data)
    except Exception as e:
        logger.error(f"Failed to insert telemetry: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to insert telemetry: {e}")

async def insert_battery(data):
    try:
        await db.battery.create(data=data)
    except Exception as e:
        logger.error(f"Failed to insert battery: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to insert battery: {e}")

def on_connect(client, userdata, flags, rc):
    logger.info("Connected with result code %s", rc)
    for topic in mqtt_topics.values():
        client.subscribe(topic)
        logger.info("Subscribed to topic: %s", topic)

def convert_unix_to_iso(unix_timestamp):
    try:
        return datetime.utcfromtimestamp(int(unix_timestamp) / 1e9).isoformat()
    except ValueError:
        raise ValueError("Invalid Unix timestamp")

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        topic_key = list(mqtt_topics.keys())[list(mqtt_topics.values()).index(msg.topic)]

        if topic_key == 'telemetry':
            if 'timestamp' in data:
                data['timestamp'] = convert_unix_to_iso(data['timestamp'])
            telemetry = TelemetryCreate(**data)
            asyncio.create_task(insert_telemetry(telemetry.dict()))
        elif topic_key == 'battery':
            if 'timestamp' in data:
                data['timestamp'] = convert_unix_to_iso(data['timestamp'])
            battery = BatteryCreate(**data)
            asyncio.create_task(insert_battery(battery.dict()))
        else:
            logger.info(f"Received message on topic {msg.topic}: {data}")
    except Exception as e:
        logger.error(f"Failed to process message: {e}")
        logger.error(f"Received data: {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)

@app.on_event("startup")
async def startup_event():
    await db.connect()
    client.loop_start()
    logger.info("Application startup complete.")

@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()
    client.loop_stop()
    logger.info("Application shutdown complete.")

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
