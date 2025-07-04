## Mass Spectrum to Audio Converter

This tool converts mass spectrometry data into audio by mapping spectral peaks to sine wave frequencies.

---

### Try It Live

[mass-spectrum-to-audio-converter.vercel.app](https://mass-spectrum-to-audio-converter.vercel.app)

---

### About the Project

This project fetches spectral data from the [MassBank](https://massbank.eu/) database, extracts m/z (mass-to-charge) values and intensities, and converts them into sine waves. You can control parameters like offset, duration, and sample rate to shape the resulting audio.

- **Backend**: Python, Flask, MassBank API, deployed via Render
- **Frontend**: React, Tailwind (via DaisyUI), Vite, deployed via Vercel
- **Local API Endpoint Example**:
  `GET /massbank/linear?compound=biotin&sample_rate=96000&offset=300&duration=5.0`

Learn more about the motivation and creative inspiration in [my blog post](https://www.nicolasmurphy.com/blog/mass-spectrometry-music)

---

### Run Locally

To run this project on your machine:

1. **Clone the repository**
   `git clone https://github.com/your-username/mass-spectrum-to-audio-converter.git`
   `cd mass-spectrum-to-audio-converter`

2. **Start the backend**

- Navigate to the backend folder:
  `cd backend`
- Install dependencies:
  `pip install -r requirements.txt`
- Run the Flask app:
  `python app.py`
- Visit the dev testing sandbox at: http://localhost:5000

3. **Start the frontend**

- Open a new terminal tab or window
- Navigate to the frontend folder:
  `cd frontend`
- Install dependencies:
  `npm i`
- Start the dev server:
  `npm run dev`
- View the frontend at: http://localhost:5173

---

### Future Plans

- Add support for multiple frequency mapping algorithms

- Add keyboard/sampler-style playback interface

- Support additional spectral databases
