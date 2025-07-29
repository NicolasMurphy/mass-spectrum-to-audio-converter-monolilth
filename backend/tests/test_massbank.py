# import pytest
# from unittest.mock import patch, MagicMock

# import sys
# import os

# backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(0, backend_dir)

# from massbank import get_massbank_peaks


# @patch("massbank.requests.get")
# def test_get_massbank_peaks_success(mock_get):
#     """Test successful MassBank API call"""
#     # Mock the search response
#     search_response = MagicMock()
#     search_response.json.return_value = {
#         "data": [{"accession": "MSBNK-ACES_SU-AS000088"}]
#     }

#     # Mock the record response
#     record_response = MagicMock()
#     record_response.json.return_value = {
#         "title": "Caffeine; LC-MS/MS; Positive",
#         "peak": {
#             "peak": {
#                 "values": [
#                     {"mz": 195.0, "intensity": 100.0},
#                     {"mz": 138.0, "intensity": 50.0},
#                 ]
#             }
#         },
#     }

#     # Return search response first, then record response
#     mock_get.side_effect = [search_response, record_response]

#     # Test the function
#     spectrum, accession, compound_actual = get_massbank_peaks("caffeine")

#     # Verify results
#     assert accession == "MSBNK-ACES_SU-AS000088"
#     assert compound_actual == "Caffeine"
#     assert len(spectrum) == 2
#     expected_spectrum = [(195.0, 100.0), (138.0, 50.0)]
#     assert spectrum == expected_spectrum


# @patch("massbank.requests.get")
# def test_get_massbank_peaks_no_records(mock_get):
#     """Test MassBank API when no records are found"""
#     # Mock search response with empty data
#     search_response = MagicMock()
#     search_response.json.return_value = {"data": []}
#     mock_get.return_value = search_response

#     # Should raise ValueError
#     with pytest.raises(ValueError, match="No records found"):
#         get_massbank_peaks("nonexistent_compound")
