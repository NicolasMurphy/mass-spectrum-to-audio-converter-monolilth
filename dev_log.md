### [2025-06-29] MassBank Integration, Flask API, and Frontend Preview

- **Goals:**

  - Fetch mass spectrum data via the MassBank API
  - Connect spectrum data to audio converter pipeline
  - Begin replacing legacy `.txt`-based workflow with automated CLI tool
  - Build minimal Flask API for serving audio previews
  - Implement basic HTML frontend for testing and preview

- **Notes:**

  - `get_massbank_peaks.py` was renamed to `massbank.py` for clarity
  - New CLI tool `generate_from_massbank.py` was created to fetch data and generate `.wav` files in one step
  - Verified the script returns `(m/z, intensity)` tuples, compatible with the existing audio converter
  - Basic Flask API endpoint `/generate?compound=NAME` is now functional — returns a `.wav` file using a `BytesIO` stream
  - Removed unused files: `generate_from_massbank.py` and `fetch_hmdb.py`
  - Removed unused dependency: `beautifulsoup4`

- **Next Steps:**
  - Display compound name in frontend; ensure download includes compound-specific filename
  - Add fallback support for compounds not found in MassBank (e.g., MoNA or PubChem)

### [2025-06-27] HMDB Script and MassBank API Fetch

- **Goals:**

  - Automate fetching `.txt` files from HMDB for a given metabolite
  - Explore MassBank as a faster and more structured alternative to HMDB
  - Lay groundwork for full pipeline: metabolite input → audio output

- **Notes:**

  - Initial script for HMDB fetching completed and functional, but HMDB is slow and less reliable
  - MassBank API script successfully implemented; returns `(m/z, intensity)` tuples via structured JSON
  - Considered a frontend-only build in React, but opted for backend approach (Flask) to support database use in the future
  - Plan is to prioritize MassBank moving forward due to performance and consistency

- **Next Steps:**
  - Integrate MassBank fetcher with `converter.py` for end-to-end audio generation
  - Begin Flask app: route for user input → `.wav` response
  - Optionally revisit MoNA or PubChem later for supplemental data
