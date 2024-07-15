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
├── package.json
└── README.md

```

## System Architecture and Communication Protocols Overview

| **Component** | **System**                  | **Protocol** | **Network Protocol**     | **Description**                                                                                       |
|---------------|-----------------------------|--------------|--------------------------|-------------------------------------------------------------------------------------------------------|
|Turtlebot3     |**TurtleBot3 Topics**        | ROS          | UDP, TCP                 |Executes movement command, Publishes sensor data, Publish image from RPI Camera                        |
|Turtlebot3     |**ros_mqtt_bridge.py**       | MQTT/ROS     | TCP (MQTT), UDP (ROS)    |Initialize ROS Node, Sets up MQTT Subscription, Facilitate communication between MQTT and ROS          |
|Computer       |**main.py (backend)**        | MQTT/HTTP    | TCP                      |Integrating MQTT communication, Database interaction, provides API endpoints to frontend application   |
|Computer       |**TeleopsKeys.js (frontend)**| MQTT         | TCP                      |Publishes movement command to the MQTT broker                                                          |
|Computer       |**DataDisplay.js (frontend)**| HTTP         | TCP                      |Fetches data from backend and displays on frontend                                                     |
|Computer       |**VideoStream.js (frontend)**| HTTP         | TCP                      |Displays live video stream from TurtleBot3                                                             |


## Components
### ***Backend***
### 1. prisma/schema.prisma
Defines the database schema using Prisma ORM. It contains models that map to database tables.
        
### 2. src/api/routes/
Contains route handlers for different API endpoints.
- battery.py: Manages battery-related API requests.
- camera.py: Handles camera-related API requests.
- lidar.py: Manages lidar-related API requests.
- telemetry.py: Handles telemetry data API requests.
- waypoint.py: Manages waypoint-related API requests.
        
### 3. src/database.py
Contains database connection logic.
        
### 4. src/main.py
FastAPI application that uses Prisma to establish connections with a database and an MQTT broker. 
It manages TurtleBot3's telemetry, battery, camera, and lidar data; it transforms MQTT messages into database entries and provides this data via API endpoints. 
        
### 5. src/models.py
Defines the data models used in the application.

### 6. src/mqtt_handler.py
Handles MQTT message publishing and subscribing.

### 7. src/ros_handler.py
Manages interaction between ROS (Robot Operating System) and the backend.

### 8. .env
Contains environment variables for the backend configuration, such as 
1. database URL
2. MQTT broker and port

### ***Frontend***
### 1. public/index.html
The main HTML file that serves the React app.

### 2. src/components/
Contains React components used in the application.
DataDisplay.js: Component for displaying telemetry, battery, and sensor data.
TeleopsKeys.js: Component for teleoperation controls (buttons to move the robot).
VideoStream.js: Component for displaying the live video stream from the robot's camera.

### 3. src/App.js
The main React component brings together all other components.
        
### 4. src/index.css
Global CSS styles for the frontend.

### 5. src/index.js
The entry point for the React app. It renders the App component into the DOM.
        
### 6. src/mqttClient.js
Manages MQTT client connections and message handling for the frontend.

### ***Turtlebot***
### "ros_mqtt_bridge.py" 
Adapter that bridges the MQTT messages and ROS topics for TurtleBot3

## Setup Turtlebot3
### Find out the IP address and set the network configuration
**Login to Turtlebot using Keyboard and Monitor (micro HDMI cable)**
`Username: ubuntu`
`Password: turtlebot`

**After logging into turtlebot3 ubuntu, use**
```bash
ifconfig
```
`IP Address (RPI): 192.168.xx.xxx *get the IP address from wlan0*`

**Open the file and update the ROS IP setting**
```bash
nano ~/.bashrc
```

**change:**
```
export ROS_MASTER_URI=http://{IP_ADDRESS_OF_REMOTE_PC}:11311
export ROS_HOSTNAME={IP_ADDRESS_OF_RASPBERRY_PI_4}
```

**Once complete**
```bash
source ~/.bashrc
```

### Set up the WIFI network
**Find the Netplan Configuration File:**
The Netplan configuration files are typically located in the `/etc/netplan/` directory.
*List the files in the directory to find the configuration file (it usually ends with `.yaml`)*
        
```bash
ls /etc/netplan/
```
        The file is often named `50-cloud-init.yaml` or `01-netcfg.yaml`.

**Edit the Configuration File:**
Open the Netplan configuration file using a text editor:      
```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```
        
**Update the Wi-Fi Settings:**
Add or update the Wi-Fi configuration in the file. Configuration:
        
```yaml
network:
  version: 2
  renderer: networkd
  wifis:
    wlan0:
      dhcp4: true
      optional: true
      access-points:
        "your_new_network_ssid":
          password: "your_new_network_password"

