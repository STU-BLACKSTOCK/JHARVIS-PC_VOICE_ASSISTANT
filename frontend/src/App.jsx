import { useState, useEffect, useRef } from 'react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([]);
  const [status, setStatus] = useState("Offline");
  const ws = useRef(null);

  useEffect(() => {
    // Connect to WebSocket backend
    ws.current = new WebSocket("ws://localhost:8000/ws");
    
    ws.current.onopen = () => setStatus("Listening...");
    ws.current.onclose = () => setStatus("Offline");
    ws.current.onerror = () => setStatus("Error connecting to Jarvis");
    
    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'response') {
        setMessages(prev => [...prev, { role: 'jarvis', content: data.message }]);
        setStatus("Listening...");
      } else if (data.type === 'status') {
        setStatus(data.message);
      }
    };

    return () => {
      ws.current.close();
    };
  }, []);

  return (
    <div className="jarvis-container">
      <div className="glass-panel main-panel">
        <header className="header">
          <div className="avatar-container">
            <div className={`avatar-ring ${status.includes('Processing') ? 'pulse' : ''}`}></div>
            <img src="https://ui-avatars.com/api/?name=J&background=0D8ABC&color=fff&rounded=true" alt="Jarvis" className="avatar" />
          </div>
          <h1>J.A.R.V.I.S.</h1>
          <div className={`status-badge ${status === 'Offline' ? 'offline' : 'online'}`}>
            <span className="dot"></span> {status}
          </div>
        </header>

        <div className="chat-container">
          {messages.length === 0 ? (
            <div className="empty-state">System Online. Awaiting voice command...</div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`message ${msg.role}`}>
                <div className="message-content">{msg.content}</div>
              </div>
            ))
          )}
        </div>

        <div className="voice-waveform">
          <div className="bar"></div>
          <div className="bar"></div>
          <div className="bar"></div>
          <div className="bar"></div>
          <div className="bar"></div>
        </div>
      </div>
    </div>
  )
}

export default App
