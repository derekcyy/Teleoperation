import os
import json
import asyncio
from fastapi import FastAPI, HTTPException
import paho.mqtt.client as mqtt
from prisma import Prisma
from pydantic import BaseModel, validator
from datetime import datetime

app = FastAPI()
db = Prisma()

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

class Telemetry(BaseModel):
    turtleBotId: int
    timestamp: str
    x: float
    y: float
    heading: float

    @validator('timestamp')
    def validate_timestamp(cls, value):
        try:
            datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Invalid timestamp format, should be ISO-8601")
        return value

async def insert_telemetry(data):
    try:
        await db.telemetry.create(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert telemetry: {e}")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    for topic in mqtt_topics.values():
        client.subscribe(topic)

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
            telemetry = Telemetry(**data)
            asyncio.run(insert_telemetry(telemetry.dict()))
        else:
            print(f"Received message on topic {msg.topic}: {data}")
    except Exception as e:
        print(f"Failed to process message: {e}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)

@app.on_event("startup")
async def startup_event():
    await db.connect()
    client.loop_start()

@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()
    client.loop_stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
