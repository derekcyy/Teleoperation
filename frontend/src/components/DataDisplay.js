import React, { useEffect, useState } from 'react';
import axios from 'axios';

const DataDisplay = () => {
  const [telemetryData, setTelemetryData] = useState([]);
  const [batteryData, setBatteryData] = useState([]);
  const [cameraData, setCameraData] = useState([]);
  const [lidarData, setLidarData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const telemetryUrl = 'http://192.168.18.22:8080/api/turtlebot3/telemetry';
        console.log(`Fetching telemetry data from: ${telemetryUrl}`);
        const telemetryResponse = await axios.get(telemetryUrl);
        console.log('Telemetry Data:', telemetryResponse.data);
        setTelemetryData(telemetryResponse.data.data ? [telemetryResponse.data.data] : []);

        const batteryUrl = 'http://192.168.18.22:8080/api/turtlebot3/battery';
        console.log(`Fetching battery data from: ${batteryUrl}`);
        const batteryResponse = await axios.get(batteryUrl);
        console.log('Battery Data:', batteryResponse.data);
        setBatteryData(batteryResponse.data.data ? [batteryResponse.data.data] : []);

        const cameraUrl = 'http://192.168.18.22:8080/api/turtlebot3/camera';
        console.log(`Fetching camera data from: ${cameraUrl}`);
        const cameraResponse = await axios.get(cameraUrl);
        console.log('Camera Data:', cameraResponse.data);
        setCameraData(cameraResponse.data.data ? [cameraResponse.data.data] : []);

        const lidarUrl = 'http://192.168.18.22:8080/api/turtlebot3/lidar';
        console.log(`Fetching lidar data from: ${lidarUrl}`);
        const lidarResponse = await axios.get(lidarUrl);
        console.log('Lidar Data:', lidarResponse.data);
        setLidarData(lidarResponse.data.data ? [lidarResponse.data.data] : []);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Telemetry Data</h2>
      {telemetryData.length > 0 ? (
        <ul>
          {telemetryData.map((item, index) => (
            <li key={index}>
              <strong>ID:</strong> {item.turtleBotId} <br />
              <strong>Timestamp:</strong> {item.timestamp} <br />
              <strong>X:</strong> {item.x} <br />
              <strong>Y:</strong> {item.y} <br />
              <strong>Heading:</strong> {item.heading}
            </li>
          ))}
        </ul>
      ) : (
        <div>No telemetry data available</div>
      )}

      <h2>Battery Data</h2>
      {batteryData.length > 0 ? (
        <ul>
          {batteryData.map((item, index) => (
            <li key={index}>
              <strong>ID:</strong> {item.turtleBotId} <br />
              <strong>Timestamp:</strong> {item.timestamp} <br />
              <strong>Voltage:</strong> {item.voltage} <br />
              <strong>Current:</strong> {item.current} <br />
              <strong>Percentage:</strong> {item.percentage}
            </li>
          ))}
        </ul>
      ) : (
        <div>No battery data available</div>
      )}

      <h2>Camera Data</h2>
      {cameraData.length > 0 ? (
        <ul>
          {cameraData.map((item, index) => (
            <li key={index}>
              <strong>ID:</strong> {item.turtleBotId} <br />
              <strong>Timestamp:</strong> {item.timestamp} <br />
              <strong>Image:</strong> <img src={`data:image/jpeg;base64,${item.image}`} alt="Camera" />
            </li>
          ))}
        </ul>
      ) : (
        <div>No camera data available</div>
      )}

      <h2>Lidar Data</h2>
      {lidarData.length > 0 ? (
        <ul>
          {lidarData.map((item, index) => (
            <li key={index}>
              <strong>ID:</strong> {item.turtleBotId} <br />
              <strong>Timestamp:</strong> {item.timestamp} <br />
              <strong>Ranges:</strong> {item.ranges.join(', ')}
            </li>
          ))}
        </ul>
      ) : (
        <div>No lidar data available</div>
      )}
    </div>
  );
};

export default DataDisplay;
