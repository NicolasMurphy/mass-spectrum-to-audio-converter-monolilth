### [2025-06-27] HMDB Fetching Script Working

- **Goals:**
  - Automate fetching `.txt` files from HMDB for a given metabolite
  - Assess performance/reliability of HMDB as a data source

- **Notes:**
  - Script returns parsed `(m/z, intensity)` tuples
  - Considered a frontend-only build in React, but opted for a backend-based approach (Flask) to allow future database use
  - HMDB is quite slow — worth exploring alternatives like MassBank or PubChem

- **Next Steps:**
  - Integrate fetcher with `converter.py` for full end-to-end audio generation
  - Evaluate performance of alternative databases (MassBank, MoNA)
  - Begin building minimal Flask app with route for input → `.wav` output
