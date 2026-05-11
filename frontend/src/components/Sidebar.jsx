import React from 'react';

const Sidebar = ({ currentTab, setCurrentTab }) => {
  const tabs = [
    { id: 'home', label: '🎙️ Jarvis Voice' },
    { id: 'system', label: '📊 System Monitor' },
    { id: 'productivity', label: '📝 Tasks & Notes' },
    { id: 'workflows', label: '⚡ Workflows' },
  ];

  return (
    <div className="sidebar glass-panel">
      <div className="sidebar-logo">JARVIS OS</div>
      <div className="sidebar-nav">
        {tabs.map(tab => (
          <button 
            key={tab.id}
            className={`nav-btn ${currentTab === tab.id ? 'active' : ''}`}
            onClick={() => setCurrentTab(tab.id)}
          >
            {tab.label}
          </button>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
