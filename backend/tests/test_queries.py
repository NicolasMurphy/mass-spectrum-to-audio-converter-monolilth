from unittest.mock import patch, MagicMock
import sys
import os

backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from db.queries import log_search


@patch("db.queries.get_db_connection")
def test_log_search_success(mock_get_db_connection):
    """Test that log_search successfully executes database operations"""
    # Set up mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Call the function
    log_search("Caffeine", "MSBNK-ACES_SU-AS000088")

    # Verify the database operations were called
    mock_get_db_connection.assert_called_once()
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()


@patch("builtins.print")
@patch("db.queries.get_db_connection")
def test_log_search_database_error(mock_get_db_connection, mock_print):
    """Test that log_search handles database errors gracefully"""
    # Set up mock to raise an exception
    mock_get_db_connection.side_effect = Exception("Database connection failed")

    # Call the function - should not raise an exception
    log_search("Caffeine", "MSBNK-ACES_SU-AS000088")

    # Verify error was logged
    mock_print.assert_called_once_with(
        "Failed to log search: Database connection failed"
    )


@patch("db.queries.get_db_connection")
def test_get_search_history_success(mock_get_db_connection):
    """Test that get_search_history successfully executes database operations"""
    from db.queries import get_search_history

    # Set up mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []  # Simple empty result

    # Call the function
    result = get_search_history(limit=5)

    # Verify database operations
    mock_get_db_connection.assert_called_once()
    mock_conn.cursor.assert_called_once()
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_conn.close.assert_called_once()

    # Just verify it returns a list (don't care about contents)
    assert isinstance(result, list)


@patch("db.queries.get_db_connection")
def test_get_search_history_formats_data_correctly(mock_get_db_connection):
    """Test that get_search_history correctly formats database rows"""
    from datetime import datetime
    from db.queries import get_search_history

    # Set up mocks
    mock_conn = MagicMock()
    mock_cursor = MagicMock()

    mock_get_db_connection.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor

    # Mock one simple database row
    mock_datetime = datetime(2025, 1, 15, 10, 30, 0)
    mock_cursor.fetchall.return_value = [("TEST-001", "Caffeine", mock_datetime)]

    # Call the function
    result = get_search_history()

    # Verify the data transformation
    expected = [
        {
            "accession": "TEST-001",
            "compound": "Caffeine",
            "created_at": "2025-01-15T10:30:00",
        }
    ]
    assert result == expected


@patch("builtins.print")
@patch("db.queries.get_db_connection")
def test_get_search_history_database_error(mock_get_db_connection, mock_print):
    """Test that get_search_history handles database errors gracefully"""
    from db.queries import get_search_history

    # Set up mock to raise an exception
    mock_get_db_connection.side_effect = Exception("Database connection failed")

    # Call the function - should not raise an exception
    result = get_search_history()

    # Verify error was logged
    mock_print.assert_called_once_with(
        "Failed to fetch search history: Database connection failed"
    )

    # Verify it returns an empty list
    assert result == []
