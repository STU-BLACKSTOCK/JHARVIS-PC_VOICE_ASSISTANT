import React, { useState, useEffect } from 'react';
import './App.css';
import Sidebar from './components/Sidebar';
import HomeView from './components/HomeView';
import SystemMonitor from './components/SystemMonitor';
import ActivityFeed from './components/ActivityFeed';

function App() {
  const [ws, setWs] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [activities, setActivities] = useState([]);
  const [systemStats, setSystemStats] = useState({ cpu_percent: 0, ram_percent: 0, battery: 'N/A' });
  
  const [currentTab, setCurrentTab] = useState('home');
  const [isNavOpen, setIsNavOpen] = useState(false);
  const [isFeedOpen, setIsFeedOpen] = useState(false);

  useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8000/ws");
    
    websocket.onopen = () => console.log("Connected to Jarvis Backend");
    
    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === "status") {
        if (data.message === "Listening...") {
          setIsListening(true);
          setIsProcessing(false);
        } else if (data.message === "Processing...") {
          setIsListening(false);
          setIsProcessing(true);
        } else {
          setIsListening(false);
          setIsProcessing(false);
        }
      } 
      else if (data.type === "response") {
        setChatHistory(prev => [...prev, { role: data.role, message: data.message }]);
        setIsProcessing(false);
        setIsListening(false);
      }
      else if (data.type === "automation_step") {
        setActivities(prev => [{ message: data.message, timestamp: Date.now() }, ...prev].slice(0, 10));
        setIsFeedOpen(true); // Auto-open feed when automation happens
      }
      else if (data.type === "system_stats") {
        setSystemStats(data);
      }
    };

    websocket.onclose = () => console.log("Disconnected from Backend");
    
    setWs(websocket);
    
    return () => websocket.close();
  }, []);

  return (
    <div className="app-container theme-dark">
      {/* Icon Dock on the left side */}
      <div className="dock glass-panel">
        <button className={`dock-btn ${isNavOpen ? 'active' : ''}`} onClick={() => { setIsNavOpen(!isNavOpen); setIsFeedOpen(false); }} title="Navigation">
          ☰
        </button>
        <button className={`dock-btn ${isFeedOpen ? 'active' : ''}`} onClick={() => { setIsFeedOpen(!isFeedOpen); setIsNavOpen(false); }} title="Activity Feed">
          ⚡
        </button>
      </div>

      {/* Collapsible Panels on the left */}
      <div className={`side-panel-container ${isNavOpen || isFeedOpen ? 'open' : ''}`}>
        {isNavOpen && <Sidebar currentTab={currentTab} setCurrentTab={setCurrentTab} />}
        {isFeedOpen && <ActivityFeed activities={activities} />}
      </div>
      
      <main className="main-content">
        {currentTab === 'home' && (
          <HomeView isListening={isListening} isProcessing={isProcessing} chatHistory={chatHistory} />
        )}
        {currentTab === 'system' && <SystemMonitor ws={ws} stats={systemStats} />}
        {currentTab === 'productivity' && (
          <div className="placeholder-view glass-panel"><h2>Productivity & Notes (Coming Soon)</h2></div>
        )}
        {currentTab === 'workflows' && (
          <div className="placeholder-view glass-panel"><h2>Saved Workflows (Coming Soon)</h2></div>
        )}
      </main>
    </div>
  );
}

export default App;
