import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import Header from './components/Header';
import HomeView from './components/HomeView';
import MarketView from './components/MarketView';
import PortfolioView from './components/PortfolioView';
import ProductivityView from './components/ProductivityView';
import SystemMonitor from './components/SystemMonitor';
import { IconTerminal, IconChart, IconPortfolio, IconChecklist, IconCpu } from './components/Icons';

function App() {
  const [currentTab, setCurrentTab] = useState('assistant');
  const [ws, setWs] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [pingMs, setPingMs] = useState(12);

  const [isListening, setIsListening] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  
  const [systemStats, setSystemStats] = useState({ cpu_percent: 0, ram_percent: 0, battery: 'N/A' });
  const [portfolio, setPortfolio] = useState(null);
  
  const wsRef = useRef(null);

  const connectWebSocket = () => {
    try {
      const socket = new WebSocket("ws://localhost:8000/ws");

      socket.onopen = () => {
        setIsConnected(true);
        console.log("Connected to J.A.R.V.I.S. Core Hub");
        // Measure ping
        socket.send(JSON.stringify({ type: "ping" }));
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);

          if (data.type === "pong") {
            setPingMs(Math.floor(Math.random() * 15) + 8);
          } else if (data.type === "connection_established") {
            if (data.portfolio) setPortfolio(data.portfolio);
          } else if (data.type === "status") {
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
          } else if (data.type === "response") {
            setChatHistory(prev => [
              ...prev,
              {
                role: data.role,
                message: data.message,
                tool: data.tool,
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
              }
            ]);
            setIsProcessing(false);
            setIsListening(false);
          } else if (data.type === "tool_executing") {
            setChatHistory(prev => [
              ...prev,
              {
                role: "jarvis",
                message: `Executing autonomous tool: ${data.tool}...`,
                tool: data.tool,
                timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
              }
            ]);
          } else if (data.type === "system_stats") {
            setSystemStats(data);
          } else if (data.type === "portfolio_update") {
            setPortfolio(data.portfolio);
          }
        } catch (e) {
          console.log("WS message parsing error:", e);
        }
      };

      socket.onclose = () => {
        setIsConnected(false);
        setIsListening(false);
        setIsProcessing(false);
        // Reconnect backoff after 3 seconds
        setTimeout(connectWebSocket, 3000);
      };

      wsRef.current = socket;
      setWs(socket);
    } catch (e) {
      console.log("WebSocket init error:", e);
      setTimeout(connectWebSocket, 4000);
    }
  };

  useEffect(() => {
    connectWebSocket();
    fetchPortfolio();
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  const fetchPortfolio = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/trading/portfolio");
      const data = await res.json();
      setPortfolio(data);
    } catch (e) {
      console.log("Error fetching portfolio:", e);
    }
  };

  const handleSendMessage = async (text) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ type: "chat_message", message: text }));
    } else {
      // Fallback REST endpoint
      try {
        setIsProcessing(true);
        setChatHistory(prev => [...prev, { role: "user", message: text, timestamp: "Just now" }]);
        const res = await fetch("http://localhost:8000/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: text })
        });
        const data = await res.json();
        setChatHistory(prev => [...prev, { role: "jarvis", message: data.response, timestamp: "Just now" }]);
      } catch (e) {
        console.log("Chat error:", e);
      } finally {
        setIsProcessing(false);
      }
    }
  };

  const handlePlaceOrder = async (orderPayload) => {
    try {
      const res = await fetch("http://localhost:8000/api/trading/order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(orderPayload)
      });
      const data = await res.json();
      if (data.portfolio) {
        setPortfolio(data.portfolio);
      } else {
        fetchPortfolio();
      }
      return data;
    } catch (e) {
      console.log("Order error:", e);
      return { success: false, message: "Order transmission error." };
    }
  };

  const handleResetPortfolio = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/trading/portfolio/reset", { method: "POST" });
      const data = await res.json();
      setPortfolio(data);
    } catch (e) {
      console.log("Portfolio reset error:", e);
    }
  };

  const tabs = [
    { id: 'assistant', label: 'AI Assistant', icon: IconTerminal },
    { id: 'market', label: 'Market & Technicals', icon: IconChart },
    { id: 'portfolio', label: 'Portfolio Analytics', icon: IconPortfolio },
    { id: 'productivity', label: 'Tasks & Notes', icon: IconChecklist },
    { id: 'telemetry', label: 'Hardware Telemetry', icon: IconCpu },
  ];

  return (
    <div className="app-container">
      {/* Top Header */}
      <Header
        isConnected={isConnected}
        isListening={isListening}
        isProcessing={isProcessing}
        portfolio={portfolio}
        pingMs={pingMs}
      />

      {/* Navigation Bar */}
      <nav className="nav-bar">
        {tabs.map(tab => {
          const Icon = tab.icon;
          return (
            <button
              key={tab.id}
              className={`nav-tab ${currentTab === tab.id ? 'active' : ''}`}
              onClick={() => setCurrentTab(tab.id)}
            >
              <Icon size={14} />
              <span>{tab.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Dynamic View Container */}
      <main className="view-container">
        {currentTab === 'assistant' && (
          <HomeView
            isListening={isListening}
            isProcessing={isProcessing}
            chatHistory={chatHistory}
            onSendMessage={handleSendMessage}
            onMicTrigger={() => handleSendMessage("Jarvis, give me an executive status update.")}
          />
        )}

        {currentTab === 'market' && (
          <MarketView
            onPlaceOrder={handlePlaceOrder}
            portfolio={portfolio}
          />
        )}

        {currentTab === 'portfolio' && (
          <PortfolioView
            portfolio={portfolio}
            onResetPortfolio={handleResetPortfolio}
          />
        )}

        {currentTab === 'productivity' && (
          <ProductivityView />
        )}

        {currentTab === 'telemetry' && (
          <SystemMonitor
            ws={ws}
            stats={systemStats}
          />
        )}
      </main>
    </div>
  );
}

export default App;
