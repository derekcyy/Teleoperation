import React, { useEffect } from 'react';
import { connectClient, sendMessage } from '../mqttClient';

const TeleopsKeys = () => {
  useEffect(() => {
    connectClient()
      .then(() => {
        console.log('Client connected in TeleopsKeys');
      })
      .catch((err) => {
        console.error('Failed to connect in TeleopsKeys:', err);
      });
  }, []);

  return (
    <div>
      <h2>Teleoperation Commands</h2>
      <button onClick={() => sendMessage('turtlebot3/move', JSON.stringify({ linear: { x: 0.2 }, angular: { z: 0.0 } }))}>Forward</button>
      <button onClick={() => sendMessage('turtlebot3/move', JSON.stringify({ linear: { x: 0.0 }, angular: { z: 0.2 } }))}>Left</button>
      <button onClick={() => sendMessage('turtlebot3/move', JSON.stringify({ linear: { x: 0.0 }, angular: { z: -0.2 } }))}>Right</button>
      <button onClick={() => sendMessage('turtlebot3/move', JSON.stringify({ linear: { x: -0.2 }, angular: { z: 0.0 } }))}>Backward</button>
    </div>
  );
};

export default TeleopsKeys;
