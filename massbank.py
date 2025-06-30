import requests
import sys


def get_massbank_peaks(compound_name):

    r = requests.get(
        "https://massbank.eu/MassBank-api/records/search",
        params={"compound_name": compound_name},
    )
    r.raise_for_status()

    # Correctly access "data" instead of "accessions"
    data = r.json().get("data", [])
    if not data:
        raise ValueError("No records found")

    accession = data[0]["accession"]
    print(f"Using accession: {accession}")

    record = requests.get(
        f"https://massbank.eu/MassBank-api/records/{accession}",
    )
    record.raise_for_status()
    record_data = record.json()

    peak_values = record_data.get("peak", {}).get("peak", {}).get("values", [])
    spectrum = [(p["mz"], p["intensity"]) for p in peak_values]
    title = record_data.get("title", "")
    compound_actual = title.split(";")[0].strip() if title else "Unknown Compound"

    return spectrum, accession, compound_actual


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_massbank_peaks.py <compound_name>")
        sys.exit(1)

    compound = sys.argv[1]
    try:
        spectrum = get_massbank_peaks(compound)
        for mz, intensity in spectrum:
            print(f"m/z: {mz:.4f} | intensity: {intensity}")
    except Exception as e:
        print(f"Error: {e}")
