## Mass Spectrum to Audio Converter

This tool converts mass spectrometry data into audio by mapping spectral peaks to sine wave frequencies.

---

### Try It Live

[mass-spectrum-to-audio-converter.vercel.app](https://mass-spectrum-to-audio-converter.vercel.app)

---

### About the Project

This project fetches spectral data from the [MassBank](https://massbank.eu/) database, extracts m/z (mass-to-charge) values and intensities, and converts them into sine waves. The project supports two frequency mapping algorithms: linear mapping (m/z values directly to frequencies with an offset) and inverse mapping (higher m/z values produce lower frequencies). Features include a keyboard playback interface for real-time interaction and displays recently generated compounds from all users for easy access.

**Tech Stack:**

- **Backend**: Python, Flask, MassBank API, deployed via Render
- **Frontend**: React, Tailwind (via DaisyUI), deployed via Vercel
- **Database**: PostgreSQL, hosted on Render

For complete API documentation, see [API_Documentation.md](API_Documentation.md)

Learn more about the motivation and creative inspiration in [my blog post](https://www.nicolasmurphy.com/blog/mass-spectrometry-music)

---

### Run Locally

To run this project on your machine:

1. **Clone the repository**

```
git clone https://github.com/your-username/mass-spectrum-to-audio-converter.git
```

```
cd mass-spectrum-to-audio-converter
```

2. **Start the backend**

- Navigate to the backend folder:

```
cd backend
```

- Install dependencies:

```
pip install -r requirements.txt
```

- Run the Flask app:

```
python app.py
```

- Visit the dev testing sandbox at: http://localhost:5000

3. **Start the frontend**

- Open a new terminal tab or window
- Navigate to the frontend folder:

```
cd frontend
```

- Install dependencies:

```
npm i
```

- Start the dev server:

```
npm run dev
```

- View the frontend at: http://localhost:5173

---

### Future Plans

- Expand further with more frequency mapping algorithms
- Support additional spectral databases
