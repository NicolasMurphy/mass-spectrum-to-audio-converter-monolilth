import numpy as np
from scipy.io.wavfile import write
import io

# import math

# import traceback

# SAMPLING_RATE = 96000
# DURATION = 5.0


def generate_sine_wave(freq, intensity, duration=5.0, sample_rate=96000):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    amplitude = np.iinfo(np.int16).max * intensity
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave


def mz_to_frequency_linear(mz, offset: float = 300):
    return mz + offset


# def mz_to_frequency_logarithmic(mz, logShift=1, scale=300, logOffset=-2000):
#     return (math.log2(mz + logShift) * scale) + logOffset


def mz_to_frequency_inverse(mz, scale: float = 100000, shift: float = 1):
    return scale / (mz + shift)


def generate_combined_wav_bytes(
    spectrum_data,
    offset: float = 300,
    # logShift=1,
    # scale=300,
    scale: float = 100000,
    shift: float = 1,
    duration: float = 5.0,
    sample_rate: int = 96000,
    algorithm: str = "linear",
):
    # print(f"Generating audio with sample_rate={sample_rate}")
    # traceback.print_stack()
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    combined_wave = np.zeros_like(t)
    # skipped = 0
    for mz, intensity in spectrum_data:

        if algorithm == "linear":
            freq = mz_to_frequency_linear(mz, offset=offset)
        # elif algorithm == "logarithmic":
        #     freq = mz_to_frequency_logarithmic(mz, logShift=logShift, scale=scale)
        elif algorithm == "inverse":
            freq = mz_to_frequency_inverse(mz, scale=scale, shift=shift)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        if freq <= 0:
            # skipped += 1
            continue
        sine_wave = generate_sine_wave(
            freq, intensity, duration=duration, sample_rate=sample_rate
        )

        combined_wave += sine_wave
    # print(f"Skipped {skipped} frequencies below 0 Hz")

    # Normalize and convert to 16-bit PCM
    combined_wave = combined_wave / np.max(np.abs(combined_wave))
    combined_wave = np.int16(combined_wave * np.iinfo(np.int16).max)

    wav_buffer = io.BytesIO()
    write(wav_buffer, sample_rate, combined_wave)
    wav_buffer.seek(0)
    return wav_buffer
