import numpy as np
from scipy.io.wavfile import write
import io


def generate_sine_wave(freq, intensity, duration=5.0, sample_rate=96000):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    amplitude = np.iinfo(np.int16).max * intensity
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave


def mz_to_frequency_linear(mz, offset: float = 300):
    return mz + offset


def mz_to_frequency_inverse(mz, scale: float = 100000, shift: float = 1):
    return scale / (mz + shift)


def mz_to_frequency_modulo(
    mz, factor: float = 10, modulus: float = 500, base: float = 100
):
    return ((mz * factor) % modulus) + base


def generate_combined_wav_bytes_and_data(
    spectrum_data,
    offset: float = 300,
    scale: float = 100000,
    shift: float = 1,
    duration: float = 5.0,
    sample_rate: int = 96000,
    algorithm: str = "linear",
    factor: float = 10,
    modulus: float = 500,
    base: float = 100,
):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    combined_wave = np.zeros_like(t)
    transformed_data = []

    # Pre-normalize intensities to prevent huge numbers
    max_intensity = max(intensity for mz, intensity in spectrum_data)

    for mz, intensity in spectrum_data:
        if algorithm == "linear":
            freq = mz_to_frequency_linear(mz, offset=offset)
        elif algorithm == "inverse":
            freq = mz_to_frequency_inverse(mz, scale=scale, shift=shift)
        elif algorithm == "modulo":
            freq = mz_to_frequency_modulo(
                mz, factor=factor, modulus=modulus, base=base
            )
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

        # Normalize intensity to 0-1 range BEFORE generating sine wave
        normalized_intensity = intensity / max_intensity

        # Store transformation data with the normalized amplitude
        transformed_data.append(
            {
                "mz": mz,
                "frequency": freq,
                "intensity": intensity,  # Keep original intensity
                "amplitude_linear": normalized_intensity,  # 0-1 range
                "amplitude_db": (
                    20 * np.log10(normalized_intensity)
                    if normalized_intensity > 0
                    else -np.inf
                ),
            }
        )

        if freq <= 0:
            continue

        # Generate sine wave with pre-normalized intensity
        sine_wave = generate_sine_wave(
            freq, normalized_intensity, duration=duration, sample_rate=sample_rate
        )

        combined_wave += sine_wave

    # Final normalization (should be minimal now since intensities are pre-normalized)
    if np.max(np.abs(combined_wave)) > 0:
        combined_wave = combined_wave / np.max(np.abs(combined_wave))
    combined_wave = np.int16(combined_wave * np.iinfo(np.int16).max)

    wav_buffer = io.BytesIO()
    write(wav_buffer, sample_rate, combined_wave)
    wav_buffer.seek(0)

    return wav_buffer, transformed_data
