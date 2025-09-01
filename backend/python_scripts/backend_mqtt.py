import paho.mqtt.client as mqtt
import io
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from cnn_model import CNN_Model
import os
import sounddevice as sd

## REAL-TIME AUDIO READING FROM MICROPHONE 
# CONFIG
BROKER = "localhost"       # MQTT broker address
PORT = 1883
TOPIC_AUDIO = "lung_sounds"
TOPIC_PREDICTION = "lung_predictions"
SPECTROGRAM_DIR = "./spectrograms1"

os.makedirs(SPECTROGRAM_DIR, exist_ok=True)

# Initialize CNN model
model = CNN_Model()

SAMPLE_RATE = 16000
CHUNK_SIZE = 1024  # samples per frame

publisher_client = mqtt.Client()
publisher_client.connect(BROKER, PORT)

stream = None

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    chunk_bytes = indata.tobytes()
    publisher_client.publish(TOPIC_AUDIO, chunk_bytes)

# Helper func: AUDIO -> SPECTROGRAM
def audio_to_spectrogram(audio_array, sr, filename):
    plt.figure(figsize=(2, 2))
    plt.specgram(audio_array, Fs=sr, NFFT=256, noverlap=128, cmap='viridis')
    plt.axis('off')
    filepath = os.path.join(SPECTROGRAM_DIR, filename)
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0)
    plt.close()
    return filepath

def start_recording():
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
    global stream
    if stream is not None:
        stream.stop()
        stream.close()
        stream = None
        print("Audio stream stopped.")
    else:
        print("Audio stream is not running.")

# MQTT callback
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    if topic == "mic_control":
        if payload == "start_recording":
            print("Starting recording...")
            # call ReSpeaker start function
            start_recording()
        elif payload == "stop_recording":
            print("Stopping recording...")
            stop_recording()  # stop and process
    elif topic == "lung_sounds":
        # existing message handling
        process_lung_sound(payload)
         
    audio_bytes = msg.payload
    try:
        # read audio 
        audio_array, sr = sf.read(io.BytesIO(audio_bytes))
        
        # convert to spectrogram PNG
        spect_file = audio_to_spectrogram(audio_array, sr, "latest.png")
        
        # predict using my CNN
        prediction = model.predict(spect_file)
        
        # PREDICTION THAT FRONTEND IS GRABBING !!
        client.publish(TOPIC_PREDICTION, str(prediction))
        print("Published prediction:", prediction)
    except Exception as e:
        print("Error processing audio:", e)

# MQTT setup
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe(TOPIC_AUDIO)
print("Backend subscribed to", TOPIC_AUDIO)

client.loop_forever()