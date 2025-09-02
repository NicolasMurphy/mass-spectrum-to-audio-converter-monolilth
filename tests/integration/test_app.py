import pytest
from app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config["TESTING"] = True
    return app.test_client()


def test_generate_audio_with_linear_algorithm(client):
    """Test linear algorithm endpoint with local database"""
    response = client.post(
        "/massbank/linear",
        json={
            "compound": "caffeine",
            "offset": 400,
            "duration": 3,
            "sample_rate": 48000,
        },
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.get_json()

    assert "audio_base64" in data
    assert "compound" in data
    assert "caffeine" in data["compound"].lower()
    assert data["algorithm"] == "linear"
    assert "parameters" in data
    assert data["parameters"]["offset"] == 400
    assert "audio_settings" in data
    assert data["audio_settings"]["duration"] == 3
    assert data["audio_settings"]["sample_rate"] == 48000
    assert "spectrum" in data
    assert len(data["spectrum"]) > 0


def test_generate_audio_with_inverse_algorithm(client):
    """Test inverse algorithm endpoint with local database"""
    response = client.post(
        "/massbank/inverse",
        json={"compound": "biotin", "scale": 2, "shift": 100},
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.get_json()

    assert "audio_base64" in data
    assert "compound" in data
    assert "biotin" in data["compound"].lower()
    assert data["algorithm"] == "inverse"
    assert "parameters" in data
    assert data["parameters"]["scale"] == 2
    assert data["parameters"]["shift"] == 100
    assert "spectrum" in data
    assert len(data["spectrum"]) > 0


def test_generate_audio_with_modulo_algorithm(client):
    """Test modulo algorithm endpoint with local database"""
    response = client.post(
        "/massbank/modulo",
        json={
            "compound": "folate",
            "factor": 15,
            "modulus": 600,
            "base": 150,
        },
        content_type="application/json",
    )

    assert response.status_code == 200
    data = response.get_json()

    assert "audio_base64" in data
    assert "compound" in data
    assert "folate" in data["compound"].lower()
    assert data["algorithm"] == "modulo"
    assert "parameters" in data
    assert data["parameters"]["factor"] == 15
    assert data["parameters"]["modulus"] == 600
    assert data["parameters"]["base"] == 150
    assert "spectrum" in data
    assert len(data["spectrum"]) > 0


def test_generate_audio_with_nonexistent_compound(client):
    """Test error handling for compound not found in database"""
    response = client.post(
        "/massbank/linear",
        json={"compound": "nonexistentcompound12345"},
        content_type="application/json",
    )

    assert response.status_code == 404
    data = response.get_json()

    assert "error" in data
    assert "No records found" in data["error"]


def test_popular_endpoint_returns_success(client):
    response = client.get("/popular")
    assert response.status_code == 200

    data = response.get_json()
    assert "popular" in data
    assert isinstance(data["popular"], list)

    if len(data["popular"]) > 0:
        assert "compound" in data["popular"][0]
        assert "search_count" in data["popular"][0]
        assert isinstance(data["popular"][0]["search_count"], int)


def test_history_endpoint_returns_success(client):
    response = client.get("/history")
    assert response.status_code == 200

    data = response.get_json()
    assert "history" in data
    assert isinstance(data["history"], list)

    if len(data["history"]) > 0:
        assert "compound" in data["history"][0]
        assert "accession" in data["history"][0]
        assert "created_at" in data["history"][0]
