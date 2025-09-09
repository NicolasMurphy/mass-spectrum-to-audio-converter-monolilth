"""
API package for mass spectrum to audio converter.

Provides route handlers and request validation.
"""

from .routes import (
    serve_frontend,
    history,
    generate_audio_with_data,
    generate_audio_with_custom_data,
    popular,
)
from .validation import (
    validate_algorithm,
    validate_and_parse_parameters,
)

__all__ = [
    "serve_frontend",
    "history",
    "generate_audio_with_data",
    "generate_audio_with_custom_data",
    "popular",
    "validate_algorithm",
    "validate_and_parse_parameters",
]
