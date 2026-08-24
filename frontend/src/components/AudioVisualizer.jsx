import React, { useEffect, useState } from 'react';

const AudioVisualizer = ({ isListening, isProcessing }) => {
  const [bars, setBars] = useState([6, 12, 18, 10, 16, 22, 14, 8, 18, 12, 6]);

  useEffect(() => {
    let interval;
    if (isListening) {
      interval = setInterval(() => {
        setBars(prev => prev.map(() => Math.floor(Math.random() * 22) + 4));
      }, 100);
    } else if (isProcessing) {
      interval = setInterval(() => {
        setBars(prev => prev.map((_, i) => Math.sin(Date.now() / 150 + i) * 8 + 14));
      }, 80);
    } else {
      setBars([4, 6, 8, 10, 8, 6, 8, 10, 8, 6, 4]);
    }
    return () => clearInterval(interval);
  }, [isListening, isProcessing]);

  return (
    <div className="visualizer-wrapper">
      <div className="waveform-bars">
        {bars.map((h, idx) => (
          <div
            key={idx}
            className="wave-bar"
            style={{
              height: `${h}px`,
              background: isProcessing
                ? 'var(--accent-indigo)'
                : isListening
                ? 'var(--accent-emerald)'
                : 'var(--accent-cyan)'
            }}
          />
        ))}
      </div>
      <span style={{ fontSize: '12px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
        {isListening ? "Listening for speech..." : isProcessing ? "Groq Reasoning..." : "Voice Gateway Ready"}
      </span>
    </div>
  );
};

export default AudioVisualizer;
