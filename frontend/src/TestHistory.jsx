import React from "react";

const TestHistory = () => {
    // Fake data for now
    const previousTests = [
      { id: 1, date: '2024-01-15', result: 'Normal',
confidence: 0.92 },
      { id: 2, date: '2024-01-10', result: 'Pneumonia',
confidence: 0.78 },
      { id: 3, date: '2024-01-05', result: 'Bronchitis',
confidence: 0.85 }
    ];

    const getResultIcon = (result) => {
        switch(result) {
            case 'Normal': return '✅';
            case 'Pneumonia': return '🫁';
            case 'Bronchitis': return '⚠️';
            default: return '📊';
        }
    };

    return (
      <div className="test-history">
        {previousTests.map(({id, date, result, confidence}) => 
            <div key={id} className="test-card">
                <h3>📅 {date}</h3>
                <p>{getResultIcon(result)} Result: {result}</p>
                {/* Conditional rendering for confidence color */}
                <p style={{ color: confidence > 0.8 ? '#00F5D4' : confidence > 0.5 ? '#FFA500' : '#FF1493' }}>
                    📈 Confidence: {Math.round(confidence * 100)}%
                </p>
            </div>
        )}
      </div>
    );
  };

  export default TestHistory;
