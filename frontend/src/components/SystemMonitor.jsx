import React, { useEffect } from 'react';
import { IconCpu } from './Icons';

const SystemMonitor = ({ ws, stats }) => {
  useEffect(() => {
    const interval = setInterval(() => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ type: "get_system_stats" }));
      }
    }, 2000);
    return () => clearInterval(interval);
  }, [ws]);

  const cpu = stats?.cpu_percent || 0;
  const ram = stats?.ram_percent || 0;
  const ramDetail = stats?.ram_detail || 'Calculating...';
  const battery = stats?.battery || 'N/A';

  return (
    <div className="telemetry-view">
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        <IconCpu size={20} className="change-positive" />
        <h2 style={{ fontSize: '18px', fontWeight: '700' }}>Host Hardware Telemetry</h2>
      </div>

      <div className="telemetry-grid">
        {/* CPU Telemetry */}
        <div className="telemetry-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span className="stat-box-label">Processor Load</span>
            <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--accent-cyan)' }}>Active</span>
          </div>
          <div style={{ fontSize: '28px', fontWeight: '700', fontFamily: 'var(--font-mono)' }}>
            {cpu}%
          </div>
          <div className="telemetry-meter">
            <div
              className="telemetry-fill"
              style={{
                width: `${cpu}%`,
                background: cpu > 85 ? 'var(--accent-rose)' : cpu > 60 ? 'var(--accent-amber)' : 'linear-gradient(90deg, #06B6D4, #6366F1)'
              }}
            />
          </div>
          <span style={{ fontSize: '11px', color: 'var(--text-dim)' }}>Multi-core dynamic sampling (interval: 0.5s)</span>
        </div>

        {/* Memory Telemetry */}
        <div className="telemetry-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span className="stat-box-label">Memory Utilization</span>
            <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--accent-indigo)' }}>Virtual RAM</span>
          </div>
          <div style={{ fontSize: '28px', fontWeight: '700', fontFamily: 'var(--font-mono)' }}>
            {ram}%
          </div>
          <div className="telemetry-meter">
            <div
              className="telemetry-fill"
              style={{
                width: `${ram}%`,
                background: ram > 85 ? 'var(--accent-rose)' : 'linear-gradient(90deg, #6366F1, #EC4899)'
              }}
            />
          </div>
          <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--text-dim)' }}>{ramDetail}</span>
        </div>

        {/* Battery Telemetry */}
        <div className="telemetry-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span className="stat-box-label">Power & Battery</span>
            <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--accent-emerald)' }}>Sensor</span>
          </div>
          <div style={{ fontSize: '22px', fontWeight: '700', fontFamily: 'var(--font-mono)', marginTop: '4px' }}>
            {battery}
          </div>
          <span style={{ fontSize: '11px', color: 'var(--text-dim)', marginTop: 'auto' }}>AC adapter & battery health tracker</span>
        </div>
      </div>
    </div>
  );
};

export default SystemMonitor;
