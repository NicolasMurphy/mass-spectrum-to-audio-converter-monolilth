from unittest.mock import patch, MagicMock


# Mock psycopg2.pool BEFORE any imports that use it
with patch("psycopg2.pool.SimpleConnectionPool"):
    from db.render_massbank_queries import get_massbank_peaks


@patch("db.render_massbank_queries.get_connection")
@patch("db.render_massbank_queries.return_connection")
def test_get_massbank_peaks_success(mock_return_connection, mock_get_connection):
    """Test that get_massbank_peaks returns spectrum data for a valid compound"""
    # Set up mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mock database responses
    mock_cursor.fetchone.return_value = ("TEST-001", "Caffeine")
    mock_cursor.fetchall.return_value = [(100.5, 0.8), (200.3, 0.6)]

    # Call function
    spectrum, accession, compound_actual = get_massbank_peaks("caffeine")

    # Verify results
    assert accession == "TEST-001"
    assert compound_actual == "Caffeine"
    assert spectrum == [(100.5, 0.8), (200.3, 0.6)]

    # Verify database operations
    mock_get_connection.assert_called_once()
    mock_cursor.execute.assert_called()
    mock_cursor.close.assert_called_once()
    mock_return_connection.assert_called_once_with(mock_conn)


@patch("db.render_massbank_queries.get_connection")
@patch("db.render_massbank_queries.return_connection")
def test_get_massbank_peaks_compound_not_found(
    mock_return_connection, mock_get_connection
):
    """Test that get_massbank_peaks raises ValueError when compound is not found"""
    # Set up mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_get_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mock database returning no results (compound not found)
    mock_cursor.fetchone.return_value = None

    # Call function and expect it to raise ValueError
    try:
        get_massbank_peaks("nonexistent_compound")
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert str(e) == "No records found"

    # Verify database operations
    mock_get_connection.assert_called_once()
    mock_cursor.execute.assert_called_once()  # Only first query should run
    mock_cursor.close.assert_called_once()
    mock_return_connection.assert_called_once_with(mock_conn)
