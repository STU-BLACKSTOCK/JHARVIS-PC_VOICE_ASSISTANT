import React, { useState, useEffect } from 'react';
import { IconPortfolio, IconRefresh, IconTrash } from './Icons';

const PortfolioView = ({ portfolio, onResetPortfolio }) => {
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/trading/analytics");
      const data = await res.json();
      setAnalytics(data);
    } catch (e) {
      console.log("Error fetching analytics:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, [portfolio]);

  const summary = analytics?.summary || {};
  const risk = analytics?.risk_metrics || {};
  const allocation = analytics?.asset_allocation || [];
  const equityCurve = analytics?.equity_curve || [];
  const positions = portfolio?.positions || [];
  const orders = portfolio?.orders || [];

  const isPos = (summary.total_return_dollar || 0) >= 0;

  return (
    <div className="portfolio-view">
      {/* Top Header & Actions */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <IconPortfolio size={20} className="change-positive" />
          <h2 style={{ fontSize: '18px', fontWeight: '700' }}>Portfolio Analytics & Risk Engine</h2>
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button className="pill-btn" onClick={fetchAnalytics} title="Recalculate metrics">
            <IconRefresh size={12} /> Recalculate
          </button>
          <button
            className="pill-btn"
            style={{ color: 'var(--accent-rose)', borderColor: 'rgba(244,63,94,0.3)' }}
            onClick={() => {
              if (window.confirm("Reset sandbox portfolio back to $100,000.00?")) {
                onResetPortfolio();
              }
            }}
          >
            Reset Sandbox
          </button>
        </div>
      </div>

      {/* Stats Hero Grid */}
      <div className="stats-hero-grid">
        <div className="stat-box">
          <span className="stat-box-label">Portfolio Value</span>
          <span className="stat-box-value">${(summary.total_portfolio_value || 100000).toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
          <span className={`stat-box-sub ${isPos ? 'change-positive' : 'change-negative'}`}>
            {isPos ? '+' : ''}${(summary.total_return_dollar || 0).toFixed(2)} ({summary.total_return_pct || 0}%)
          </span>
        </div>

        <div className="stat-box">
          <span className="stat-box-label">Cash Balance</span>
          <span className="stat-box-value">${(summary.cash_balance || 100000).toLocaleString('en-US', { minimumFractionDigits: 2 })}</span>
          <span className="stat-box-sub" style={{ color: 'var(--text-dim)' }}>Unallocated Capital</span>
        </div>

        <div className="stat-box">
          <span className="stat-box-label">Unrealized P&L</span>
          <span className={`stat-box-value ${(summary.unrealized_pnl || 0) >= 0 ? 'change-positive' : 'change-negative'}`}>
            {(summary.unrealized_pnl || 0) >= 0 ? '+' : ''}${(summary.unrealized_pnl || 0).toFixed(2)}
          </span>
          <span className="stat-box-sub" style={{ color: 'var(--text-dim)' }}>Open positions delta</span>
        </div>

        <div className="stat-box">
          <span className="stat-box-label">Sharpe Ratio</span>
          <span className="stat-box-value" style={{ color: 'var(--accent-cyan)' }}>{risk.sharpe_ratio || 1.25}</span>
          <span className="stat-box-sub" style={{ color: 'var(--text-dim)' }}>Risk-Adjusted Return</span>
        </div>

        <div className="stat-box">
          <span className="stat-box-label">Max Drawdown</span>
          <span className="stat-box-value" style={{ color: 'var(--accent-rose)' }}>{risk.max_drawdown || 0.0}%</span>
          <span className="stat-box-sub" style={{ color: 'var(--text-dim)' }}>Peak-to-Trough Risk</span>
        </div>

        <div className="stat-box">
          <span className="stat-box-label">Win Rate</span>
          <span className="stat-box-value" style={{ color: 'var(--accent-emerald)' }}>{risk.win_rate || 0.0}%</span>
          <span className="stat-box-sub" style={{ color: 'var(--text-dim)' }}>Closed Trades ({risk.profit_factor || 1.0} PF)</span>
        </div>
      </div>

      {/* Middle Grid: Equity Curve & Asset Allocation */}
      <div className="portfolio-charts-grid">
        {/* Equity Curve SVG */}
        <div className="panel-card" style={{ padding: '16px' }}>
          <div className="panel-title" style={{ marginBottom: '12px' }}>Equity Growth Trajectory</div>
          <EquityCurveSVG curve={equityCurve} />
        </div>

        {/* Asset Allocation Breakdown */}
        <div className="panel-card" style={{ padding: '16px' }}>
          <div className="panel-title" style={{ marginBottom: '12px' }}>Asset Allocation</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {allocation.map((item, idx) => (
              <div key={idx}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '4px' }}>
                  <span>{item.name}</span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontWeight: '600' }}>{item.percentage}%</span>
                </div>
                <div style={{ height: '6px', background: 'rgba(255,255,255,0.06)', borderRadius: '3px', overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${item.percentage}%`, background: item.color || 'var(--accent-cyan)', borderRadius: '3px' }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom: Open Positions & Order History */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        {/* Active Holdings */}
        <div className="panel-card">
          <div className="panel-header">
            <span className="panel-title">Active Holdings ({positions.length})</span>
          </div>
          <div style={{ overflowX: 'auto', padding: '8px' }}>
            {positions.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '20px', color: 'var(--text-dim)', fontSize: '13px' }}>
                No open positions. Use the Market tab to place your first trade.
              </div>
            ) : (
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px', fontFamily: 'var(--font-mono)' }}>
                <thead>
                  <tr style={{ color: 'var(--text-dim)', textAlign: 'left', borderBottom: '1px solid var(--border-subtle)' }}>
                    <th style={{ padding: '6px' }}>ASSET</th>
                    <th style={{ padding: '6px' }}>SHARES</th>
                    <th style={{ padding: '6px' }}>AVG PRICE</th>
                    <th style={{ padding: '6px' }}>MKT VALUE</th>
                    <th style={{ padding: '6px' }}>P&L</th>
                  </tr>
                </thead>
                <tbody>
                  {positions.map(p => (
                    <tr key={p.symbol} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                      <td style={{ padding: '8px 6px', fontWeight: 'bold' }}>{p.symbol}</td>
                      <td style={{ padding: '8px 6px' }}>{p.shares}</td>
                      <td style={{ padding: '8px 6px' }}>${p.avg_price.toFixed(2)}</td>
                      <td style={{ padding: '8px 6px' }}>${p.market_value.toFixed(2)}</td>
                      <td style={{ padding: '8px 6px' }} className={p.unrealized_pnl >= 0 ? 'change-positive' : 'change-negative'}>
                        {p.unrealized_pnl >= 0 ? '+' : ''}${p.unrealized_pnl.toFixed(2)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>

        {/* Trade Execution History */}
        <div className="panel-card">
          <div className="panel-header">
            <span className="panel-title">Recent Executions</span>
          </div>
          <div style={{ overflowX: 'auto', padding: '8px' }}>
            {orders.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '20px', color: 'var(--text-dim)', fontSize: '13px' }}>
                No recent trades logged.
              </div>
            ) : (
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px', fontFamily: 'var(--font-mono)' }}>
                <thead>
                  <tr style={{ color: 'var(--text-dim)', textAlign: 'left', borderBottom: '1px solid var(--border-subtle)' }}>
                    <th style={{ padding: '6px' }}>SIDE</th>
                    <th style={{ padding: '6px' }}>ASSET</th>
                    <th style={{ padding: '6px' }}>SHARES</th>
                    <th style={{ padding: '6px' }}>PRICE</th>
                    <th style={{ padding: '6px' }}>STATUS</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.slice(0, 8).map(o => (
                    <tr key={o.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.03)' }}>
                      <td style={{ padding: '8px 6px', fontWeight: 'bold', color: o.side === 'BUY' ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
                        {o.side}
                      </td>
                      <td style={{ padding: '8px 6px' }}>{o.symbol}</td>
                      <td style={{ padding: '8px 6px' }}>{o.shares}</td>
                      <td style={{ padding: '8px 6px' }}>${o.price.toFixed(2)}</td>
                      <td style={{ padding: '8px 6px' }}>
                        <span className="brand-pill" style={{ fontSize: '9px' }}>{o.status}</span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

const EquityCurveSVG = ({ curve }) => {
  const width = 500;
  const height = 150;
  const padding = { top: 15, right: 40, bottom: 20, left: 10 };

  if (!curve || curve.length < 2) {
    return <div style={{ height: '150px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-dim)' }}>Collecting trajectory points...</div>;
  }

  const values = curve.map(p => p.value);
  const minVal = Math.min(...values) * 0.995;
  const maxVal = Math.max(...values) * 1.005;
  const range = maxVal - minVal || 1;

  const getY = (val) => padding.top + (height - padding.top - padding.bottom) * (1 - (val - minVal) / range);
  const getX = (idx) => padding.left + (idx / (curve.length - 1)) * (width - padding.left - padding.right);

  const points = curve.map((p, idx) => `${getX(idx)},${getY(p.value)}`).join(' ');
  const areaPoints = `${points} ${getX(curve.length - 1)},${height - padding.bottom} ${getX(0)},${height - padding.bottom}`;

  return (
    <svg viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', height: '150px', overflow: 'visible' }}>
      <defs>
        <linearGradient id="equityGradient" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#10B981" stopOpacity="0.25" />
          <stop offset="100%" stopColor="#10B981" stopOpacity="0.0" />
        </linearGradient>
      </defs>
      <polygon points={areaPoints} fill="url(#equityGradient)" />
      <polyline points={points} fill="none" stroke="#10B981" strokeWidth="2" />
      {/* Label latest point */}
      <text x={width - padding.right + 4} y={getY(values[values.length - 1]) + 4} fill="#10B981" fontSize="10" fontFamily="var(--font-mono)">
        ${(values[values.length - 1] / 1000).toFixed(1)}k
      </text>
    </svg>
  );
};

export default PortfolioView;
