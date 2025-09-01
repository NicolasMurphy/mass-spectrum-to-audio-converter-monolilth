import pytest
from db import get_massbank_peaks, init_pool, close_all_connections


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    """Initialize database connection pool for integration tests"""
    init_pool()
    yield
    close_all_connections()


def test_get_massbank_peaks():
    """Test get_massbank_peaks with local database"""
    spectrum, accession, compound_actual = get_massbank_peaks("caffeine")

    assert len(spectrum) > 0
    assert accession is not None
    assert "caffeine" in compound_actual.lower()

# docker-compose exec app python -m pytest tests/ -v
