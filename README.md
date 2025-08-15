# FoundersHack2025
# Medical ML Hackathon Project Roadmap
*Lung Sound Analysis Platform - 2-3 Week Sprint*

##  Project Overview: "PulseLink"
**Goal**: Arduino-based lung sound analysis using STFT → Spectrogram → CNN → Disease prediction via web interface

**Stack**: Arduino + Node.js + MongoDB + React + TensorFlow.js + Audio Processing

**Team**: Valentin, Agnes, Nicey, Sally

---

## **SPRINT PLAN: 21-Day Execution**

### **Week 1: Foundation & MVP (Days 1-7)**

#### **Day 1-2: Architecture & Team Setup**
**Valentin**: System architect and Frontend dev

**Tasks**:
- [ ] Set up project repository with clear folder structure
- [ ] Define API endpoints and data models
- [ ] Assign team roles and responsibilities
- [ ] Set up development environment for all team members
- [ ] Build CNN model alongside Nicey

**Team Division**:
- **Valentin**: Project architect + frontend (React + data visualization) + ML integration (TensorFlow)
- **Nicey**: Backend specialist +  (Node.js + Express.js) + ML integration (TensorFlow)
- **Agnes**: Data specialist (MongoDB + Arduino integration) + data filtering (STFT)
- **Sally**: Data aquisition and medical specialist (100+ lung sound files) + lung disease research 

**Quick Architecture**:
```
Arduino Mic (ReSpeaker Mic v2.0) → Node.js API → STFT Processing → MongoDB → 
TensorFlow.js → CNN Prediction → React Dashboard
```

#### **Day 3-4: Core Technologies Crash Course**

**Your Learning Priority** (2 days intensive):