```
        
    - Replace `"your_new_network_ssid"` and `"your_new_network_password"` with your actual network's SSID and password.
**Save and Exit:**
    - Use `nano`, save the file by pressing `CTRL + X`, then `Y`, and `Enter`.

### Setting up ROS and bringup
*Nodes are all installed within turtlebot3*
        
**SSH into RPI**

```bash
ssh -X ubuntu@192.168.XX.XXX
```
Password: `turtlebot`
        
**Launch each node with terminal (after ssh):**
`$ roscore`
`$ export TURTLEBOT3_MODEL=burger` *only use this if the nodes are installed in the linux* 
`$ roslaunch turtlebot3_bringup turtlebot3_robot.launch`
`$ roslaunch camera_launch cv_camera.launch`
`$ rosrun web_video_server web_video_server`
`$ roslaunch rosbridge_server rosbridge_websocket.launch`
        
**The following shall only run in sequence #only for linux**
`$ roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch` 
`$ roslaunch turtlebot3_slam turtlebot3_slam.launch`
`$ rosrun map_server map_saver -f ~/map`
`$ roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml` 

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
### 3. Run MQTT broker  and postgresql
**Start the MQTT Broker (Mosquitto)**
Open a terminal and start the MQTT broker:

```bash
brew services start mosquitto
```

**Ensure PostgreSQL is Running**
Make sure your PostgreSQL server is running. You can start it with:
```bash
sudo brew services start postgresql
```

**Check PostgreSQL Status**:
Ensure PostgreSQL is running by checking its status:
```bash
brew services list
```

Should see `postgresql@14` listed as `started`.
  
## Run the Application
**Run the backend server**
```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8080
```
**Run the frontend server**
```bash
cd frontend
npm install
npm start
```

## Interacting with the Turtlebot3
### 1. MQTT and ROS Integration on TURTLEBOT3
- Create a Python script ros_mqtt_bridge.py on TurtleBot3 to bridge ROS messages to MQTT and vice versa.

```bash
import rospy
import paho.mqtt.client as mqtt
import json
import requests
from std_msgs.msg import String, Empty
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import BatteryState, Image, LaserScan
import logging
from datetime import datetime  # Import the datetime module

# MQTT topics
mqtt_cmd_vel_topic = 'turtlebot3/move'
mqtt_telemetry_topic = 'turtlebot3/telemetry'
mqtt_battery_topic = 'turtlebot3/battery'
mqtt_camera_topic = 'turtlebot3/camera'
mqtt_lidar_topic = 'turtlebot3/lidar'
mqtt_recovery_topic = 'turtlebot3/recovery'
mqtt_waypoint_topic = 'turtlebot3/waypoint'
mqtt_map_topic = 'turtlebot3/map'

# ROS topics
ros_cmd_vel_topic = '/cmd_vel'
ros_telemetry_topic = '/odom'
ros_battery_topic = '/battery_state'
ros_camera_topic = '/cv_camera_node/image_raw'
ros_lidar_topic = '/scan'
ros_recovery_topic = '/reset'
ros_waypoint_topic = '/move_base_simple/goal'
ros_map_topic = '/map'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_post_request(endpoint, data):
    url = f'http://192.168.10.159:8080/api/turtlebot3/{endpoint}'
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        rospy.loginfo(f'Successfully sent data to {endpoint}')
    except requests.exceptions.RequestException as e:
        rospy.logerr(f'Failed to send data to {endpoint}: {e}')
        logger.error(f'Failed to send data to {endpoint}: {e}')

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
        reset_pub.publish(Empty())

def telemetry_callback(msg):
    telemetry_data = {
        'turtleBotId': 1,
        'timestamp': str(datetime.utcfromtimestamp(msg.header.stamp.to_sec()).isoformat() + "Z"),
        'x': msg.pose.pose.position.x,
        'y': msg.pose.pose.position.y,
        'heading': msg.pose.pose.orientation.z
    }
    logger.info(f"Telemetry data: {telemetry_data}")
    send_post_request('telemetry', telemetry_data)

