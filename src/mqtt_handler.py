import paho.mqtt.client as mqtt
import json
import logging
from .database import db
from .models import TelemetryCreate, BatteryCreate, CameraCreate, LidarCreate

logging.basicConfig(level=logging.INFO)

def on_connect(client, userdata, flags, rc):
    logging.info(f"Connected with result code {rc}")
    client.subscribe("turtlebot3/telemetry")
    client.subscribe("turtlebot3/battery")
    client.subscribe("turtlebot3/camera")
    client.subscribe("turtlebot3/lidar")

def on_message(client, userdata, msg):
    logging.info(f"Received message: {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        if msg.topic == "turtlebot3/telemetry":
            telemetry_data = TelemetryCreate(
                turtleBotId=data['turtleBotId'],
                timestamp=data['timestamp'],
                x=data['position']['x'],
                y=data['position']['y'],
                heading=data['orientation']['z']
            )
            insert_telemetry(telemetry_data)
        elif msg.topic == "turtlebot3/battery":
            battery_data = BatteryCreate(
                turtleBotId=data['turtleBotId'],
                timestamp=data['timestamp'],
                voltage=data['voltage'],
                current=data['current'],
                percentage=data['percentage']
            )
            insert_battery(battery_data)
        elif msg.topic == "turtlebot3/camera":
            camera_data = CameraCreate(
                turtleBotId=data['turtleBotId'],
                timestamp=data['timestamp'],
                image=data['image']
            )
            insert_camera(camera_data)
        elif msg.topic == "turtlebot3/lidar":
            lidar_data = LidarCreate(
                turtleBotId=data['turtleBotId'],
                timestamp=data['timestamp'],
                ranges=data['ranges']
            )
            insert_lidar(lidar_data)
    except KeyError as e:
        logging.error(f"Missing key in data: {e}")

def insert_telemetry(telemetry_data: TelemetryCreate):
    try:
        db.telemetry.create(data=telemetry_data.dict())
    except Exception as e:
        logging.error(f"Failed to insert telemetry: {e}")

def insert_battery(battery_data: BatteryCreate):
    try:
        db.battery.create(data=battery_data.dict())
    except Exception as e:
        logging.error(f"Failed to insert battery data: {e}")

def insert_camera(camera_data: CameraCreate):
    try:
        db.camera.create(data=camera_data.dict())
    except Exception as e:
        logging.error(f"Failed to insert camera data: {e}")

def insert_lidar(lidar_data: LidarCreate):
    try:
        db.lidar.create(data=lidar_data.dict())
    except Exception as e:
        logging.error(f"Failed to insert lidar data: {e}")

def start_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)
    client.loop_start()
