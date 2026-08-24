import React from 'react';
import { IconTerminal } from './Icons';

const Header = ({ isConnected, isListening, isProcessing, portfolio, pingMs }) => {
  const totalVal = portfolio?.total_portfolio_value || 100000.00;
  const returnDollar = portfolio?.total_return_dollar || 0.00;
  const returnPct = portfolio?.total_return_pct || 0.00;
  const isPositive = returnDollar >= 0;

  return (
    <header className="app-header">
      <div className="brand-section">
        <div className="brand-logo">
          <IconTerminal size={18} />
          <span>J.A.R.V.I.S.</span>
        </div>
        <span className="brand-pill">QUANT & OS AGENT</span>
      </div>

      <div className="status-badges">
        {/* Quick Portfolio Balance */}
        <div className="quick-equity">
          <span>PORTFOLIO:</span>
          <strong>${totalVal.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</strong>
          <span style={{ color: isPositive ? 'var(--accent-emerald)' : 'var(--accent-rose)' }}>
            ({isPositive ? '+' : ''}{returnDollar.toFixed(2)} / {returnPct.toFixed(2)}%)
          </span>
        </div>

        {/* Neural Hub Status */}
        <div className="status-badge">
          <span className={`status-dot ${!isConnected ? 'disconnected' : isProcessing ? 'processing' : isListening ? 'pulsing' : ''}`}></span>
          <span>{isProcessing ? 'PROCESSING' : isListening ? 'LISTENING' : isConnected ? 'ONLINE' : 'OFFLINE'}</span>
        </div>

        {/* Latency badge */}
        <div className="status-badge">
          <span>WS: {pingMs}ms</span>
        </div>
      </div>
    </header>
  );
};

export default Header;
