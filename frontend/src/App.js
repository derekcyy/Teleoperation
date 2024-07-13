import React from 'react';
import DataDisplay from './components/DataDisplay';
import TeleopsKeys from './components/TeleopsKeys';
import VideoStream from './components/VideoStream';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>TurtleBot3 Teleoperation Command Center</h1>
      </header>
      <main>
        <VideoStream />
        <DataDisplay />
        <TeleopsKeys />
      </main>
    </div>
  );
}

export default App;
