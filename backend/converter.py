import numpy as np
from scipy.io.wavfile import write
import io

# import traceback

# SAMPLING_RATE = 96000
DURATION = 5.0
INTENSITY_THRESHOLD = 0.1  # Adjust as needed


def generate_sine_wave(freq, intensity, duration=DURATION, sample_rate=96000):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    amplitude = np.iinfo(np.int16).max * intensity
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave


def mz_to_frequency_linear(mz_value, offset=300):
    return mz_value + offset


def generate_combined_wav_bytes(spectrum_data, sample_rate=96000, offset=300):
    # print(f"Generating audio with sample_rate={sample_rate}")
    # traceback.print_stack()
    t = np.linspace(0, DURATION, int(sample_rate * DURATION), False)
    combined_wave = np.zeros_like(t)
    # skipped = 0
    for mz, intensity in spectrum_data:
        freq = mz_to_frequency_linear(mz, offset=offset)
        if freq <= 0:
            # skipped += 1
            continue
        sine_wave = generate_sine_wave(
            freq, intensity, duration=DURATION, sample_rate=sample_rate
        )

        combined_wave += sine_wave
    # print(f"Skipped {skipped} frequencies below 0 Hz")

    combined_wave = combined_wave / np.max(np.abs(combined_wave))
    combined_wave = np.int16(combined_wave * np.iinfo(np.int16).max)

    wav_buffer = io.BytesIO()
    write(wav_buffer, sample_rate, combined_wave)
    wav_buffer.seek(0)
    return wav_buffer
