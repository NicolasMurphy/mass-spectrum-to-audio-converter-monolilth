import pytest
from unittest.mock import patch
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config["TESTING"] = True
    return app.test_client()


def test_missing_compound_parameter(client):
    """Test that missing compound parameter returns 400 error"""
    response = client.get("/massbank/linear")

    assert response.status_code == 400
    data = response.get_json()
    assert data["error"] == "No compound provided"


def test_invalid_algorithm(client):
    """Test that invalid algorithm returns 400 error"""
    response = client.get("/massbank/invalid_algo?compound=test")

    assert response.status_code == 400
    data = response.get_json()
    assert "Unsupported algorithm" in data["error"]


def test_invalid_duration_too_short(client):
    """Test that duration too short returns 400 error"""
    response = client.get("/massbank/linear?compound=test&duration=0.005")

    assert response.status_code == 400
    data = response.get_json()
    assert "Duration must be between 0.01 and 30 seconds" in data["error"]


def test_invalid_duration_too_long(client):
    """Test that duration too long returns 400 error"""
    response = client.get("/massbank/linear?compound=test&duration=35")

    assert response.status_code == 400
    data = response.get_json()
    assert "Duration must be between 0.01 and 30 seconds" in data["error"]


def test_invalid_sample_rate_too_low(client):
    """Test that sample rate too low returns 400 error"""
    response = client.get("/massbank/linear?compound=test&sample_rate=1000")

    assert response.status_code == 400
    data = response.get_json()
    assert "Sample rate must be between 3500 and 192000" in data["error"]


def test_invalid_sample_rate_too_high(client):
    """Test that sample rate too high returns 400 error"""
    response = client.get("/massbank/linear?compound=test&sample_rate=200000")

    assert response.status_code == 400
    data = response.get_json()
    assert "Sample rate must be between 3500 and 192000" in data["error"]


def test_invalid_sample_rate_format(client):
    """Test that non-integer sample rate returns 400 error"""
    response = client.get("/massbank/linear?compound=test&sample_rate=48000.1")

    assert response.status_code == 400
    data = response.get_json()
    assert "Invalid sample rate. Must be an integer" in data["error"]


@patch("app.get_massbank_peaks")
def test_rate_limiting_blocks_excess_requests(mock_get_peaks, client):
    """Test that too many requests get rate limited"""
    # Mock successful MassBank response
    mock_get_peaks.return_value = ([(100, 0.5)], "MSBNK-TEST-001", "Test Compound")

    # Make 10 requests (the limit)
    for i in range(10):
        response = client.get(
            "/massbank/linear?compound=test", headers={"X-Forwarded-For": "1.2.3.4"}
        )
        assert response.status_code == 200

    # The 11th request should be rate limited
    response = client.get(
        "/massbank/linear?compound=test", headers={"X-Forwarded-For": "1.2.3.4"}
    )

    assert response.status_code == 429
    data = response.get_json()
    assert "Rate limit exceeded" in data["error"]


@patch("app.get_massbank_peaks")
def test_successful_audio_generation(mock_get_peaks, client):
    """Test successful audio generation returns WAV file"""
    mock_get_peaks.return_value = ([(100, 0.5)], "MSBNK-TEST-001", "Caffeine")

    response = client.get("/massbank/linear?compound=caffeine")

    assert response.status_code == 200
    assert response.mimetype == "audio/wav"
    assert response.headers["X-Compound"] == "Caffeine"
    assert response.headers["X-Accession"] == "MSBNK-TEST-001"
