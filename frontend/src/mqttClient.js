import { Client as PahoClient, Message as PahoMessage } from 'paho-mqtt';

const client = new PahoClient('ws://broker.hivemq.com:8000/mqtt', 'clientId');

client.connect({
    onSuccess: () => {
        console.log('Connected to MQTT broker');
        client.subscribe('turtlebot3/#');
    },
    onFailure: (err) => {
        console.error('Failed to connect to MQTT broker:', err);
    },
});

client.onMessageArrived = (message) => {
    console.log('Message received:', message.payloadString);
};

const sendMessage = (topic, payload) => {
    const message = new PahoMessage(payload);
    message.destinationName = topic;
    client.send(message);
};

export { client, sendMessage };
