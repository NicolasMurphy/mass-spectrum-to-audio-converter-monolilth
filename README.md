# Mass Spectrum to Audio Converter

A project for converting mass spectrum `.txt` files into `.wav` files.

## Instructions:

1. Go to [HMDB](https://hmdb.ca/) (or any database that includes Spectra data).
2. Search for a chemical (drug, hormone, protein, etc.).
3. Click on the chemical, scroll down to the **Spectra** section, and click "View Spectrum".
4. Find the "Generated list of m/z values for the spectrum (TXT)" and click "Download file".
5. Copy and paste the values into a `.txt` file in the root directory of this project.
6. Run `python converter.py`, and the script will convert the `.txt` file(s) into `.wav` file(s) with the same name.
7. You may need to adjust the `INTENSITY_THRESHOLD` in order to get clean sounding audio.
