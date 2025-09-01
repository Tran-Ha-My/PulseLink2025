import paho.mqtt.client as mqtt
import io
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from cnn_model import CNN_Model
import os
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

# Helper func: AUDIO -> SPECTROGRAM
def audio_to_spectrogram(audio_array, sr, filename):
    plt.figure(figsize=(2, 2))
    plt.specgram(audio_array, Fs=sr, NFFT=256, noverlap=128, cmap='viridis')
    plt.axis('off')
    filepath = os.path.join(SPECTROGRAM_DIR, filename)
    plt.savefig(filepath, bbox_inches='tight', pad_inches=0)
    plt.close()
    return filepath

# MQTT callback
def on_message(client, userdata, msg):
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

# continuously records audio and publishes it to the MQTT topic
# completing the end-to-end real-time pipeline
import sounddevice as sd

SAMPLE_RATE = 16000
CHUNK_SIZE = 1024  # samples per frame

# Publisher client
publisher_client = mqtt.Client()
publisher_client.connect(BROKER, PORT)

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    chunk_bytes = indata.tobytes()
    publisher_client.publish(TOPIC_AUDIO, chunk_bytes)

# Start audio stream
with sd.InputStream(channels=1, samplerate=SAMPLE_RATE,
                    blocksize=CHUNK_SIZE,
                    callback=audio_callback):
    print("Recording and publishing ReSpeaker audio to MQTT...")
    sd.sleep(1000000)
    
    