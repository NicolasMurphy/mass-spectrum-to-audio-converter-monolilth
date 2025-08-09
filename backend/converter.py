import numpy as np
from scipy.io.wavfile import write
import io


def generate_sine_wave(freq, intensity, time_array, wave_buffer):
    """
    Generate sine wave into provided buffer (reusable array)
    Args:
        freq: Frequency in Hz
        intensity: Normalized amplitude intensity (0-1)
        time_array: Pre-allocated time array
            time_array contains TIME values (in seconds):
            time_array = [0.0, 0.0000227, 0.0000454, 0.0000681, ...]
            These are moments in time: 0 seconds, 0.0000227 seconds, etc.
        wave_buffer: Pre-allocated array to write sine wave into
            wave_buffer will contain AUDIO values (-32,768 to +32,767):
            wave_buffer = [0, 15000, -8000, 22000, ...]
            These are the actual sound amplitudes
    """
    # np.iinfo(np.int16) - Output: iinfo(min=-32768, max=32767, dtype=int16)
    # We use the positive max (32,767) because the sine function will naturally create both positive and negative values when we multiply
    # Converts the normalized intensity (0-1) to find the max value of the sine wave (which also gives us the negative peak when the sine wave is calculated)
    amplitude = np.iinfo(np.int16).max * intensity

    # Write sine wave directly into the buffer
    # Calculate sine wave: 2*pi*freq*time gives the phase, sin() gives wave height
    # Phase gives us the radian values and np.sin() converts these to be -1 to 1
    # np.sin with 'out' parameter avoids creating temporary arrays
    # numpy vectorizes this so all calculations for the entire array are done at once
    np.sin(2 * np.pi * freq * time_array, out=wave_buffer)

    # Multiply by amplitude in-place (no new array created)
    # Multiplies each value in the array by the amplitude to give us the actual usable sound amplitudes
    wave_buffer *= amplitude

    return wave_buffer


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
    sample_rate: int = 44100,
    algorithm: str = "linear",
    factor: float = 10,
    modulus: float = 500,
    base: float = 100,
):
    # Pre-allocate all arrays once

    # Time array: represents sample points from 0 to duration
    time_array = np.linspace(0, duration, int(sample_rate * duration), False)

    # Final output: will contain the sum of all sine waves
    combined_wave = np.zeros_like(time_array)

    # Reusable buffer that gets overwritten for each peak
    # Instead of creating 1,815 new arrays, we reuse this one buffer 1,815 times
    sine_wave_buffer = np.zeros_like(time_array)

    transformed_data = []

    # Pre-normalize intensities to prevent huge numbers
    max_intensity = max(intensity for mz, intensity in spectrum_data)

    for mz, intensity in spectrum_data:
        if algorithm == "linear":
            freq = mz_to_frequency_linear(mz, offset=offset)
        elif algorithm == "inverse":
            freq = mz_to_frequency_inverse(mz, scale=scale, shift=shift)
        elif algorithm == "modulo":
            freq = mz_to_frequency_modulo(mz, factor=factor, modulus=modulus, base=base)
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

        # Generate sine wave using pre-allocated arrays
        # This overwrites sine_wave_buffer with new sine wave data
        sine_wave = generate_sine_wave(
            freq, normalized_intensity, time_array, sine_wave_buffer
        )

        combined_wave += sine_wave

    # Final normalization (should be minimal now since intensities are pre-normalized)
    # Just realized since this final normalization happens after the transformed data is stored, the frontend is not showing the "true" amplitude, will leave as is for now
    if np.max(np.abs(combined_wave)) > 0:
        combined_wave = combined_wave / np.max(np.abs(combined_wave))
    combined_wave = np.int16(combined_wave * np.iinfo(np.int16).max)

    wav_buffer = io.BytesIO()
    write(wav_buffer, sample_rate, combined_wave)
    wav_buffer.seek(0)

    return wav_buffer, transformed_data


# TODO: Implement custom compound generation

# def parse_spectrum_text(text_input):
#     values = text_input.strip().split()
#     float_values = [float(x) for x in values]

#     spectrum_data = []
#     for i in range(0, len(float_values), 2):
#         mz = float_values[i]
#         intensity = float_values[i + 1]
#         spectrum_data.append((mz, intensity))

#     return spectrum_data
