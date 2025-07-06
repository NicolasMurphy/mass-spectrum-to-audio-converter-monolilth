### [2025-07-06] Fix Keyboard responsive design, fix negative number UX issue, implement database

- **Goals:**

  - Fix Keyboard responsive design
  - Fix UX issue with entering negative numbers
  - Create `search_history` database

- **Notes:**

  - Have been stuck on the keyboard not centering on mobile devices. Plan is to experiment further with Responsive design mode in Firefox. Also observed some unexpected layout issues in Firefox, even at standard laptop screen sizes.
  - Massbank cert expires Aug 15, will likely have to download a newer cert. Possible more sustainable solutions: Use Let’s Encrypt Root CA, or (back up plan) auto renew the cert (parse through a live TLS connection)
  - Keyboard plays when entering compound, not too concerning, but ideally should not be doing that. Not an immediate bug to address, but making note of it.
  - Consider help text for explaining what m/z is - end user may not understand what is happening
  - Consider using a different library for keyboard
  - Switched numeric inputs from Number state to string state for smoother typing (e.g. -, empty)
  - Used `ResizeObserver` to clamp and center piano width responsively

- **Next Steps:**

  - Displaying all m/z values, and hz values after transformation.
  - Experiment further with algorithm options
  - Integrate additional spectral databases beyond MassBank
  - Develop a searchable database of recently generated samples

### [2025-07-05] Implement `inverse` algorithm

- **Goals:**

  - Implement `inverse` algorithm in backend
  - Implement rate limiting by IP
  - Implement `inverse` algorithm in frontend
  - Display fields dynamically based on algorithm selected

- **Notes:**

  - Commented out all code related to the `logarithmic` algorithm — not as applicable as initially expected; may revisit later
  - Keyboard is still not centered on all mobile devices. Difficult to troubleshoot since Chrome's Toggle Device Toolbar is not rendering accurately; need a better strategy for debugging mobile layout
  - Discovered that Vercel's `Ignored Build Step` logic only checks the latest commit in a push for changes. This becomes an issue with multi-commit pushes where the final commit doesn’t touch the watched folder - the build is skipped even if earlier commits did. Not ideal. Could explore workarounds, but for now, it's just important to be aware of the behavior. Avoid multi-commit pushes, or ensure the last commit touches the target folder.

- **Next Steps:**

  - Fix Keyboard responsive design
  - Experiment further with algorithm options
  - Integrate additional spectral databases beyond MassBank
  - Develop a searchable database of recently generated samples

### [2025-07-04] Implement Keyboard

- **Goals:**

  - Update `README.md`
  - Add a basic playable keyboard to the frontend using `react-piano` and `Tone.js`
  - Implement `mz_to_frequency_logarithmic` in backend

- **Notes:**

  - Kept the scope minimal: the goal is to give users a quick "feel" for the generated audio before downloading and using it in their own sampler setup
  - Applied a short fade-in and fade-out to prevent audio clicks
  - Reduced playback volume to avoid clipping/distortion from polyphony
  - Scaled the keyboard to ensure responsive design on mobile
  - Consider bit depth selector `scipy.io.wavfile.write()` only supports 8, 16, or 32
  - logarithmic algorithm hard to control, unsure how much more time I want to spend on it, difficult to get musical results out of

- **Next Steps:**

  - Add support for multiple frequency mapping algorithms (e.g., logarithmic, inverse)
  - Integrate additional spectral databases beyond MassBank
  - Develop a searchable database of recently generated samples

### [2025-07-03] Implement offset & duration

- **Goals:**

  - Add `offset` parameter to backend
  - Implement offset input in frontend
  - Switch to path-based routing for algorithm: `/<database>/<algorithm>`
  - Ensure responsive design for frontend
  - Skip m/z values that result in frequencies ≤ 0
  - Add `duration` parameter to backend
  - Implement duration input in frontend

