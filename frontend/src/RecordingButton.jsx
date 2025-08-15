import React from "react";

const RecordingButton = ({ name, className, disabled=false, onClick}) => {

    return (
      <button
        className={className}
        style={{ 
          cursor: disabled ? 'not-allowed' : 'pointer',
          opacity: disabled ? 0.6 : 1,
          width: "14vh",
          height: "7vh",
          fontSize: "1.5rem"
        }}
        onClick={onClick}
        disabled={disabled}
      >
        {name}
      </button>
    )
}

export default RecordingButton;