import os
import shutil
import librosa
import soundfile as sf

wav_folder = "ICBHI_challenge/wav_files"
txt_folder = "ICBHI_challenge/annotations"
output_folder = "lung_wavs"


# create output subfolder
for label in ["crackle", "wheeze", "normal"]:
    os.makedirs(os.path.join(output_folder, label), exist_ok=True)


for wav_file in os.listdir(wav_folder):
    if not wav_file.endswith('.wav'):
        continue
    base_name = os.path.splitext(wav_file)[0]
    txt_file = os.path.join(txt_folder, base_name + ".txt")

    if not os.path.exists(txt_file):
        print(f"No annotation for {wav_file}, skipping...")
        continue

    # load audio
    y, sr = librosa.load(os.path.join(wav_folder, wav_file), sr=None, mono=True)
    
    # read annotation
    with open(txt_file, "r") as f:
        lines = f.readlines()

    # lables for the .wav files (increment number order later)
    counters = {"crackle": 1, "wheeze": 1, "normal": 1, "both": 1}  


    for line in lines:
        parts = line.strip().split()
        if len(parts) < 4:
            continue

        start_time = float(parts[0])  # start of respitory cycle, i.e. first column in .txt file
        end_time = float(parts[1])
        crackle_flag = int(parts[2])  # 1 = present, 0 = absent
        wheeze_flag = int(parts[3])

        # determine segment label
        if crackle_flag == 0 and wheeze_flag == 0:
            label = "normal"
        elif crackle_flag == 1 and wheeze_flag == 1:
            label = "both"
        elif crackle_flag == 1 and wheeze_flag == 0:
            label = "crackle"
        elif crackle_flag == 0 and wheeze_flag == 1:
            label = "wheeze"

        # Segment out (so Python knows) the part the 'abnormal' part actually happens
        start_sample = int(start_time * sr) # sr = sampling rate
        end_sample = int(end_time * sr)
        segment = y[start_sample:end_sample]  # y = NumPy array

        # save segment
        out_name = f"{label}{counters[label]}.wav"
        out_path = os.path.join(output_folder, label, out_name)
        sf.write(out_path, segment, sr)
        counters[label] += 1


print("All segments are labelled !!")


