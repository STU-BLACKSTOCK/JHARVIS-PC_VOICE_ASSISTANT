import React, { useEffect } from 'react';

const SystemMonitor = ({ ws, stats }) => {
  // Request stats from WS periodically
  useEffect(() => {
    const interval = setInterval(() => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "get_system_stats" }));
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [ws]);

  // For demonstration, let's just show placeholders if no real data
  return (
    <div className="system-monitor-view fade-in">
      <h2>System Monitor</h2>
      <div className="stats-grid">
        <div className="stat-card glass-panel">
          <h3>CPU Usage</h3>
          <div className="stat-value">{stats.cpu_percent}%</div>
          <div className="progress-bar"><div className="progress" style={{width: `${stats.cpu_percent}%`}}></div></div>
        </div>
        <div className="stat-card glass-panel">
          <h3>RAM Usage</h3>
          <div className="stat-value">{stats.ram_percent}%</div>
          <div className="progress-bar"><div className="progress" style={{width: `${stats.ram_percent}%`}}></div></div>
        </div>
        <div className="stat-card glass-panel">
          <h3>Battery</h3>
          <div className="stat-value">{stats.battery}</div>
        </div>
      </div>
    </div>
  );
};

export default SystemMonitor;
