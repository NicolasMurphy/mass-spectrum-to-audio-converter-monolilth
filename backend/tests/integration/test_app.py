import pytest
from unittest.mock import patch
import json

with patch("db.init_pool"):
    from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    app.config["TESTING"] = True
    return app.test_client()


def test_post_endpoint_rejects_missing_json(client):
    """Test that POST /massbank/linear requires JSON data"""

    response = client.post(
        "/massbank/linear",
        data="{}",
        content_type="application/json",
    )

    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data["error"] == "No JSON data provided"


def test_post_endpoint_rejects_missing_compound(client):
    """Test that POST /massbank/linear requires compound parameter"""

    request_data = {"duration": 5}

    response = client.post(
        "/massbank/linear",
        data=json.dumps(request_data),
        content_type="application/json",
    )

    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data["error"] == "No compound provided"


def test_post_endpoint_rejects_invalid_algorithm(client):
    """Test that POST /massbank/<algorithm> rejects unsupported algorithms"""

    request_data = {"compound": "caffeine"}

    response = client.post(
        "/massbank/fourier",
        data=json.dumps(request_data),
        content_type="application/json",
    )

    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert (
        response_data["error"]
        == "Unsupported algorithm: 'fourier'. Must be 'linear', 'inverse', or 'modulo'"
    )


def test_post_endpoint_rejects_invalid_duration(client):
    """Test that POST /massbank/linear rejects duration outside valid range"""

    request_data = {"compound": "caffeine", "duration": 50.0}

    response = client.post(
        "/massbank/linear",
        data=json.dumps(request_data),
        content_type="application/json",
    )

    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data["error"] == "Duration must be between 0.01 and 30 seconds."


def test_post_endpoint_rejects_invalid_sample_rate_range(client):
    """Test that POST /massbank/linear rejects sample rate outside valid range"""

    request_data = {"compound": "caffeine", "sample_rate": 2000}

    response = client.post(
        "/massbank/linear",
        data=json.dumps(request_data),
        content_type="application/json",
    )

    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data["error"] == "Sample rate must be between 3500 and 192000."


def test_post_endpoint_rejects_invalid_sample_rate_type(client):
    """Test that POST /massbank/linear rejects non-integer sample rate"""

    request_data = {"compound": "caffeine", "sample_rate": 44100.5}

    response = client.post(
        "/massbank/linear",
        data=json.dumps(request_data),
        content_type="application/json",
    )

    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data["error"] == "Invalid sample rate. Must be an integer."
