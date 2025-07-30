## Mass Spectrum to Audio Converter

This tool converts mass spectrometry data into audio by mapping spectral peaks to sine wave frequencies.

---

### Try It Live

[mass-spectrum-to-audio-converter.vercel.app](https://mass-spectrum-to-audio-converter.vercel.app)

---

### About the Project

This project uses migrated data from MassBank hosted on Render, uses spectrometry data (m/z (mass-to-charge) values and intensities), and converts them into sine waves. The project supports three frequency mapping algorithms: linear, inverse, and modulo - with adjustable parameters. Features include a piano keyboard playback interface, displays recently generated as well as most generated compounds from all users, and provides detailed transformation tables showing mass spectrum data and audio transformation data to visualize exactly how the data is being transformed.

**Tech Stack:**

- **Backend**: Python, Flask, deployed via Render
- **Frontend**: React, TypeScript, Tailwind (via DaisyUI), deployed via Vercel
- **Database**: PostgreSQL hosted on Render (using MassBank data from [Release 2025.05.1](https://github.com/MassBank/MassBank-data/releases/tag/2025.05.1))

For complete API documentation, see [API_Documentation.md](API_Documentation.md)

Learn more about the motivation and creative inspiration in [my blog post](https://www.nicolasmurphy.com/blog/mass-spectrometry-music)
