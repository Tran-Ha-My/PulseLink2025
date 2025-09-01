import paho.mqtt.client as mqtt
import io
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from cnn_model import CNN_Model
import os
import sounddevice as sd

## REAL-TIME AUDIO READING FROM MICROPHONE 
# CONFIGURATION
BROKER = "localhost"       # MQTT broker address
PORT = 9001                # Port for WebSocket connection
TOPIC_AUDIO = "lung_sounds"
TOPIC_PREDICTION = "lung_predictions"
SPECTROGRAM_DIR = "./spectrograms1"

# Initialize MQTT client with WebSocket transport
client = mqtt.Client(transport="websockets")

# Ensure spectrogram directory exists
os.makedirs(SPECTROGRAM_DIR, exist_ok=True)

# Initialize CNN model
model = CNN_Model()

SAMPLE_RATE = 16000
CHUNK_SIZE = 1024  # samples per frame

stream = None

def audio_callback(indata, frames, time, status):
    """Callback function for audio input stream."""
    if status:
        print(f"Audio stream status: {status}")
    chunk_bytes = indata.tobytes()
    client.publish(TOPIC_AUDIO, chunk_bytes)

def audio_to_spectrogram(audio_array, sr, filename):
    """
    Converts audio array to a spectrogram image and saves it.
    Returns the filepath of the saved image.
    """
    plt.figure(figsize=(2, 2))
    plt.specgram(audio_array, Fs=sr, NFFT=256, noverlap=128, cmap='viridis')
    plt.axis('off')
    filepath = os.path.join(SPECTROGRAM_DIR, filename)
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0)
    plt.close()
    return filepath

def start_recording():
    """Starts the audio recording stream."""
    global stream
    if stream is None:
        stream = sd.InputStream(channels=1, samplerate=SAMPLE_RATE,
                                blocksize=CHUNK_SIZE,
                                callback=audio_callback)
        stream.start()
        print("Audio stream started.")
    else:
        print("Audio stream already running.")

def stop_recording():
    """Stops the audio recording stream."""
    global stream
    if stream is not None:
        stream.stop()
        stream.close()
        stream = None
        print("Audio stream stopped.")
    else:
        print("Audio stream is not running.")

def on_message(client, userdata, msg):
    """
    Callback for MQTT message reception.
    Logs received messages and handles commands and audio data.
    """
    topic = msg.topic
    payload = msg.payload
    try:
        decoded_payload = payload.decode()
    except Exception:
        decoded_payload = "<binary data>"

    print(f"Received message on topic '{topic}': {decoded_payload}")

    if topic == "mic_control":
        if decoded_payload == "start_recording":
            print("Starting recording...")
            start_recording()
        elif decoded_payload == "stop_recording":
            print("Stopping recording...")
            stop_recording()
    elif topic == TOPIC_AUDIO:
        audio_bytes = payload
        try:
            # Read audio from bytes
            audio_array, sr = sf.read(io.BytesIO(audio_bytes))
            
            # Convert audio to spectrogram PNG
            spect_file = audio_to_spectrogram(audio_array, sr, "latest.png")
            
            # Predict using CNN model
            prediction = model.predict(spect_file)
            
            # Publish prediction for frontend consumption
            client.publish(TOPIC_PREDICTION, str(prediction))
            print("Published prediction:", prediction)
        except Exception as e:
            print("Error processing audio:", e)

# MQTT client setup
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe("mic_control")
client.subscribe(TOPIC_AUDIO)
print("Backend subscribed to topics: mic_control, lung_sounds")

# Start MQTT loop to process messages indefinitely
client.loop_forever()