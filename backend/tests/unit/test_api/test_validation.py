from api.validation import validate_algorithm, validate_and_parse_parameters


# Validate algorithm tests


def test_validate_algorithm_with_valid_algorithms():
    validate_algorithm("linear")
    validate_algorithm("inverse")
    validate_algorithm("modulo")


def test_validate_algorithm_with_none():
    try:
        validate_algorithm(None)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Unsupported algorithm" in str(e)


def test_validate_algorithm_with_invalid_algorithm():
    try:
        validate_algorithm("Bozo")
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Unsupported algorithm" in str(e)


def test_validate_algorithm_with_empty_string():
    try:
        validate_algorithm("")
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Unsupported algorithm" in str(e)


def test_validate_algorithm_case_sensitive():
    try:
        validate_algorithm("LINEAR")
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Unsupported algorithm" in str(e)


# Validate and parse parameters tests


def test_validate_and_parse_parameters_returns_defaults():
    data = {"compound": "caffeine"}

    result = validate_and_parse_parameters(data)

    assert result["compound"] == "caffeine"
    assert result["duration"] == 5
    assert result["sample_rate"] == 44100
    assert result["offset"] == 300
    assert result["scale"] == 100000
    assert result["shift"] == 1
    assert result["factor"] == 10
    assert result["modulus"] == 500
    assert result["base"] == 100


def test_validate_and_parse_parameters_with_explicit_values():
    data = {
        "compound": "caffeine",
        "offset": 500,
        "duration": 10.5,
        "sample_rate": 48000,
    }
    result = validate_and_parse_parameters(data)

    assert result["compound"] == "caffeine"
    assert result["offset"] == 500
    assert result["duration"] == 10.5
    assert result["sample_rate"] == 48000


def test_validate_and_parse_parameters_empty_data():
    data = {}
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "No JSON data provided" == str(e)


def test_validate_and_parse_parameters_none_data():
    data = None
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "No JSON data provided" == str(e)


def test_validate_and_parse_parameters_no_compound():
    data = {"compound": ""}
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "No compound provided" == str(e)


def test_validate_and_parse_parameters_compound_too_long():
    data = {
        "compound": "2-[(4R,5S,6S,7R,9R,11E,13E,15R,16R)-15-[[(2R,3R,4R,5R,6R)-3,4-dimethoxy-6-methyl-5-oxidanyl-oxan-2-yl]oxymethyl]-6-[(2R,3R,4R,5S,6R)-4-(dimethylamino)-5-[(2S,4R,5S,6S)-4,6-dimethyl-4,5-bis(oxidanyl)oxan-2-yl]oxy-6-methyl-3-oxidanyl-oxan-2-yl]oxy-16-ethyl-5,9,13-trimethyl-4-oxidanyl-2,10-bis(oxidanylidene)-1-oxacyclohexadeca-11,13-dien-7-yl]ethanall"
    }
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Compound name is too long. Maximum length is 349 characters." == str(e)


def test_validate_and_parse_parameters_invalid_sample_rate():
    data = {"compound": "Caffeine", "sample_rate": "5000.1"}
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Invalid sample rate. Must be an integer." == str(e)


def test_validate_and_parse_parameters_invalid_offset():
    data = {"compound": "Caffeine", "offset": "Not a number"}
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Invalid offset. Must be a float." == str(e)


def test_validate_and_parse_parameters_offset_too_low():
    data = {"compound": "Caffeine", "offset": "-1000001"}
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "must be between -1,000,000 and 1,000,000." in str(e)


def test_validate_and_parse_parameters_offset_too_high():
    data = {"compound": "Caffeine", "offset": "1000001"}
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "must be between -1,000,000 and 1,000,000." in str(e)


def test_validate_and_parse_parameters_duration_too_low():
    data = {"compound": "Caffeine", "duration": "0"}
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Duration must be between 0.01 and 30 seconds." == str(e)


def test_validate_and_parse_parameters_duration_too_high():
    data = {"compound": "Caffeine", "duration": "31"}
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Duration must be between 0.01 and 30 seconds." == str(e)


def test_validate_and_parse_parameters_sample_rate_too_low():
    data = {"compound": "Caffeine", "sample_rate": "3499"}
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Sample rate must be between 3500 and 192000." == str(e)


def test_validate_and_parse_parameters_sample_rate_too_high():
    data = {"compound": "Caffeine", "sample_rate": "192001"}
    try:
        validate_and_parse_parameters(data)
        assert False, "Expected ValueError to be raised"
    except ValueError as e:
        assert "Sample rate must be between 3500 and 192000." == str(e)
