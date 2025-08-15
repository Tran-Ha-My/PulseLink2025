import React from "react";

const StatusDisplay = ({ status, timer }) => {
    let statusText;
    if (status === 'idle') {
        statusText = "⚪ Ready to record";
    } else if (status === 'recording') {
        statusText = "🔴 Recording in progress...";
    } else if (status === 'paused') {
        statusText = "⏸️ Recording paused";
    } else if (status === 'stopped') {
        statusText = "⏹️ Recording stopped";
    }
    
    // helper function to format MM:SS
    const formatTime = (totalSeconds) => {
        const mins = Math.floor(totalSeconds/60);
        const secs = totalSeconds % 60;

        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    return (
        <div className="status-display">
            <h2>Status: {statusText}</h2>
          
            {(status === 'recording' || status === 'paused') && <p className="modern-timeline">{formatTime(timer)}</p>}  
            {/* AND operator (&&) */}
           
        </div>
    );
}

export default StatusDisplay;