import os
import librosa
import numpy as np
import pandas as pd
from pydub import AudioSegment, silence
from tempfile import NamedTemporaryFile
import uuid


# Set base path
BASE_DIR = "audio/hakim/CWS"

# Store results
results = []


def analyze_audio(mp3_path, group, subtype):
    try:
        # Convert MP3 to WAV using a unique filename
        audio = AudioSegment.from_mp3(mp3_path)
        tmp_wav_path = f"temp_{uuid.uuid4().hex}.wav"
        audio.export(tmp_wav_path, format="wav")

        # Load with librosa
        y, sr = librosa.load(tmp_wav_path)
        duration = librosa.get_duration(y=y, sr=sr)

        # Extract pitch
        f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
        pitch_var = np.nanstd(f0)

        # Silence detection
        silent_parts = silence.detect_silence(audio, min_silence_len=1000, silence_thresh=-40)
        silence_duration = sum([end - start for start, end in silent_parts]) / 1000.0

        # Clean up temp file
        os.remove(tmp_wav_path)

        return {
            "file": os.path.basename(mp3_path),
            "group": group,
            "subtype": subtype,
            "duration_sec": duration,
            "pitch_variation": pitch_var,
            "silence_duration_sec": silence_duration
        }

    except Exception as e:
        print(f"⚠️ Error processing {mp3_path}: {e}")
        return None
# Walk through all files in CWS subfolders
for subtype in os.listdir(BASE_DIR):
    subtype_path = os.path.join(BASE_DIR, subtype)
    if not os.path.isdir(subtype_path):
        continue
    for filename in os.listdir(subtype_path):
        if filename.endswith(".mp3"):
            print(f"🔍 Processing {filename} in subtype {subtype}...")
            file_path = os.path.join(subtype_path, filename)
            features = analyze_audio(file_path, group="CWS", subtype=subtype)
            if features:
                results.append(features)
        print(f"✅ Processed {filename} in subtype {subtype}")
    print(f"✅ Finished processing subtype {subtype}")
print("✅ All subtypes processed successfully.")

# Save to CSV
df = pd.DataFrame(results)
df.to_csv("hakim_cws_features.csv", index=False)
print("✅ Analysis complete. Saved to hakim_cws_features.csv")
