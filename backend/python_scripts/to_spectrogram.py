import os
import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
from pydub import AudioSegment

# paths
audio_folder = "./audio_files"
spec_folder = "./spectrograms1"
os.makedirs(spec_folder, exist_ok=True)

# Parameters for STFT
n_fft = 1024
hop_length = 512
win_length = 1024

def convert_to_wav(file_path, temp_folder="temp_wav"):
    """If file is OGG, convert to WAV and return new path."""
    os.makedirs(temp_folder, exist_ok=True)
    if file_path.lower().endswith(".ogg"):
        audio = AudioSegment.from_ogg(file_path)
        wav_file = os.path.join(temp_folder, os.path.splitext(os.path.basename(file_path))[0] + ".wav")
        audio.export(wav_file, format="wav")
        print(f"Converted {file_path} -> {wav_file}")
        return wav_file
    else:
        return file_path  # already WAV

def plot_spectrogram(file_path, save_folder):
    y, sr = librosa.load(file_path, sr=None)
    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)
    S_db = librosa.amplitude_to_db(np.abs(S))

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')

    base = os.path.basename(file_path).replace(".wav", ".png").replace(".ogg", ".png")
    save_path = os.path.join(save_folder, base)
    plt.savefig(save_path)
    plt.close()
    print("Saved:", save_path)

# Process all audio files
for file in os.listdir(audio_folder):
    if file.lower().endswith((".wav", ".ogg")):
        file_path = os.path.join(audio_folder, file)

        # Convert if needed
        processed_path = convert_to_wav(file_path)

        # Generate spectrogram
        plot_spectrogram(processed_path, spec_folder)