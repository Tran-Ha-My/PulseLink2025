import React from "react";

const AnalysisCard = ({ result, confidence, severity}) => {
    const getSeverityColor = (severity) => {
        return {
            'normal': 'green',
            'mild': 'orange', 
            'severe': 'red'
        }[severity];
    };
    
    const getSeverityBorder = (severity) => {
        return {
            'normal': '2px solid green',
            'mild': '2px solid orange',
            'severe': '2px solid red'   
        }[severity];
    };
    
    return (
        <div className="analysis-card" style={{
            color: getSeverityColor(severity), 
            border: getSeverityBorder(severity)
        }}>
        <div>{result}</div>

        <p>Confidence: {Math.round(confidence)}%</p>
        </div>
    );
};

export default AnalysisCard;