**TensorFlow.js Essentials** 
- [TensorFlow.js Quick Start](https://www.tensorflow.org/js/tutorials/setup)
- [CNN Tutorial](https://www.tensorflow.org/js/tutorials/training/building_CNN)
- **Practice**: Build simple image classification CNN

**Audio Processing** (Day 3):
- [Web Audio API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)
- [FFT in JavaScript](https://github.com/indutny/fft.js)
- **Practice**: Record audio and generate basic spectrogram

**MongoDB + Node.js** (Day 4):
- [MongoDB Crash Course](https://www.youtube.com/watch?v=pWbMrx5rVBE) (2 hours)
- [Express + MongoDB](https://www.youtube.com/watch?v=7H_QH9nipNs) (2 hours)
- **Practice**: Build CRUD API for audio samples

#### **Day 5-7: MVP Development**

**Sprint Goal**: Working end-to-end pipeline with dummy data

**Valentin Tasks**:
- [ ] Basic CNN model for spectrogram classification
- [ ] React app with audio recording interface + result dashboard
- [ ] Spectrogram visualization component
- [ ] Integration layer between all components (me or nicey)

**Nicey Tasks**:

- [ ] Basic CNN model for spectrogram classification
- [ ] Node.js API with audio upload endpoints
- [ ] Integration layer between all components


**Agnes Tasks**:
- [ ] STFT → Spectrogram conversion pipeline
- [ ] MongoDB schema and basic CRUD operations
- [ ] Arduino microphone data acquisition

**Sally Tasks**:
- [ ] Lung Sound data aquisition (100-200 sound samples- .wav file)
- [ ] Lung disease research
- [ ] Medical info sanity check and UX (user experience) head 

**Week 1 Milestone**:  **Working prototype with dummy data**

---

### **Week 2: ML Model & Real Data (Days 8-14)**

#### **Day 8-10: ML Model Development**

**Your Focus**: CNN architecture and training

**Learning Resources**:
- [Medical Audio Classification](https://www.kaggle.com/code/ashishpatel26/lung-sound-classification)
- [Spectrogram CNN Architecture](https://towardsdatascience.com/audio-classification-with-tensorflow-js-c9cb83aecf8b)
- [Transfer Learning for Medical Audio](https://arxiv.org/abs/1912.07875)

**Implementation Steps**:
1. **Data Preparation**:
   ```javascript
   // Lung sound categories
   const diseaseCategories = [
     'normal', 'pneumonia', 'bronchitis', 'asthma', 'copd'
   ];
   ```

2. **CNN Model Architecture**:
   ```javascript
   const model = tf.sequential({
     layers: [
       tf.layers.conv2d({filters: 32, kernelSize: 3, activation: 'relu'}),
       tf.layers.maxPooling2d({poolSize: 2}),
       tf.layers.conv2d({filters: 64, kernelSize: 3, activation: 'relu'}),
       tf.layers.maxPooling2d({poolSize: 2}),
       tf.layers.flatten(),
       tf.layers.dense({units: 128, activation: 'relu'}),
       tf.layers.dense({units: 5, activation: 'softmax'}) // 5 disease categories
     ]
   });
   ```

3. **Training Pipeline**:
   - Find lung sound dataset (Respiratory Sound Database)
   - Implement data augmentation
   - Train model with validation split

**Tasks**:
- [ ] Implement STFT algorithm
- [ ] Create spectrogram generation function
- [ ] Build and train CNN model
- [ ] Model evaluation and optimization

#### **Day 11-14: Integration & Real Data**

**Sprint Goal**: Real Arduino data through complete pipeline

**Val's Tasks**:
- [ ] Integrate trained model with web interface
- [ ] Real-time audio processing pipeline
- [ ] Model serving API endpoints

**Team Tasks**:
- [ ] Arduino microphone calibration and data collection
- [ ] Real-time audio streaming to backend
- [ ] Enhanced UI with prediction confidence scores
- [ ] Database optimization for audio storage

**Technical Challenges to Solve**:
1. **Real-time Audio Processing**:
   ```javascript
   // STFT Implementation
   function computeSTFT(audioBuffer, windowSize = 1024, hopLength = 512) {
     // Windowing + FFT + Magnitude spectrum
   }
   
   // Spectrogram Generation
   function generateSpectrogram(stftResult) {
     // Convert to image format for CNN
   }
   ```

2. **Arduino Integration**:
   ```arduino
   // Arduino code for microphone sampling
   void setup() {
     // ADC configuration for audio sampling
   }
   
   void loop() {
     // Real-time audio capture and transmission
   }
   ```

**Week 2 Milestone**:  **Real Arduino data → ML prediction → Web display**

---

### **Week 3: Polish & Presentation (Days 15-21)**

#### **Day 15-17: Advanced Features**

**Your Focus**: Performance optimization and advanced ML features

**Advanced Features to Implement**:
- [ ] Real-time prediction with confidence intervals
- [ ] Historical analysis and trend visualization
- [ ] Model uncertainty quantification
- [ ] Prediction explanation (which frequency bands contributed)

**Technical Enhancements**:
```javascript
// Advanced prediction with uncertainty
async function predictWithUncertainty(spectrogram) {
  const predictions = [];
  for (let i = 0; i < 10; i++) {
    // Monte Carlo dropout for uncertainty estimation
    const pred = await model.predict(spectrogram);
    predictions.push(pred);
  }
  return calculateUncertainty(predictions);
}
```

#### **Day 18-19: Testing & Bug Fixes**

**Sprint Goal**: Production-ready application

**Testing Strategy**:
- [ ] Unit tests for STFT and spectrogram functions
- [ ] Integration tests for API endpoints
- [ ] End-to-end testing with real hardware
- [ ] Performance testing with multiple users

**Quality Assurance**:
- [ ] Code review and refactoring
- [ ] Error handling and edge cases
- [ ] UI/UX polish and responsiveness
- [ ] Documentation and API docs

#### **Day 20-21: Presentation Prep**

**Demo Script**:
1. **Problem Statement** (30 seconds)
2. **Live Demo** (2 minutes):
   - Record lung sound with Arduino
   - Show real-time spectrogram generation
   - Display ML prediction with confidence
   - Historical analysis dashboard
3. **Technical Architecture** (1 minute)
4. **Business Case & Impact** (30 seconds)

**Presentation Materials**:
- [ ] Live demo environment setup
- [ ] Backup demo video (in case of technical issues)
- [ ] Architecture diagrams
- [ ] Performance metrics and accuracy results

---

##  **TECHNICAL IMPLEMENTATION GUIDE**

### **Day-by-Day Learning Resources**

#### **Day 1-2: Quick Setup**
```bash
# Project structure
mkdir pulse-link
cd pulse-link
mkdir client server arduino-code
npx create-react-app client
cd server && npm init -y
npm install express mongoose multer cors body-parser
```

#### **Day 3: TensorFlow.js Crash Course**

- [TensorFlow.js Basics](https://www.youtube.com/watch?v=WIHZ7kjJ35o) - 1 hour
- [CNN from Scratch](https://www.youtube.com/watch?v=aircAruvnKk) - 1 hour
- Practice: Build MNIST classifier - 1 hour


- [Web Audio API Tutorial](https://www.youtube.com/watch?v=8aQwOBVaXHE) - 1 hour
- [Audio Processing in JS](https://www.youtube.com/watch?v=ZuNiN7PzoZI) - 1 hour
- Practice: Record and visualize audio - 1 hour

#### **Day 4: Backend Foundations**
- [Node.js + MongoDB](https://www.youtube.com/watch?v=fBNz5xF-Kx4) - 2 hours
- [File Upload with Multer](https://www.youtube.com/watch?v=ysS4sL8oKQM) - 1 hour
- Practice: Build audio upload API - 2 hours

### **Critical Code Snippets**

#### **STFT Implementation**:
```javascript
// stft.js
import * as tf from '@tensorflow/tfjs';

export function stft(signal, frameLength = 1024, frameStep = 512) {
  return tf.signal.stft(signal, frameLength, frameStep).abs();
}

export function spectrogramToImage(stft) {
  // Convert STFT to image format for CNN
  const normalized = tf.div(stft, tf.max(stft));
  return tf.expandDims(normalized, -1); // Add channel dimension
}
```

#### **CNN Model**:
```javascript
// model.js
export function createLungSoundModel() {
  const model = tf.sequential({
    layers: [
      tf.layers.conv2d({
        inputShape: [128, 128, 1], // Spectrogram dimensions
        filters: 32,
        kernelSize: 3,
        activation: 'relu'
      }),
      tf.layers.maxPooling2d({poolSize: 2}),
      tf.layers.conv2d({filters: 64, kernelSize: 3, activation: 'relu'}),
      tf.layers.maxPooling2d({poolSize: 2}),
      tf.layers.conv2d({filters: 64, kernelSize: 3, activation: 'relu'}),
      tf.layers.flatten(),
      tf.layers.dropout({rate: 0.5}),
      tf.layers.dense({units: 128, activation: 'relu'}),
      tf.layers.dense({units: 5, activation: 'softmax'}) // 5 disease classes
    ]
  });
  
  model.compile({
    optimizer: 'adam',
    loss: 'categoricalCrossentropy',
    metrics: ['accuracy']
  });
  
  return model;
}
```

#### **Real-time Audio Processing**:
```javascript
// audioProcessor.js
export class AudioProcessor {
  constructor() {
    this.audioContext = new AudioContext();
    this.analyser = this.audioContext.createAnalyser();
  }
  
  async startRecording() {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const source = this.audioContext.createMediaStreamSource(stream);
    source.connect(this.analyser);
    
    this.analyser.fftSize = 2048;
    const bufferLength = this.analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);
    
    const processAudio = () => {
      this.analyser.getByteFrequencyData(dataArray);
      // Process audio data and generate spectrogram
      this.processAudioFrame(dataArray);
      requestAnimationFrame(processAudio);
    };
    
    processAudio();
  }
}
```

### **Arduino Integration**:
```arduino
// lung_sound_sensor.ino
const int micPin = A0;
const int sampleRate = 8000; // 8kHz sampling
const int bufferSize = 1024;

void setup() {
  Serial.begin(115200);
  analogReference(EXTERNAL); // For better ADC resolution
}

void loop() {
  int16_t audioBuffer[bufferSize];
  
  // Collect audio samples
  for (int i = 0; i < bufferSize; i++) {
    audioBuffer[i] = analogRead(micPin);
    delayMicroseconds(125); // 8kHz sampling
  }
  
  // Send via Serial to Node.js
  Serial.write((uint8_t*)audioBuffer, bufferSize * 2);
  delay(100);
}
```

---

##  **SUCCESS METRICS & GOALS**

### **Technical Objectives**:
- [ ] >80% accuracy on test dataset
- [ ] <2 second prediction latency
- [ ] Real-time audio processing at 44.1kHz
- [ ] Responsive web interface on mobile/desktop
- [ ] Scalable to 100+ concurrent users

### **Demo Objectives**:
- [ ] Flawless live demonstration
- [ ] Clear business value proposition
- [ ] Technical depth demonstration
- [ ] Team coordination showcase

### **Learning Objectives**:
- [ ] Full-stack development proficiency
- [ ] ML model deployment experience
- [ ] Real-time system architecture
- [ ] Hardware-software integration

---

##  **RISK MITIGATION**

### **High-Risk Areas**:
1. **Arduino Integration**: Have backup with computer microphone
2. **Model Training Time**: Use pre-trained models if needed
3. **Real-time Performance**: Optimize with Web Workers
4. **Team Coordination**: Daily standups and clear task division

### **Backup Plans**:
- **Plan B**: Use computer microphone instead of Arduino
- **Plan C**: Pre-recorded audio samples for demo
- **Plan D**: Simplified model with basic classification

---

## 🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀🚀 **FINAL WEEK PREPARATION**

### **Hackathon Day Strategy**:
1. **Setup** (30 min): Deploy application, test all connections
2. **Practice Demo** (30 min): Run through presentation 3 times
3. **Pitch Preparation** (60 min): Fine-tune business case and technical explanation
4. **Contingency Testing** (30 min): Test backup plans

### **Presentation Structure** (5 minutes total):
- **Hook** (30s): "This is a medical bill of an average Joe" or "Lung diseases affect 500M people globally..."
- **Demo** (2.5m): Live Arduino → AI → Diagnosis pipeline
- **Tech Deep Dive** (1.5m): STFT, CNN, real-time architecture
- **Business Case** (30s): Market size, scalability, impact



