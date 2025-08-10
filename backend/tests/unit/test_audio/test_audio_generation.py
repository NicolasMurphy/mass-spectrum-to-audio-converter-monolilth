from audio import (
    generate_sine_wave,
    generate_combined_wav_bytes_and_data,
)
import numpy as np


# generate sine wave tests
def test_generate_sine_wave_returns_buffer():
    """Test that generate_sine_wave returns the same buffer object it was given"""

    time_array = np.linspace(0, 0.1, 800, False)  # dummy data
    wave_buffer = np.zeros_like(time_array)  # array of 800 zeroes

    result = generate_sine_wave(440, 0.5, time_array, wave_buffer)

    assert result is wave_buffer


def test_generate_sine_wave_modifies_buffer():
    """Test that generate_sine_wave modifies the wave_buffer (not all zeros)"""

    time_array = np.linspace(0, 0.1, 800, False)  # dummy data
    wave_buffer = np.zeros_like(time_array)  # array of 800 zeroes

    generate_sine_wave(440, 0.5, time_array, wave_buffer)

    assert not np.all(wave_buffer == 0)


# generate combined wav bytes and data tests
def test_generate_combined_wav_bytes_and_data_basic():
    """Test that generate_combined_wav_bytes_and_data returns valid WAV buffer and transformation data"""
    spectrum_data = [(100, 0.5), (200, 0.3)]
    wav_buffer, transformed_data = generate_combined_wav_bytes_and_data(
        spectrum_data,
        duration=0.1,  # Short duration for fast test
        sample_rate=8000,  # Low sample rate for fast test
        algorithm="linear",
    )

    # Should return a BytesIO buffer
    assert hasattr(wav_buffer, "read")
    assert hasattr(wav_buffer, "seek")

    # Buffer should have content
    wav_buffer.seek(0)
    content = wav_buffer.read()
    assert len(content) > 0

    # Should return transformation data
    assert isinstance(transformed_data, list)
    assert len(transformed_data) == 2  # Same length as input spectrum

    # Each data point should have expected fields
    for item in transformed_data:
        assert "mz" in item
        assert "frequency" in item
        assert "intensity" in item
        assert "amplitude_linear" in item
        assert "amplitude_db" in item
