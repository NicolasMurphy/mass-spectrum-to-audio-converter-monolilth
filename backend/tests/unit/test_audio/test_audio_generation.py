from audio import (
    generate_sine_wave,
    generate_combined_wav_bytes_and_data,
)


# TODO: Update this unit test
# generate sine wave tests
# def test_generate_sine_wave_basic():
#     """Test that generate_sine_wave returns correct array length"""
#     wave = generate_sine_wave(440, 0.5, duration=1.0, sample_rate=44100)

#     # Should have correct number of samples
#     expected_samples = int(44100 * 1.0)  # sample_rate * duration
#     assert len(wave) == expected_samples


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
