from typing import Union
from fastapi import FastAPI, Request


import os
from dotenv import load_dotenv  
from pymongo import MongoClient

# run: either "uvicorn main:app" or "fastapi dev main.py"
app = FastAPI()


load_dotenv()  # add mongodb connection str to .env instead of hardcoding it with your usrname & pw
MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
try:
    client.server_info()
    print("MongoDB connected!")
except Exception as e:
    print("MongoDB connection failed:", e)
    
    
print("Mongo URI loaded:", MONGO_URI)
db = client["audio_data"]
collection = db["past_results"]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/predict")
async def predict_audio(file: UploadFile):
    # Save the uploaded file temporarily
    temp_path = f"temp_uploads/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())

   
    # Optionally store in MongoDB
    record = {
        "patient_id": "user_id_or_session", 
        "timestamp": datetime.datetime.utcnow(),
        "audio_filename": file.filename,
        "spectrogram_filename": os.path.basename(spec_path),
        "predicted_label": predicted_label
    }
    collection.insert_one(record)

    # Return prediction to frontend
    return {"prediction": predicted_label}