import sys
from massbank import get_massbank_peaks
from converter import generate_combined_wav_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_from_massbank.py <compound_name>")
        sys.exit(1)

    compound = sys.argv[1]

    try:
        spectrum = get_massbank_peaks(compound)
        if not spectrum:
            raise ValueError("No spectrum data found.")

        generate_combined_wav_file(spectrum, "output.wav")
        print("Audio file 'output.wav' generated successfully.")

    except Exception as e:
        print(f"Error: {e}")
