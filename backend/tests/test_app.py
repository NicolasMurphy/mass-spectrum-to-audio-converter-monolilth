import pytest
from unittest.mock import patch
import sys
import os
import json

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

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

    request_data = {"duration": 5.0}

    response = client.post(
        "/massbank/linear",
        data=json.dumps(request_data),
        content_type="application/json",
    )

    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data["error"] == "No compound provided"
