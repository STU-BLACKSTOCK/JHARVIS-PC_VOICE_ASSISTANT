import React from 'react';

const HomeView = ({ isListening, isProcessing, chatHistory }) => {
  return (
    <div className="home-view">
      <div className="status-indicator">
        <div className={`orb ${isListening ? 'listening' : ''} ${isProcessing ? 'processing' : ''}`}></div>
        <h2>{isListening ? "Listening..." : isProcessing ? "Processing..." : "Jarvis is Online"}</h2>
      </div>
      
      <div className="chat-container glass-panel">
        {chatHistory.length === 0 ? (
          <p className="placeholder-text">Say "Jarvis" to wake me up.</p>
        ) : (
          chatHistory.map((msg, idx) => (
            <div key={idx} className={`chat-message ${msg.role}`}>
              <span className="role-label">{msg.role === 'user' ? 'You' : 'Jarvis'}</span>
              <p>{msg.message}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default HomeView;