def battery_callback(msg):
    battery_data = {
        'turtleBotId': 1,
        'timestamp': str(datetime.utcfromtimestamp(rospy.Time.now().to_sec()).isoformat() + "Z"),
        'voltage': msg.voltage,
        'current': msg.current,
        'percentage': msg.percentage
    }
    logger.info(f"Battery data: {battery_data}")
    send_post_request('battery', battery_data)

def camera_callback(msg):
    camera_data = {
        'turtleBotId': 1,
        'timestamp': str(datetime.utcfromtimestamp(rospy.Time.now().to_sec()).isoformat() + "Z"),
        'image': list(msg.data)  # Adjust encoding if necessary
    }
    logger.info(f"Camera data: {camera_data}")
    send_post_request('camera', camera_data)

def lidar_callback(msg):
    lidar_data = {
        'turtleBotId': 1,
        'timestamp': str(datetime.utcfromtimestamp(rospy.Time.now().to_sec()).isoformat() + "Z"),
        'ranges': list(msg.ranges)
    }
    logger.info(f"Lidar data: {lidar_data}")
    send_post_request('lidar', lidar_data)

def ros_to_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect('192.168.10.159', 1883, 60)

    rospy.init_node('ros_mqtt_bridge', anonymous=True)

    global cmd_vel_pub, waypoint_pub, reset_pub
    cmd_vel_pub = rospy.Publisher(ros_cmd_vel_topic, Twist, queue_size=10)
    waypoint_pub = rospy.Publisher(ros_waypoint_topic, PoseStamped, queue_size=10)
    reset_pub = rospy.Publisher(ros_recovery_topic, Empty, queue_size=10)

    rospy.Subscriber(ros_telemetry_topic, Odometry, telemetry_callback)
    rospy.Subscriber(ros_battery_topic, BatteryState, battery_callback)
    rospy.Subscriber(ros_camera_topic, Image, camera_callback)
    rospy.Subscriber(ros_lidar_topic, LaserScan, lidar_callback)

    client.subscribe(mqtt_cmd_vel_topic)
    client.subscribe(mqtt_waypoint_topic)
    client.subscribe(mqtt_recovery_topic)

    client.loop_start()
    rospy.spin()

if __name__ == '__main__':
    try:
        ros_to_mqtt()
    except rospy.ROSInterruptException:
        pass

```

### 2. Run the ROS node on TurtleBot3

```bash
python3 ros_mqtt_bridge.py
```

## View Data in HTTP
`192.168.XX.XXX:8080/api/turtlebot3/telemetry`
`192.168.XX.XXX:8080/api/turtlebot3/battery`
`192.168.XX.XXX:8080/api/turtlebot3/lidar`

## View Data in pgAdmin
1. Connect to the PostgreSQL database in pgAdmin using the same credentials specified in your .env file.
2. Run SQL queries to view data

```bash
SELECT * FROM public."Telemetry";
SELECT * FROM public."Battery";
SELECT * FROM public."Camera";
SELECT * FROM public."Lidar";

```

## Future improvements that can be made
*Show Video on Frontend:*
Current Method: Using images for video streaming.
Improved Method: Using WebRTC for smoother video streaming.

*Separate API Endpoints into Service Folders:*
Current Method: API endpoints might be scattered or not organized.
Improved Method: Organize API endpoints into service folders in the frontend for better maintainability and readability.

*Show Charts for Data:*
Current Method: Displaying only the most current data.
Improved Method: Use charts to display data from the database for better data visualization.

*Map Data and Robot Position:*
Current Method: Might not be displaying map data.
Improved Method: Show the map and the robot's position on it.

*Connection Method:*
Current Method: Using MQTT for backend communication.
Improved: Use WebSockets for backend communication.

*Improve Visual Styling of Components:*
Current Method: Basic styling.
Improved Method: Enhance the UI with better CSS or use styling libraries like Material-UI or Bootstrap.

*DataDisplay.js*
Current Method: Directly from turtlebot3
Improved Method: Fetched from the API server

*TeleopsKeys.js* 
Current Method: React UI publishing the ROS message to the robot directly
Improved Method: Move data is sent to the API server via WebSockets. The API then publishes an MQTT message, which the adapter subscribes to and translates into a ROS message


