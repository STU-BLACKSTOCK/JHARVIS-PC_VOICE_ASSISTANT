import React, { useState, useRef, useEffect } from 'react';
import AudioVisualizer from './AudioVisualizer';
import { IconSend, IconMic, IconTerminal } from './Icons';

const HomeView = ({ isListening, isProcessing, chatHistory, onSendMessage, onMicTrigger }) => {
  const [inputText, setInputText] = useState("");
  const chatEndRef = useRef(null);

  const samplePrompts = [
    "What is the RSI and MACD of AAPL?",
    "Buy 10 shares of NVDA at market",
    "Show me my portfolio risk & balance",
    "Add complete financial audit to my tasks",
    "Take a note: Review Q3 earnings call"
  ];

  const handleSend = (e) => {
    e?.preventDefault();
    if (!inputText.trim()) return;
    onSendMessage(inputText.trim());
    setInputText("");
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chatHistory, isProcessing]);

  return (
    <div className="assistant-view">
      {/* Top Telemetry Visualizer HUD */}
      <div className="assistant-top-hud">
        <AudioVisualizer isListening={isListening} isProcessing={isProcessing} />
        <div style={{ fontSize: '11px', fontFamily: 'var(--font-mono)', color: 'var(--text-dim)' }}>
          MODEL: LLaMA 3.3 70B Versatile
        </div>
      </div>

      {/* Main Chat Scroll Feed */}
      <div className="chat-scroll-area">
        {chatHistory.length === 0 ? (
          <div className="chat-empty-state">
            <div className="empty-icon">⚡</div>
            <h3>J.A.R.V.I.S. Core Online</h3>
            <p style={{ maxWidth: '420px', fontSize: '13px', marginTop: '6px', lineHeight: '1.4' }}>
              Speak aloud by saying <strong>"Jarvis"</strong> or choose a quick prompt to analyze technicals, execute paper trades, or automate tasks.
            </p>
            <div className="suggestion-chips">
              {samplePrompts.map((prompt, idx) => (
                <button
                  key={idx}
                  className="suggestion-chip"
                  onClick={() => onSendMessage(prompt)}
                >
                  {prompt}
                </button>
              ))}
            </div>
          </div>
        ) : (
          chatHistory.map((msg, idx) => (
            <div key={idx} className={`message-row ${msg.role}`}>
              <div className="message-meta">
                <span>{msg.role === 'user' ? 'YOU' : 'J.A.R.V.I.S.'}</span>
                <span>•</span>
                <span>{msg.timestamp || 'Just now'}</span>
              </div>
              <div className="message-card">
                {msg.tool && (
                  <div className="tool-chip">
                    <IconTerminal size={12} />
                    <span>Tool executed: {msg.tool}</span>
                  </div>
                )}
                <div style={{ whiteSpace: 'pre-wrap' }}>{msg.message}</div>
              </div>
            </div>
          ))
        )}
        {isProcessing && (
          <div className="message-row jarvis">
            <div className="message-meta">J.A.R.V.I.S. • Thinking</div>
            <div className="message-card" style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className="status-dot processing pulsing"></span>
              <span style={{ fontSize: '13px', color: 'var(--text-muted)' }}>Analyzing telemetry & executing tool pipeline...</span>
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Bottom Command Bar */}
      <form className="chat-input-bar" onSubmit={handleSend}>
        <input
          type="text"
          className="chat-input-field"
          placeholder="Ask Jarvis anything or type a trade / automation command..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        <button
          type="button"
          className="action-btn"
          title="Push to talk"
          onClick={onMicTrigger}
        >
          <IconMic />
        </button>
        <button
          type="submit"
          className="action-btn send-btn"
          title="Send command"
        >
          <IconSend />
        </button>
      </form>
    </div>
  );
};

export default HomeView;
