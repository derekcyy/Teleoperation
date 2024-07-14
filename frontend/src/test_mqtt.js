const mqtt = require('mqtt');

const client = mqtt.connect('mqtt://192.168.18.22:1883');

client.on('connect', () => {
  console.log('Connected to MQTT broker');
  client.publish('turtlebot3/move', JSON.stringify({ linear: { x: -0.2 }, angular: { z: 0.0 } }), (err) => {
    if (err) {
      console.error('Failed to publish message:', err);
    } else {
      console.log('Message published successfully');
    }
    client.end(); // Close the connection after publishing
  });
});

client.on('error', (err) => {
  console.error('Connection error:', err);
});
