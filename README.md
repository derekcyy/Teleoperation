# Teleoperation Command Centre (TCC) Development

## Overview
The Teleoperation Capstone Project aims to create a versatile and user-friendly Teleoperation Command Centre (TCC) that enhances unmanned systems' remote control and monitoring capabilities. This project utilizes a TurtleBot3 robot as the primary unmanned system to demonstrate the functionalities and improvements in teleoperation.

## Project Requirements
This project aims to develop a Teleoperation System that is intuitive, versatile, and adaptable to various industrial applications. The core objectives include:

1. Designing a user-friendly interface to make the technology accessible to a broader range of users.
2. Integrating video streaming capabilities is essential for real-time monitoring and control in various unmanned systems.
3. Incorporating real-time data processing for enhanced operational decision-making, ensuring a human is in the loop for critical decisions.

By addressing these objectives, the project will significantly contribute to the evolution of teleoperation technologies, making them more efficient, safe, and accessible. This aligns with the sustainable innovation goals, focusing on technological advancement and its positive impact on society and the environment.

## Project structure

```bash
TeleoperationCapstone/
├── backend/
│   ├── prisma/
│   │   ├── schema.prisma
│   ├── src/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── routes/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── battery.py
│   │   │   │   ├── camera.py
│   │   │   │   ├── lidar.py
│   │   │   │   ├── telemetry.py
│   │   │   │   ├── waypoint.py
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── mqtt_handler.py
│   │   ├── ros_handler.py
│   ├── .env
│   ├── README.md
│   ├── requirements.txt
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   ├── DataDisplay.js
│   │   │   ├── TeleopsKeys.js
│   │   │   ├── VideoStream.js
│   │   ├── App.js
│   │   ├── index.css
│   │   ├── index.js
│   │   ├── mqttClient.js
│   │   ├── reportWebVitals.js
│   ├── package.json
│   ├── .gitignore
│   ├── README.md
├── node_modules/
├── turtlebot3/
│   ├── ros_mqtt_bridge.py
├── package.json
└── README.md

```
## System Architecture and Communication Protocols Overview
| Left |  Center  | Right |
|:-----|:--------:|------:|
| L0   | **bold** | $1600 |
| L1   |  `code`  |   $12 |
| L2   | _italic_ |    $1 |
## Components

## Setup Turtlebot3

## Setup the project
### 1. Set Up the Python Environment

```bash
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```
### 2. Set Up the Database
  - Ensure PostgreSQL server is running and that the credentials in  `.env` file are correct.
  
  - Check the status of migrations
  ```bash
  npx prisma migrate status
  ```
  - Run/Re-run Prisma migrations
  ```bash
  npx prisma migrate dev --name init
  npx prisma generate
  ```
  
### 3. Run the Application

```bash
uvicorn src.main:app --reload
```

##Interacting with the Turtlebot3
### 1. MQTT and ROS Integration on TURTLEBOT3
- Create a Python script ros_mqtt_bridge.py on TurtleBot3 to bridge ROS messages to MQTT and vice versa.

