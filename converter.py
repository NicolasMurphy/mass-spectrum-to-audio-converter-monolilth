import numpy as np
from scipy.io.wavfile import write

SAMPLING_RATE = 44100
DURATION = 5.0
INTENSITY_THRESHOLD = 0.4


def generate_sine_wave(freq, intensity, duration=DURATION, sample_rate=SAMPLING_RATE):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    amplitude = np.iinfo(np.int16).max * intensity
    wave = amplitude * np.sin(2 * np.pi * freq * t)
    return wave


def read_spectrum_file(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            mz, intensity = map(float, line.split())
            if intensity >= INTENSITY_THRESHOLD:
                data.append((mz, intensity))
    return data


def mz_to_frequency(mz_value):
    return 200 + (mz_value * 5)


def generate_combined_wav_file(spectrum_data, output_file):
    t = np.linspace(0, DURATION, int(SAMPLING_RATE * DURATION), False)
    combined_wave = np.zeros_like(t)

    for mz, intensity in spectrum_data:
        freq = mz_to_frequency(mz)
        sine_wave = generate_sine_wave(freq, intensity)
        combined_wave += sine_wave

    combined_wave = combined_wave / np.max(np.abs(combined_wave))

    combined_wave = np.int16(combined_wave * np.iinfo(np.int16).max)

    write(output_file, SAMPLING_RATE, combined_wave)
    print(f"WAV file generated: {output_file}")


if __name__ == "__main__":
    spectrum_file = "spectrum.txt"
    output_wav = "output.wav"

    spectrum_data = read_spectrum_file(spectrum_file)
    generate_combined_wav_file(spectrum_data, output_wav)
