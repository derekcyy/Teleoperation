import React from 'react';
import { Button, Card, CardContent, Grid, Typography } from '@mui/material';
import mqtt from 'mqtt';

const client = mqtt.connect('ws://broker.hivemq.com:8000/mqtt');

const TeleopsKeys = () => {
  const sendCommand = (command) => {
    client.publish('turtlebot3/command', JSON.stringify({ command }), (err) => {
      if (err) {
        console.error('Error sending command:', err);
      }
    });
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="h2">
          Teleoperation Commands
        </Typography>
        <Grid container spacing={2} justifyContent="center" alignItems="center">
          <Grid item>
            <Button variant="contained" color="primary" onClick={() => sendCommand('forward')}>
              Forward
            </Button>
          </Grid>
          <Grid item>
            <Button variant="contained" color="primary" onClick={() => sendCommand('left')}>
              Left
            </Button>
          </Grid>
          <Grid item>
            <Button variant="contained" color="primary" onClick={() => sendCommand('right')}>
              Right
            </Button>
          </Grid>
          <Grid item>
            <Button variant="contained" color="primary" onClick={() => sendCommand('backward')}>
              Backward
            </Button>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default TeleopsKeys;