- **Notes:**

  - For the `offset` in def `mz_to_frequency` - need to change this to be offset by a single value for simplicity (+2000-3000 seems reasonable). Ended up settling on +300 for default.
  - Need to consider negative offsets causing frequencies below 0hz - seems like this will cause the sine wave to flip in phase. Consider adding a `if freq <= 0: continue `in def `generate_sine_wave`
  - Create `/linear/` path for the API, rename `mz_to_frequency` to `mz_to_frequency_linear`
  - Considered a query param for algorithm, but used a path instead since the algorithm defines the resource
  - Renamed html debugger to dev testing sandbox, not a full debugger, since it doesn't reflect internal state or allow inspection of transformed data
  - Decided to skip threshold implementation for now

- **Next Steps:**

  - consider displaying warning to user if frequencies below 0hz are detected?

### [2025-07-02] Sample Rate Support & Endpoint Refactor

- **Goals:**

  - Refactor `/generate` to `/massbank` for a more RESTful API
  - Add `sample_rate` parameter to backend
  - Update React frontend to support sample rate input
  - Improve Flask HTML debugger

- **Notes:**

  - Added a query URL in the debugger
  - Observed that deploying frontend and backend can cause temporary breakage

- **Next Steps:**

  - Add support for `duration`, `threshold`, `frequency equation`

### [2025-07-01] Create and Deploy React Frontend

- **Goals:**

  - Create frontend with React with same functionality
  - Style with Tailwind and DaisyUI
  - Deploy with Vercel

- **Notes:**

  - Added CORS origins/headers in backend to avoid CORS errors
  - Separate deployments by folder (frontend/ to Vercel, backend/ to Render)

- **Next Steps:**

  - Add sliders or controls for adjusting sample rate, duration, threshold, frequency equation.
  - Search by accession
  - Fallback support?
  - Autocomplete
  - Consider multiple alogrithms: linear, logarithmic, inverse, etc.
  - multiple database support?

### [2025-06-30] Frontend Enhancements & Deployment

- **Goals:**

  - Deploy working version via Render
  - Make accession a clickable link to MassBank record
  - User should be able to click enter to generate audio

- **Notes:**

  - Ended up needing to manually grab the SSL cert from MassBank, put the cert in /certs

- **Next Steps:**

  - Add sliders or controls for adjusting sample rate, duration, threshold, frequency equation.
  - Search by accession
  - Fallback support?
  - Autocomplete
  - Need to consider if it's better to switch to React Frontend now or later
  - Consider multiple alogrithms: linear, logarithmic, inverse, etc.

### [2025-06-29] MassBank Integration, Flask API, and Frontend Preview

- **Goals:**

  - Fetch mass spectrum data via the MassBank API
  - Connect spectrum data to audio converter pipeline
  - Begin replacing legacy `.txt`-based workflow with automated CLI tool
  - Build minimal Flask API for serving audio previews
  - Implement basic HTML frontend for testing and preview
  - Display compound name in frontend; ensure download includes compound and accession

- **Notes:**

  - `get_massbank_peaks.py` was renamed to `massbank.py` for clarity
  - New CLI tool `generate_from_massbank.py` was created to fetch data and generate `.wav` files in one step
  - Verified the script returns `(m/z, intensity)` tuples, compatible with the existing audio converter
  - Basic Flask API endpoint `/generate?compound=NAME` is now functional — returns a `.wav` file using a `BytesIO` stream
  - Removed unused files: `generate_from_massbank.py` and `fetch_hmdb.py`
  - Removed unused dependency: `beautifulsoup4`

- **Next Steps:**

  - Deploy on Render for live access and testing
  - Make accession in frontend a hyperlink to the corresponding MassBank record
  - Add sliders or controls for adjusting sample rate, duration, threshold, frequency equation.
  - Add fallback support for compounds not found in MassBank (e.g., MoNA or PubChem)
  - Implement autocomplete (potential for misleading the user to believe a compound is available)
  - (Further down the line)
    - Use React for frontend - implement keyboard
    - Implement database - display "recently searched/downloaded compounds"

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
