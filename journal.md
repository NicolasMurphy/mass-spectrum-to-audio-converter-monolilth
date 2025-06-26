### Develop a Web-Based Version of the Converter

Instead of manually grabbing a text file from HMDB, it would be more seamless to scrape this data. This concept would be even more approachable if the code was implemented as a simple web app.

**Concept:**

- User opens webpage.
- A search bar and button are displayed.
- The user enters the name of a metabolite and clicks **“Generate WAV.”**
- The script searches HMDB, navigates to the Spectra section, and downloads the first applicable `.txt` file (May be some complications here as some metabolites don't contain `.txt` files, or the `.txt` files contain extra text - filtering out the text is a possibility. Most likely will have to iterate through the results until a matching result is found).
- The Python script processes the file, converts the values into audio, and returns a `.wav` file.
- The `.wav` file is downloaded via the browser.

**Future Ideas / Enhancements:**

- HMDB is fairly slow, there may be a better option for a database. Other databases may have other advantages/disadvantages. `.txt` fetching script could maybe use multiple databases to find the most suitable `.txt` file quickly.
- Right now the python script has a few constants, ideally this would be configurable on the webpage as well:
  - Sample rate: `96000 Hz`
  - Duration: `5 seconds`
  - Intensity threshold: `0.1`
  - m/z transformation: `value * 5 + 200`
- Audio preview would be ideal before downloading the file.

**Technical Specifications**

Originally considered bridging the existing Python implementation with a React frontend by exposing the Python script as an API endpoint.
The plan was to use Flask for the backend (hosted on Render, Heroku, or Railway) and deploy the React frontend to Vercel.

However, since the frontend is minimal (just a search bar and button, possibly some sliders), using Flask for both the backend and frontend seems like the better option.
This allows everything to be handled within a single Python-based app, reducing deployment complexity and avoiding the need for CORS or multi-environment setup.

I've used Django before, but Flask is more lightweight and minimal, making it a better fit.

The full Flask app will likely be hosted on Render, with GitHub integration for auto-deploys.
