import pytest
from app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config["TESTING"] = True
    return app.test_client()


def test_generate_audio_with_caffeine(client):
    """Test audio generation endpoint with local database"""
    response = client.post(
        "/massbank/linear",
        json={"compound": "caffeine"},
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.get_json()

    assert "audio_base64" in data
    assert "compound" in data
    assert "caffeine" in data["compound"].lower()


def test_popular_endpoint_returns_success(client):
    response = client.get("/popular")
    assert response.status_code == 200
