import React, { useState, useEffect } from 'react';
import './App.css';
import RecordingButton from './RecordingButton';
import StatusDisplay from './StatusDisplay';  
import TestHistory from './TestHistory';
import AnalysisCard from './AnalysisCard';
import ThreeDScene from './3d';
import ConfidenceBar from './ConfidenceBar';
import { color } from 'three/src/nodes/TSL.js';


function App() {
  const [recordingStatus, setRecordingStatus] = useState('idle');
  const [timer, setTimer] = useState(0);
  const [typedText, setTypedText] = useState('');
  const [currPercent, setPercent] = useState(0);
  let PREDICTION = 50;
  const result = 'COVID-19'  // IF CONDITIONS HERE

  /* TYPEWRITTER EFFECT */
  useEffect(() => {
    const brand = "PulseLink™";
    let i = 0;
    let currentText = "";
  
    const timerId = setInterval(() => {
      if (i < brand.length) {
        currentText += brand[i];
        setTypedText(currentText + "|");
        i++;
      } else {
        setTypedText(currentText);
        clearInterval(timerId); // Stop the interval when typing is complete
      }
    }, 150);
  
    return () => clearInterval(timerId); // Cleanup 
  }, []); // Empty dependency array to run only once when page loads


  /* HANDLE TIMER LOGIC WITH useEffect() - start when recording */
  useEffect( () => {
    let timerId = null;
    if (recordingStatus === 'recording') {
      timerId = setInterval( () => {
          setTimer(prevTime => prevTime + 1);
      }, 1000);
    } else if (recordingStatus === 'idle') {
      setTimer(0);  
    } // cleanup function !!
      return () => { if (timerId) {clearInterval(timerId);}}

 }, [recordingStatus] );  // run once (hence dependency arr = []) when component loads
 
 
  const handleStart = () => {
    setRecordingStatus('recording');
  };

  const handleStop = () => {
    setRecordingStatus('idle');
  }

  const handlePause = () => {
    setRecordingStatus('paused');
  }
 

  return (
    <div className="App">
      <div id="three-container">

      <ThreeDScene  />

      </div>
        

      <header className="App-header">
        <h1>{typedText}</h1>
      </header>
 
      <main>
          <div className='horizontal-container'>
                 
              <div className='vertical-container'>
                    {/* Recording Section */}
                    <section className="recording-section" style={{width: "80vh", fontSize:"2vh"}}>
                    <h2>🎤 Record Your Cough</h2>
                    <div className="controls">
                        <RecordingButton name="▶️ Start" className="action-button button-start" onClick={handleStart}/>
                        <RecordingButton name="⏸️ Pause"  className="action-button button-pause"  onClick={handlePause}/>
                        <RecordingButton name="⏹️ Stop" className="action-button button-stop" onClick={handleStop} />

                    </div>
                    <StatusDisplay status={recordingStatus} timer={timer} />
                  </section>

                      {/* Results Section */}
                  <section className="results-section" style={{width: "80vh"}}>
                      <h2 style={{fontWeight: 'bold'}}><img src='/pie-chart.svg' alt="icon" width={40} height={40} />  Disease Analysis</h2>
                      <AnalysisCard
                        confidence={currPercent}
                        result={
                          currPercent < PREDICTION / 2? (
                            <h4>Analyzing...</h4>
                          ) : currPercent < PREDICTION ? (
                            <h4>Hang in there...</h4>
                          ) : (
                            <h4>
                              Prediction complete! You have:
                              <br />
                              <br />
                              <span style={{ fontWeight: "bolder", fontSize: "larger" }}>
                                🚨{result}🚨
                              </span>
                            </h4>
                          )
                        }
                      />
                      {/* We'll add chart here later */}
                      <div className="results-section chart-placeholder" style={{width: 500, height: 500}} >
                        <ConfidenceBar currPercent={currPercent} setPercent={setPercent}/>
                      </div>
                  </section>

              </div>
                    {/* History Section */}
                  <section className="history-section">
                        <h2>📋 Previous Tests</h2>
                        <TestHistory />
                        {/* MongoDB data will go here */}
                  </section>
          </div>


      

      </main>
    </div>
  );
}

export default App;
