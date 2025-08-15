import React, {useEffect, useState} from "react";
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';


export default function ConfidenceBar({currPercent, setPercent}, PREDICTION=null){  // make currPercent available in App.js


    const percentage = PREDICTION || 50;  // = ? if null
  
    useEffect ( () => {
        if (currPercent === percentage) return;

        const timer = setInterval ( () => {
            setPercent( prev => {
                if (currPercent >= percentage) {
                    clearInterval(timer);  // stop last interval
                    return prev;
                }
                return prev + 1;
            });
        }, 100);
        
        return () => clearInterval(timer);
    
    }, [currPercent]);


    return (
        <div>
            <CircularProgressbar value={currPercent} text={`${currPercent}%`}
                styles={{
                    // ref: https://www.npmjs.com/package/react-circular-progressbar
                    root: {},
                    // Customize the path, i.e. the "completed progress"
                    path: {
                      // Path color
                      stroke: `rgba(231, 39, 54, 1), ${currPercent / 100})`,
                      // Whether to use rounded or flat corners on the ends - can use 'butt' or 'round'
                      strokeLinecap: 'butt',
                      // Customize transition animation
                      transition: 'stroke-dashoffset 0.5s ease 0s',
                      // Rotate the path
                      transform: 'rotate(0.25turn)',
                      transformOrigin: 'center center',
                    },
                    // Customize the circle behind the path, i.e. the "total progress"
                    trail: {
                      // Trail color
                      stroke: '#BAF797',
                      // Whether to use rounded or flat corners on the ends - can use 'butt' or 'round'
                      strokeLinecap: 'butt',
                      // Rotate the trail
                      transform: 'rotate(0.25turn)',
                      transformOrigin: 'center center',
                    },
                    // Customize the text
                    text: {
                      // Text color
                      fill: '#FFE863',
                      // Text size
                      fontSize: '16px',
                    },
                    
                  }} />

        </div>

    )
}
