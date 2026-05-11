import React from 'react';

const ActivityFeed = ({ activities }) => {
  return (
    <div className="activity-feed glass-panel">
      <h3>Live Automation Feed</h3>
      <div className="feed-list">
        {activities.length === 0 ? (
          <p className="placeholder-text">No active tasks.</p>
        ) : (
          activities.map((act, idx) => (
            <div key={idx} className="feed-item fade-in">
              <span className="feed-time">{new Date(act.timestamp).toLocaleTimeString()}</span>
              <span className="feed-msg">{act.message}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ActivityFeed;
