import React, { useEffect, useState } from 'react';

const VideoStream = () => {
  const [streamUrl, setStreamUrl] = useState('http://192.168.18.142:8080/stream?topic=/cv_camera_node/image_raw');
  const [imageSrc, setImageSrc] = useState(null);

  useEffect(() => {
    const interval = setInterval(() => {
      // Create a new timestamp to force the image to update
      const timestamp = new Date().getTime();
      setImageSrc(`${streamUrl}&timestamp=${timestamp}`);
    }, 1000); // Update the image every second

    return () => clearInterval(interval); // Cleanup interval on component unmount
  }, [streamUrl]);

  return (
    <div>
      <h2>Live Video Stream</h2>
      {imageSrc ? (
        <img src={imageSrc} alt="Live Video Stream" style={{ width: '100%' }} />
      ) : (
        <div>Loading video stream...</div>
      )}
    </div>
  );
};

export default VideoStream;
