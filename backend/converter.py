import numpy as np
from scipy.io.wavfile import write
import io
# import os

SAMPLING_RATE = 96000
DURATION = 5.0
INTENSITY_THRESHOLD = 0.1  # Adjust as needed


def generate_sine_wave(freq, intensity, duration=DURATION, sample_rate=SAMPLING_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    amplitude = np.iinfo(np.int16).max * intensity
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave


def mz_to_frequency(mz_value):
    return 200 + (mz_value * 5)


def generate_combined_wav_bytes(spectrum_data):
    t = np.linspace(0, DURATION, int(SAMPLING_RATE * DURATION), False)
    combined_wave = np.zeros_like(t)

    for mz, intensity in spectrum_data:
        freq = mz_to_frequency(mz)
        sine_wave = generate_sine_wave(freq, intensity)
        combined_wave += sine_wave

    combined_wave = combined_wave / np.max(np.abs(combined_wave))
    combined_wave = np.int16(combined_wave * np.iinfo(np.int16).max)

    wav_buffer = io.BytesIO()
    write(wav_buffer, SAMPLING_RATE, combined_wave)
    wav_buffer.seek(0)
    return wav_buffer


# --- Legacy file-based approach (currently unused) ---

# def read_spectrum_file(file_path):
#     data = []
#     with open(file_path, "r") as file:
#         for line in file:
#             mz, intensity = map(float, line.split())
#             if intensity >= INTENSITY_THRESHOLD:
#                 data.append((mz, intensity))
#     return data

# def convert_all_txt_to_wav(directory="."):
#     for file_name in os.listdir(directory):
#         if file_name.endswith(".txt") and file_name != "requirements.txt":
#             base_name = os.path.splitext(file_name)[0]
#             txt_path = os.path.join(directory, file_name)
#             wav_path = os.path.join(directory, base_name + ".wav")

#             spectrum_data = read_spectrum_file(txt_path)
#             generate_combined_wav_file(spectrum_data, wav_path)
