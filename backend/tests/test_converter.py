import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from converter import (
    mz_to_frequency_linear,
    mz_to_frequency_inverse,
    generate_sine_wave,
)


# linear tests
def test_mz_to_frequency_linear_basic():
    """Test that linear frequency conversion works with basic values"""
    # Default offset is +300
    assert mz_to_frequency_linear(100) == 400  # 100 + 300
    assert mz_to_frequency_linear(200) == 500  # 200 + 300
    assert mz_to_frequency_linear(0) == 300  # 0 + 300


def test_mz_to_frequency_linear_custom_offset():
    """Test linear frequency conversion with custom offset"""
    assert mz_to_frequency_linear(100, offset=500) == 600  # 100 + 500
    assert mz_to_frequency_linear(50, offset=0) == 50  # 50 + 0


# inverse tests
def test_mz_to_frequency_inverse_basic():
    """Test that inverse frequency conversion works with basic values"""
    # Default: scale=100000, shift=1
    assert mz_to_frequency_inverse(99) == 1000  # 100000 / (99 + 1) = 1000
    assert mz_to_frequency_inverse(999) == 100  # 100000 / (999 + 1) = 100


def test_mz_to_frequency_inverse_custom_scale():
    """Test inverse frequency conversion with custom scale"""
    # Custom scale=50000, default shift=1
    assert mz_to_frequency_inverse(99, scale=50000) == 500  # 50000 / (99 + 1)
    assert mz_to_frequency_inverse(999, scale=50000) == 50  # 50000 / (999 + 1)


def test_mz_to_frequency_inverse_custom_shift():
    """Test inverse frequency conversion with custom shift"""
    # Default scale=100000, custom shift=2
    assert mz_to_frequency_inverse(98, shift=2) == 1000  # 100000 / (98 + 2)
    assert mz_to_frequency_inverse(998, shift=2) == 100  # 100000 / (998 + 2)


def test_mz_to_frequency_inverse_custom_both():
    """Test inverse frequency conversion with both custom scale and shift"""
    # Custom scale=1000, custom shift=4
    assert mz_to_frequency_inverse(1, scale=1000, shift=4) == 200  # 1000 / (1 + 4)
    assert mz_to_frequency_inverse(96, scale=1000, shift=4) == 10  # 1000 / (96 + 4)


def test_mz_to_frequency_inverse_zero_mz():
    """Test inverse frequency conversion with zero m/z value"""
    # Should handle mz=0 without issues
    assert mz_to_frequency_inverse(0) == 100000  # 100000 / (0 + 1)
    assert mz_to_frequency_inverse(0, scale=1000, shift=2) == 500  # 1000 / (0 + 2)


# generate sine wave tests
def test_generate_sine_wave_basic():
    """Test that generate_sine_wave returns correct array length"""
    wave = generate_sine_wave(440, 0.5, duration=1.0, sample_rate=44100)

    # Should have correct number of samples
    expected_samples = int(44100 * 1.0)  # sample_rate * duration
    assert len(wave) == expected_samples


# python -m pytest backend/tests/ -v

# python -m pytest backend/tests/ --cov=backend --cov-report=html
