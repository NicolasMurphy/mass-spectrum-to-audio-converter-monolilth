import base64
from audio import generate_combined_wav_bytes_and_data


class AudioGenerationService:
    """Handles the core business logic for audio generation from spectra"""

    def generate_audio_from_spectrum(self, spectrum, algorithm, parameters):
        """
        Generate audio from a compound's spectrum.

        Args:
            spectrum: List of (m/z, intensity) tuples
            algorithm: Algorithm type ('linear', 'inverse', 'modulo')
            parameters: Dict containing all generation parameters

        Returns:
            Dict containing wav_buffer, transformed_data, and audio_base64
        """
        wav_buffer, transformed_data = generate_combined_wav_bytes_and_data(
            spectrum,
            offset=parameters.get("offset", 0),
            scale=parameters.get("scale", 1),
            shift=parameters.get("shift", 0),
            duration=parameters["duration"],
            sample_rate=parameters["sample_rate"],
            algorithm=algorithm,
            factor=parameters.get("factor", 1),
            modulus=parameters.get("modulus", 1000),
            base=parameters.get("base", 2),
        )

        return {
            "wav_buffer": wav_buffer,
            "transformed_data": transformed_data,
            "audio_base64": base64.b64encode(wav_buffer.getvalue()).decode(),
        }

    def get_algorithm_parameters(self, algorithm, params):
        """Extract only the relevant parameters for the specified algorithm"""
        if algorithm == "linear":
            return {"offset": params["offset"]}
        elif algorithm == "inverse":
            return {"scale": params["scale"], "shift": params["shift"]}
        elif algorithm == "modulo":
            return {
                "factor": params["factor"],
                "modulus": params["modulus"],
                "base": params["base"],
            }
        return {}
