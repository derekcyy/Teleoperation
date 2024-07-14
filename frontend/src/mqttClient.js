import mqtt from 'mqtt';

let client = null;

const connectClient = () => {
  return new Promise((resolve, reject) => {
    client = mqtt.connect('ws://192.168.18.22:9001'); // Use the WebSocket port

    client.on('connect', () => {
      console.log('Connected to MQTT broker');
      resolve(client);
    });

    client.on('error', (err) => {
      console.error('Failed to connect to MQTT broker:', err);
      reject(err);
    });
  });
};

const sendMessage = (topic, payload) => {
  if (!client || !client.connected) {
    console.error('Client not connected');
    return;
  }
  client.publish(topic, payload);
};

export { connectClient, sendMessage };
