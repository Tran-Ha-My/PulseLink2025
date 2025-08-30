import os
import pandas as pd
import json
import requests  # to POST JSON to FastAPI
from pymongo import MongoClient
from dotenv import load_dotenv
import datetime
import subprocess
import shutil
import librosa
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image

csv_file = "../frontend/src/python_scripts/patient_diagnosis.csv"  
print(csv_file)   
audio_folder = "../frontend/src/python_scripts/audio_files"
wav_folder = "../frontend/src/python_scripts/wav_files"
spectrogram_folder = "../frontend/src/python_scripts/spectrograms1"
fastapi_url = "http://127.0.0.1:8000/specs_png"  # POST target

# Load environment variables from .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in .env")

client = MongoClient(MONGO_URI)
db = client['audio_data'] 
collection = db['test1']  

patient_data = pd.read_csv(csv_file)

# Load the trained CNN model
model_path = "trained_cnn_model.h5" 
print(f"Loading CNN model from {"../frontend/src/python_scripts/cnn_model.py"}...")
model = load_model(model_path)
print("CNN model loaded.")

# --- OGG to WAV conversion ---
def convert_ogg_to_wav(ogg_path, wav_path):
    try:
        # Use ffmpeg for conversion (must be installed)
        subprocess.run(['ffmpeg', '-y', '-i', ogg_path, wav_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"Converted {ogg_path} -> {wav_path}")
        return True
    except Exception as e:
        print(f"Error converting {ogg_path} to WAV: {e}")
        return False

# --- Spectrogram generation ---
def generate_spectrogram(wav_path, output_png_path):
    try:
        y, sr = librosa.load(wav_path, sr=None)
        S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
        S_DB = librosa.power_to_db(S, ref=np.max)
        plt.figure(figsize=(3, 3))
        librosa.display.specshow(S_DB, sr=sr, x_axis='time', y_axis='mel')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_png_path, bbox_inches='tight', pad_inches=0)
        plt.close()
        print(f"Generated spectrogram for {wav_path} -> {output_png_path}")
        return True
    except Exception as e:
        print(f"Error generating spectrogram for {wav_path}: {e}")
        return False

# Preprocess PNG for CNN prediction
def preprocess_image(image_path, target_size=(128, 128)):
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize(target_size)
        img_array = img_to_array(img)
        img_array = img_array / 255.0  # normalize to [0,1]
        img_array = np.expand_dims(img_array, axis=0)  # batch dimension
        return img_array
    except Exception as e:
        print(f"Error preprocessing image {image_path}: {e}")
        return None

# Ensure folders exist
os.makedirs(wav_folder, exist_ok=True)
os.makedirs(spectrogram_folder, exist_ok=True)

# --- Main processing: convert OGG to WAV, generate spectrograms, build records, insert to MongoDB ---
records = []
for file in os.listdir(audio_folder):
    if file.lower().endswith(".ogg"):
        ogg_path = os.path.join(audio_folder, file)
        base = os.path.splitext(file)[0]
        patient_id = base.split('_')[0]
        wav_filename = base + ".wav"
        wav_path = os.path.join(wav_folder, wav_filename)
        png_filename = base + ".png"
        spectrogram_path = os.path.join(spectrogram_folder, png_filename)

        # OGG to WAV
        if not os.path.exists(wav_path):
            success = convert_ogg_to_wav(ogg_path, wav_path)
            if not success:
                continue
        else:
            print(f"WAV exists: {wav_path}")

        # Generate spectrogram
        if not os.path.exists(spectrogram_path):
            success = generate_spectrogram(wav_path, spectrogram_path)
            if not success:
                continue
        else:
            print(f"Spectrogram exists: {spectrogram_path}")

        # Predict label using CNN on spectrogram
        img_array = preprocess_image(spectrogram_path, target_size=(128, 128))
        if img_array is not None:
            preds = model.predict(img_array)
            pred_class_index = np.argmax(preds, axis=1)[0]
            # Get label from CSV for this patient_id
            label_row = patient_data.loc[patient_data["ID"] == patient_id, "CLASS"]
            predicted_label = label_row.values[0] if not label_row.empty else "unknown"
            print(f"Predicted label for {file}: {predicted_label}")
        else:
            predicted_label = "unknown"
            print(f"Prediction skipped for {file} due to preprocessing error.")

        # Timestamp (file creation time or now)
        try:
            timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(ogg_path)).isoformat()
        except Exception:
            timestamp = datetime.datetime.now().isoformat()

        # Build record for MongoDB
        record = {
            "patient_id": patient_id,
            "timestamp": timestamp,
            "audio_filename": file,
            "spectrogram_filename": png_filename,
            "label": predicted_label
        }
        records.append(record)
        print(f"Processed: {file} -> label: {predicted_label}")

        # Insert into MongoDB immediately
        try:
            collection.insert_one(record)
            print(f"Inserted into MongoDB: {record}")
        except Exception as e:
            print(f"MongoDB insert error: {e}")

# save JSON locally for debugging (optional)
with open("spectrogram_records.json", "w") as f:
    json.dump(records, f, indent=2)

# send JSON to FastAPI endpoint (optional)
if records:
    try:
        response = requests.post(fastapi_url, json=records)
        print(response.json())
    except Exception as e:
        print("POST error:", e)