```bash
import rospy
import paho.mqtt.client as mqtt
import json
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import BatteryState, Image, LaserScan

mqtt_cmd_vel_topic = 'turtlebot3/move'
mqtt_telemetry_topic = 'turtlebot3/telemetry'
mqtt_battery_topic = 'turtlebot3/battery'
mqtt_camera_topic = 'turtlebot3/camera'
mqtt_lidar_topic = 'turtlebot3/lidar'
mqtt_recovery_topic = 'turtlebot3/recovery'
mqtt_waypoint_topic = 'turtlebot3/waypoint'
mqtt_map_topic = 'turtlebot3/map'

ros_cmd_vel_topic = '/cmd_vel'
ros_telemetry_topic = '/odom'
ros_battery_topic = '/battery_state'
ros_camera_topic = '/cv_camera_node/image_raw'
ros_lidar_topic = '/scan'
ros_recovery_topic = '/reset'
ros_waypoint_topic = '/move_base_simple/goal'
ros_map_topic = '/map'

def on_connect(client, userdata, flags, rc):
    rospy.loginfo("Connected to MQTT broker")
    client.subscribe(mqtt_cmd_vel_topic)
    client.subscribe(mqtt_waypoint_topic)
    client.subscribe(mqtt_recovery_topic)

def on_message(client, userdata, msg):
    if msg.topic == mqtt_cmd_vel_topic:
        data = json.loads(msg.payload)
        twist = Twist()
        twist.linear.x = data['linear']['x']
        twist.angular.z = data['angular']['z']
        cmd_vel_pub.publish(twist)
    elif msg.topic == mqtt_waypoint_topic:
        data = json.loads(msg.payload)
        goal = PoseStamped()
        goal.header.frame_id = "map"
        goal.pose.position.x = data['x']
        goal.pose.position.y = data['y']
        goal.pose.orientation.z = data['theta']
        waypoint_pub.publish(goal)
    elif msg.topic == mqtt_recovery_topic:
        reset_pub.publish(String("reset"))

def ros_to_mqtt():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.10.159", 1883, 60)

    rospy.init_node('ros_mqtt_bridge', anonymous=True)

    global cmd_vel_pub, waypoint_pub, reset_pub
    cmd_vel_pub = rospy.Publisher(ros_cmd_vel_topic, Twist, queue_size=10)
    waypoint_pub = rospy.Publisher(ros_waypoint_topic, PoseStamped, queue_size=10)
    reset_pub = rospy.Publisher(ros_recovery_topic, String, queue_size=10)

    rospy.Subscriber(ros_telemetry_topic, Odometry, lambda msg: client.publish(mqtt_telemetry_topic, json.dumps({
        'turtleBotId': 1,
        'timestamp': rospy.Time.now().to_sec(),
        'x': msg.pose.pose.position.x,
        'y': msg.pose.pose.position.y,
        'heading': msg.pose.pose.orientation.z,
    })))
    rospy.Subscriber(ros_battery_topic, BatteryState, lambda msg: client.publish(mqtt_battery_topic, json.dumps({
        'voltage': msg.voltage,
        'current': msg.current,
        'percentage': msg.percentage
    })))
    rospy.Subscriber(ros_camera_topic, Image, lambda msg: client.publish(mqtt_camera_topic, json.dumps({
        'image': msg.data  # You might want to encode this differently
    })))
    rospy.Subscriber(ros_lidar_topic, LaserScan, lambda msg: client.publish(mqtt_lidar_topic, json.dumps({
        'ranges': msg.ranges
    })))
    rospy.Subscriber(ros_map_topic, OccupancyGrid, lambda msg: client.publish(mqtt_map_topic, json.dumps({
        'data': msg.data,
        'info': {
            'resolution': msg.info.resolution,
            'width': msg.info.width,
            'height': msg.info.height
        }
    })))

    client.loop_start()
    rospy.spin()

if __name__ == '__main__':
    try:
        ros_to_mqtt()
    except rospy.ROSInterruptException:
        pass
```

- Bring Up Turtlebot

```bash
$ roscore
$ ssh -X ubuntu@{IP_ADDRESS_OF_RASPBERRY_PI}
$ export TURTLEBOT3_MODEL=burger
$ roslaunch turtlebot3_bringup turtlebot3_robot.launch
$ roslaunch camera_launch cv_camera.launch
$ roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
$ roslaunch rosbridge_server rosbridge_websocket.launch
$ roslaunch camera_launch gmapping.launch (not necessary)
$ roslaunch turtlebot3_slam turtlebot3_slam.launch
$ rostopic list #Check if the topics are declared
```

### 2. Run the MQTT broker on-board computer 

```bash
brew services start mosquitto
```

### 3. Run the ROS node on TurtleBot3

```bash
python3 ros_mqtt_bridge.py
```

## View Data in pgAdmin
1. Connect to the PostgreSQL database in pgAdmin using the same credentials specified in your .env file.
2. Run SQL queries to view data

```bash
SELECT * FROM public."Telemetry";
SELECT * FROM public."Battery";
SELECT * FROM public."Camera";
SELECT * FROM public."Lidar";

```
