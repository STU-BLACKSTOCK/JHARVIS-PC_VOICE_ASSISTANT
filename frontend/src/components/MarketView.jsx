import React, { useState, useEffect } from 'react';
import { IconChart, IconRefresh } from './Icons';

const MarketView = ({ onPlaceOrder, portfolio }) => {
  const [watchlist, setWatchlist] = useState([]);
  const [selectedSymbol, setSelectedSymbol] = useState("AAPL");
  const [candlesData, setCandlesData] = useState(null);
  const [loadingChart, setLoadingChart] = useState(false);
  
  // Indicators display state
  const [showEMA, setShowEMA] = useState(true);
  const [showRSI, setShowRSI] = useState(true);
  const [showMACD, setShowMACD] = useState(false);

  // Order Console State
  const [orderSide, setOrderSide] = useState("BUY");
  const [orderType, setOrderType] = useState("MARKET");
  const [sharesInput, setSharesInput] = useState(10);
  const [orderStatusMsg, setOrderStatusMsg] = useState(null);

  const fetchWatchlist = async () => {
    try {
      const res = await fetch("http://localhost:8000/api/trading/watchlist");
      const data = await res.json();
      setWatchlist(data);
    } catch (e) {
      console.log("Error fetching watchlist:", e);
    }
  };

  const fetchCandles = async (symbol) => {
    setLoadingChart(true);
    try {
      const res = await fetch(`http://localhost:8000/api/trading/candles/${symbol}?range_str=3mo&interval=1d`);
      const data = await res.json();
      setCandlesData(data);
    } catch (e) {
      console.log("Error fetching candles:", e);
    } finally {
      setLoadingChart(false);
    }
  };

  useEffect(() => {
    fetchWatchlist();
    const intv = setInterval(fetchWatchlist, 10000);
    return () => clearInterval(intv);
  }, []);

  useEffect(() => {
    if (selectedSymbol) {
      fetchCandles(selectedSymbol);
    }
  }, [selectedSymbol]);

  const handleOrderSubmit = async (e) => {
    e.preventDefault();
    if (!sharesInput || sharesInput <= 0) return;
    
    setOrderStatusMsg("Placing order...");
    const res = await onPlaceOrder({
      symbol: selectedSymbol,
      shares: parseFloat(sharesInput),
      side: orderSide,
      order_type: orderType
    });

    if (res?.message) {
      setOrderStatusMsg(res.message);
      setTimeout(() => setOrderStatusMsg(null), 5000);
    }
  };

  const currentPrice = watchlist.find(w => w.symbol === selectedSymbol)?.price || (candlesData?.candles?.slice(-1)[0]?.close || 150.0);
  const totalCost = (sharesInput * currentPrice).toFixed(2);
  const userPosition = portfolio?.positions?.find(p => p.symbol === selectedSymbol);

  const candles = candlesData?.candles || [];
  const indicators = candlesData?.indicators || {};

  return (
    <div className="market-view">
      {/* Column 1: Watchlist */}
      <div className="panel-card">
        <div className="panel-header">
          <span className="panel-title">
            <IconChart size={14} />
            Watchlist
          </span>
          <button className="pill-btn" onClick={fetchWatchlist} title="Refresh quotes">
            <IconRefresh size={11} />
          </button>
        </div>
        <div className="watchlist-scroll">
          {watchlist.map(item => {
            const isPos = item.change_pct >= 0;
            const isSel = item.symbol === selectedSymbol;
            return (
              <div
                key={item.symbol}
                className={`watchlist-item ${isSel ? 'selected' : ''}`}
                onClick={() => setSelectedSymbol(item.symbol)}
              >
                <div>
                  <div className="ticker-name">{item.symbol}</div>
                  <div className="ticker-meta">{item.is_crypto ? 'Crypto' : 'US Equity'}</div>
                </div>
                <div className="ticker-price">
                  <div>${item.price.toFixed(2)}</div>
                  <div className={isPos ? 'change-positive' : 'change-negative'}>
                    {isPos ? '+' : ''}{item.change_pct}%
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Column 2: Candlestick & Technical Indicator Charts */}
      <div className="panel-card chart-area-panel">
        <div className="chart-hud-bar">
          <div className="chart-symbol-info">
            <h2>{selectedSymbol}</h2>
            <div className="chart-price">${currentPrice.toFixed(2)}</div>
            {indicators?.summary && (
              <span className="brand-pill" style={{ textTransform: 'uppercase' }}>
                {indicators.summary.trend}
              </span>
            )}
          </div>
          <div className="chart-controls">
            <button className={`pill-btn ${showEMA ? 'active' : ''}`} onClick={() => setShowEMA(!showEMA)}>EMA 20/50</button>
            <button className={`pill-btn ${showRSI ? 'active' : ''}`} onClick={() => setShowRSI(!showRSI)}>RSI (14)</button>
            <button className={`pill-btn ${showMACD ? 'active' : ''}`} onClick={() => setShowMACD(!showMACD)}>MACD</button>
          </div>
        </div>

        <div className="chart-canvas-container">
          {loadingChart ? (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
              Loading quantitative chart data...
            </div>
          ) : candles.length === 0 ? (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-muted)' }}>
              No chart data available for {selectedSymbol}
            </div>
          ) : (
            <CandleChartSVG
              candles={candles}
              indicators={indicators}
              showEMA={showEMA}
              showRSI={showRSI}
              showMACD={showMACD}
            />
          )}
        </div>
      </div>

      {/* Column 3: Order Execution Console */}
      <div className="panel-card">
        <div className="panel-header">
          <span className="panel-title">Trade Console</span>
          <span style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--text-dim)' }}>
            SANDBOX $100K
          </span>
        </div>

        <form className="order-form" onSubmit={handleOrderSubmit}>
          <div className="form-group">
            <label>Order Side</label>
            <div className="side-toggle">
              <button
                type="button"
                className={`side-btn buy ${orderSide === 'BUY' ? 'active' : ''}`}
                onClick={() => setOrderSide('BUY')}
              >
                BUY
              </button>
              <button
                type="button"
                className={`side-btn sell ${orderSide === 'SELL' ? 'active' : ''}`}
                onClick={() => setOrderSide('SELL')}
              >
                SELL
              </button>
            </div>
          </div>

          <div className="form-group">
            <label>Order Type</label>
            <div className="side-toggle">
              <button
                type="button"
                className={`pill-btn ${orderType === 'MARKET' ? 'active' : ''}`}
                onClick={() => setOrderType('MARKET')}
              >
                Market Order
              </button>
              <button
                type="button"
                className={`pill-btn ${orderType === 'LIMIT' ? 'active' : ''}`}
                onClick={() => setOrderType('LIMIT')}
              >
                Limit Order
              </button>
            </div>
          </div>

          <div className="form-group">
            <label>Quantity (Shares / Units)</label>
            <input
              type="number"
              step="any"
              min="0.1"
              className="form-input"
              value={sharesInput}
              onChange={(e) => setSharesInput(e.target.value)}
            />
          </div>

          <div style={{ background: 'rgba(255,255,255,0.03)', padding: '10px', borderRadius: '8px', border: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: 'var(--text-muted)', marginBottom: '4px' }}>
              <span>Est. Unit Price:</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: '#fff' }}>${currentPrice.toFixed(2)}</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', fontWeight: '600' }}>
              <span>Total Est. Cost:</span>
              <span style={{ fontFamily: 'var(--font-mono)', color: 'var(--accent-cyan)' }}>${totalCost}</span>
            </div>
          </div>

          <button type="submit" className={`order-submit-btn ${orderSide.toLowerCase()}`}>
            Execute {orderSide} {sharesInput} {selectedSymbol}
          </button>

          {orderStatusMsg && (
            <div style={{ fontSize: '12px', padding: '8px', borderRadius: '6px', background: 'rgba(255,255,255,0.06)', color: 'var(--text-main)' }}>
              {orderStatusMsg}
            </div>
          )}

          {/* User's Position in this Asset */}
          <div style={{ marginTop: 'auto', paddingTop: '12px', borderTop: '1px solid var(--border-subtle)' }}>
            <div style={{ fontSize: '11px', textTransform: 'uppercase', color: 'var(--text-dim)', marginBottom: '6px' }}>
              Current Position
            </div>
            {userPosition ? (
              <div style={{ fontSize: '12px', display: 'flex', flexDirection: 'column', gap: '4px', fontFamily: 'var(--font-mono)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Shares Owned:</span>
                  <strong>{userPosition.shares}</strong>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Avg Cost:</span>
                  <span>${userPosition.avg_price.toFixed(2)}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <span style={{ color: 'var(--text-muted)' }}>Unrealized P&L:</span>
                  <span className={userPosition.unrealized_pnl >= 0 ? 'change-positive' : 'change-negative'}>
                    {userPosition.unrealized_pnl >= 0 ? '+' : ''}${userPosition.unrealized_pnl.toFixed(2)} ({userPosition.pnl_pct}%)
                  </span>
                </div>
              </div>
            ) : (
              <div style={{ fontSize: '12px', color: 'var(--text-dim)' }}>No active position in {selectedSymbol}</div>
            )}
          </div>
        </form>
      </div>
    </div>
  );
};

// High-Performance Clean SVG Candlestick & Indicator Chart
const CandleChartSVG = ({ candles, indicators, showEMA, showRSI, showMACD }) => {
  const width = 680;
  const height = 280;
  const padding = { top: 20, right: 55, bottom: 25, left: 10 };

  const recentCandles = candles.slice(-45);
  if (recentCandles.length === 0) return null;

  const minPrice = Math.min(...recentCandles.map(c => c.low)) * 0.995;
  const maxPrice = Math.max(...recentCandles.map(c => c.high)) * 1.005;
  const priceRange = maxPrice - minPrice || 1;

  const candleWidth = Math.max(3, (width - padding.left - padding.right) / recentCandles.length - 3);

  const getY = (price) => {
    return padding.top + (height - padding.top - padding.bottom) * (1 - (price - minPrice) / priceRange);
  };

  const getX = (index) => {
    return padding.left + index * ((width - padding.left - padding.right) / recentCandles.length) + candleWidth / 2;
  };

  // EMA Lines
  const ema20Points = (indicators?.ema20 || []).slice(-recentCandles.length)
    .map((val, idx) => val ? `${getX(idx)},${getY(val)}` : null)
    .filter(Boolean)
    .join(' ');

  const ema50Points = (indicators?.ema50 || []).slice(-recentCandles.length)
    .map((val, idx) => val ? `${getX(idx)},${getY(val)}` : null)
    .filter(Boolean)
    .join(' ');

  // Latest RSI
  const rsiArr = (indicators?.rsi || []).slice(-recentCandles.length);
  const latestRSI = rsiArr.slice(-1)[0] || 50;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', gap: '8px' }}>
      <svg viewBox={`0 0 ${width} ${height}`} style={{ width: '100%', height: '70%', overflow: 'visible' }}>
        {/* Horizontal grid lines */}
        {[0, 0.25, 0.5, 0.75, 1].map((ratio, i) => {
          const price = minPrice + priceRange * ratio;
          const y = getY(price);
          return (
            <g key={i}>
              <line x1={padding.left} y1={y} x2={width - padding.right} y2={y} stroke="rgba(255,255,255,0.06)" strokeDasharray="3 3" />
              <text x={width - padding.right + 5} y={y + 4} fill="var(--text-dim)" fontSize="10" fontFamily="var(--font-mono)">
                ${price.toFixed(1)}
              </text>
            </g>
          );
        })}

        {/* Candlesticks */}
        {recentCandles.map((c, idx) => {
          const x = getX(idx);
          const isGreen = c.close >= c.open;
          const color = isGreen ? '#10B981' : '#F43F5E';
          const topY = getY(Math.max(c.open, c.close));
          const botY = getY(Math.min(c.open, c.close));
          const bodyHeight = Math.max(2, botY - topY);

          return (
            <g key={idx}>
              {/* Wick */}
              <line x1={x} y1={getY(c.high)} x2={x} y2={getY(c.low)} stroke={color} strokeWidth="1.2" />
              {/* Body */}
              <rect
                x={x - candleWidth / 2}
                y={topY}
                width={candleWidth}
                height={bodyHeight}
                fill={color}
                rx="1"
              />
            </g>
          );
        })}

        {/* EMA Lines Overlay */}
        {showEMA && ema20Points && (
          <polyline points={ema20Points} fill="none" stroke="#06B6D4" strokeWidth="1.5" />
        )}
        {showEMA && ema50Points && (
          <polyline points={ema50Points} fill="none" stroke="#F59E0B" strokeWidth="1.5" />
        )}
      </svg>

      {/* Sub-chart: RSI (14) */}
      {showRSI && (
        <div style={{ height: '70px', background: 'rgba(0,0,0,0.2)', borderRadius: '6px', padding: '6px 10px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', border: '1px solid var(--border-subtle)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10px', fontFamily: 'var(--font-mono)' }}>
            <span style={{ color: 'var(--accent-cyan)' }}>RSI (14): <strong>{latestRSI.toFixed(1)}</strong></span>
            <span style={{ color: latestRSI > 70 ? 'var(--accent-rose)' : latestRSI < 30 ? 'var(--accent-emerald)' : 'var(--text-dim)' }}>
              {latestRSI > 70 ? 'Overbought (70+)' : latestRSI < 30 ? 'Oversold (30-)' : 'Normal (30-70)'}
            </span>
          </div>
          <div style={{ height: '32px', position: 'relative', width: '100%' }}>
            <div style={{ position: 'absolute', top: '15%', left: 0, right: 0, borderBottom: '1px dashed rgba(244,63,94,0.3)' }}></div>
            <div style={{ position: 'absolute', top: '85%', left: 0, right: 0, borderBottom: '1px dashed rgba(16,185,129,0.3)' }}></div>
            <div style={{ height: '6px', background: 'rgba(255,255,255,0.08)', borderRadius: '3px', marginTop: '13px', overflow: 'hidden' }}>
              <div style={{ height: '100%', width: `${Math.min(100, Math.max(0, latestRSI))}%`, background: latestRSI > 70 ? 'var(--accent-rose)' : latestRSI < 30 ? 'var(--accent-emerald)' : 'var(--accent-cyan)' }}></div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MarketView;
