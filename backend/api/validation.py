def validate_algorithm(algorithm):
    if algorithm not in ["linear", "inverse", "modulo"]:
        raise ValueError(
            f"Unsupported algorithm: '{algorithm}'. Must be 'linear', 'inverse', or 'modulo'"
        )


def validate_and_parse_parameters(data):
    if not data:
        raise ValueError("No JSON data provided")

    # Validate sample_rate BEFORE conversion
    raw_sr = data.get("sample_rate")
    if raw_sr is not None:
        if isinstance(raw_sr, float) or (isinstance(raw_sr, str) and "." in raw_sr):
            raise ValueError("Invalid sample rate. Must be an integer.")

    # Parse and validate compound
    compound = data.get("compound")
    if not compound or not compound.strip():
        raise ValueError("No compound provided")

    # Parse all parameters with error handling
    try:
        offset = float(data.get("offset", 300))
    except (ValueError, TypeError):
        raise ValueError("Invalid offset. Must be a float.")

    try:
        scale = float(data.get("scale", 100000))
    except (ValueError, TypeError):
        raise ValueError("Invalid scale. Must be a float.")

    try:
        shift = float(data.get("shift", 1))
    except (ValueError, TypeError):
        raise ValueError("Invalid shift. Must be a float.")

    try:
        duration = float(data.get("duration", 5))
    except (ValueError, TypeError):
        raise ValueError("Invalid duration. Must be a float.")

    try:
        sample_rate = int(data.get("sample_rate", 44100))
    except (ValueError, TypeError):
        raise ValueError("Invalid sample_rate. Must be an integer.")

    try:
        factor = float(data.get("factor", 10))
    except (ValueError, TypeError):
        raise ValueError("Invalid factor. Must be a float.")

    try:
        modulus = float(data.get("modulus", 500))
    except (ValueError, TypeError):
        raise ValueError("Invalid modulus. Must be a float.")

    try:
        base = float(data.get("base", 100))
    except (ValueError, TypeError):
        raise ValueError("Invalid base. Must be a float.")

    # Validate ranges
    if not (0.01 <= duration <= 30):
        raise ValueError("Duration must be between 0.01 and 30 seconds.")

    if not 3500 <= sample_rate <= 192000:
        raise ValueError("Sample rate must be between 3500 and 192000")

    # Return all parsed parameters
    return {
        "compound": compound,
        "offset": offset,
        "scale": scale,
        "shift": shift,
        "duration": duration,
        "sample_rate": sample_rate,
        "factor": factor,
        "modulus": modulus,
        "base": base,
    }
