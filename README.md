# TurtleBot3 FastAPI Backend

## Overview
The Teleoperation Capstone Project aims to create a versatile and user-friendly Teleoperation Command Centre (TCC) that enhances unmanned systems' remote control and monitoring capabilities. This project utilizes a TurtleBot3 robot as the primary unmanned system to demonstrate the functionalities and improvements in teleoperation.

## Project structure

```bash
Capstone/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── mqtt_handler.py
│   ├── ros_handler.py
│   ├── database.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── telemetry.py
│   │   │   ├── battery.py
│   │   │   ├── camera.py
│   │   │   ├── lidar.py
│   │   │   ├── waypoint.py
├── prisma/
│   ├── schema.prisma
├── node_modules/
├── .env
├── package.json
├── requirements.txt
└── README.md
'''

## Setup

### 1. Install Node.js Dependencies

```bash
npm install
npx prisma migrate dev --name init
npx prisma generate
