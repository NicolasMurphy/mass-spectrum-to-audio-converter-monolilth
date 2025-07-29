### [2025-07-28] Info Modal, modulo algorithm implementation and utilize Render database instead of Massbank API

- **Goals:**

  - Add Info Modal explaining the app
  - Add modulo algorithm in backend
  - Implement modulo in form in frontend
  - Utilize Render database instead of Massbank API

- **Notes:**

  - Implemented DaisyUI modal explaining the app and technical info
  - Experimented with different algorithms, decided on modulo algorithm
  - Implemented modulo algorithm in backend and frontend
  - **Database Migration Process:**
    - Motivated by SSL certificate expiration issues, eliminating external API dependency, and desire for better performance
    - Extracted necessary tables from 520MB Massbank.sql file using MariaDB locally
    - Exported spectrum data from MariaDB to CSV using mysqldump command with four-table join query: `"SELECT p.RECORD as accession, n.CH_NAME as compound_name, p.PK_PEAK_MZ as mz, p.PK_PEAK_INTENSITY as intensity FROM PEAK p JOIN RECORD r ON p.RECORD = r.ACCESSION JOIN COMPOUND_NAME cn ON r.CH = cn.COMPOUND JOIN NAME n ON cn.NAME = n.ID" > massbank_spectrum_data.csv`
    - Used PowerShell to clean encoding issues (removed non-ASCII characters from 7 compounds): `Get-Content massbank_spectrum_data.csv -Encoding UTF8 | Where-Object { $_ -match '^[a-zA-Z0-9\t\-\.\s_()\/\[\]:;,+]*$' } | Out-File -Encoding UTF8 massbank_spectrum_data_clean.csv`
    - Imported 6.3M peak records to Render PostgreSQL database with proper data types (DECIMAL precision increased for large intensity values)
    - Created optimized table structure: `spectrum_data(accession, compound_name, mz, intensity)` and `compound_accessions(compound_name, accession)` lookup table
  - **Performance Optimization:**
    - Implemented two-step search pattern matching previous MassBank API usage: fast compound lookup then accession-based peak retrieval
    - Created strategic indexes: `idx_compound_accessions_name_lower`, `idx_accession`, `idx_compound_name_exact`
    - Eliminated expensive LIKE queries on large tables by using dedicated compound lookup table
  - **Results:** Successfully migrated 6.3M peak records from MassBank's normalized schema, achieving 3x faster performance (1.5s → 470ms average) and eliminated external API dependency, SSL certificate issues, and network latency

- **Next Steps:**

  - Remove MassBank related code
  - Clean up unnecessary tables and indexes in Render database
  - Update README - document Render database architecture instead of MassBank API integration
  - Update tests - mock database calls instead of HTTP requests, add tests for modulo algorithm
  - Update API Documentation - remove MassBank API references, add modulo algorithm parameters and Render database details
  - Update error handling for new Render database instead of Massbank API
  - Sort table columns by clicking on table headers
  - Spectrum tables can be quite large, perhaps a conditional scroll bar?
  - Simplify SamplePiano width/responsive logic
  - SamplePiano keyboard interaction should not occur when user is typing in the compound search field
  - Organize Typescript types
  - Unit Tests
  - Integration Tests
  - E2E Tests

### [2025-07-27] UI Improvements, Component Organization and "Most Generated" list

- **Goals:**

  - Improve frontend styling with card-based layout
  - Implement skeleton loading states for better UX
  - Reorganize component folder structure for maintainability
  - Enhance Recently Generated functionality
  - Fix rate limiting memory leak and adjust limits
  - Add Most Generated list more retrieving most searched compounds

- **Notes:**

  - Added card layout for all three columns with proper spacing
  - Implemented skeleton animation for spectrum data tables using DaisyUI skeleton components
  - Reorganized Components folder structure
  - Styled Recently Generated section with clickable badges that auto-populate compound search
  - Fixed rate limiting memory leak and updated to 20 requests per 5 minutes
  - Fixed Git case sensitivity issue with Components folder for successful Vercel deployments
  - Added Most Generated list, following Recently Generated look and functionality

- **Next Steps:**

  - Spectrum tables can be quite large, perhaps a conditional scroll bar?
  - Add about/info help text (modal?)
  - Simplify SamplePiano width/responsive logic
  - SamplePiano keyboard interaction should not occur when user is typing in the compound search field
  - Organize Typescript types
  - Migrate all spectrum data over to Render database as to not rely on MassBank API
  - Unit Tests
  - Integration Tests
  - E2E Tests

### [2025-07-26] Explore Performance Improvements

- **Goals:**

  - Explore Performance Improvements

- **Notes:**

  - Discovered Render automatically provides Brotli compression (Content-Encoding: br) at the platform level

- **Next Steps:**

  - Continue exploring performance improvements (rate-limiting cleanup, MassBank API caching)
  - Improve styling (cards for spectrum table and recently generated)
  - Add about/info help text (modal?)
  - Integration Tests
  - E2E Tests

### [2025-07-25] Finish `App.tsx` refactoring, implement db connection pool & Auto run tests on push

- **Goals:**

  - Finish `App.tsx` refactoring
  - Implement connection pooling for db
  - Auto run tests on push (GitHub Actions)

- **Notes:**

  - Extract `AlgorithmSelector`, `LinearParameters`, `InverseParameters`, and `AudioSettings` components from `App.tsx`
  - Created `connection_pool.py` with `psycopg2.pool` (minconn=1, maxconn=5)
  - Updated `queries.py` to use `get_connection` instead of `get_db_connection`
  - Updated `test_queries.py` and `test_app.py` to work with new connection pooling (mocking before import)
  - Add GitHub Actions CI workflow for backend tests

- **Next Steps:**

  - Improve styling (cards for spectrum table and recently generated)
  - Add about/info help text (modal?)
  - Integration Tests
  - E2E Tests

### [2025-07-24] Fix dependency warning in `useSearchHistory`

- **Goals:**

  - Wrap fetchHistory in useCallback to fix dependency warning

- **Notes:**

  - Wrapped fetchHistory in useCallback, added correct dependencies as `[limit, loading]`

- **Next Steps:**

  - Continue `App.tsx` refactoring - Extract form sections into components (`AlgorithmSelector`, `LinearParameters`, etc.)
  - Autocomplete improvements: fuzzy matching, substring matching, stemming...
  - Database Connection Pooling
  - Auto run tests on Push (GitHub Actions)
  - Integration Tests
  - E2E Tests

### [2025-07-23] Prevent decimal input in sample rate field

- **Goals:**

  - Prevent decimal input in sample rate field

- **Notes:**

  - Used regex on the form input onChange for sample rate, to prevent float values, matching backend validation

- **Next Steps:**

  - Continue `App.tsx` refactoring - Extract form sections into components (`AlgorithmSelector`, `LinearParameters`, etc.)
  - Autocomplete improvements: fuzzy matching, substring matching, stemming...
  - Database Connection Pooling
  - Auto run tests on Push (GitHub Actions)
  - Integration Tests
  - E2E Tests

### [2025-07-22] Refactor `App.tsx`

- **Goals:**

  - Refactor `App.tsx` into smaller components
  - Clean up large `useEffect`

- **Notes:**

  - Decided not to use `Zustand` as there isn't too much state to manage, and prop drilling isn't really a concern
  - Refactor `RecentlyGenerated`, `CompoundSearch`, `AudioPlayer`, `NameAndAccession`, `base64ToBlob`, `SpectrumTables` to own files
  - Add keyboard navigation to `CompoundSearch`
  - Extract handleFetch function from `useEffect` with `useCallback`
  - Remove dependency from global enter key `useEffect`, use `useRef` for `handleFetch`

- **Next Steps:**

  - Continue `App.tsx` refactoring - Extract form sections into components (`AlgorithmSelector`, `LinearParameters`, etc.)
  - Autocomplete improvements: fuzzy matching, substring matching, stemming...
  - Database Connection Pooling
  - Auto run tests on Push (GitHub Actions)
  - Integration Tests
  - E2E Tests

### [2025-07-21] Implement auto-refetch for Recently Generated list

- **Goals:**

  - Implement auto-refetch for Recently Generated list

- **Notes:**

  - Created `useSearchHistory` custom hook.
  - Created `/hooks` folder.
  - Need to further refactor the react side of things, need `/utils` folder or file, perhaps use Zustand for state management, env variables for API link, .tsx can be separated into different files.
  - Use environment variables for API link in frontend
  - Use environment variable for CORS origins

- **Next Steps:**

  - General refactoring - App.tsx is getting unwieldy
  - Autocomplete improvements: fuzzy matching, substring matching, stemming...
  - Database Connection Pooling
  - Auto run tests on Push (GitHub Actions)
  - Integration Tests
  - E2E Tests

### [2025-07-20] Implement autocomplete

- **Goals:**

  - Implement autocomplete for compound name input

- **Notes:**

  - Extracted compound names from MassBank.sql file (226,829 compound names from lines 4027157-4253994), converted from MariaDB to PostgreSQL format
  - Fixed SQL escaping issues (`\'` → `''`)
  - Imported compound names into Render database (226,822 compounds after handling syntax/encoding errors)
  - Database returned 37,627 unique compound names (significant duplicates in original data)
  - Decided frontend caching approach was best for performance
  - Created static `compounds.json` (1,509 KB) file in `/public` (automatic browser caching)
  - Implemented React autocomplete with useEffect to load all compounds on initial load, useState for suggestions, dropdown display, and click/blur handling
  - Added `autoComplete="off"` to disable browser's built-in autocomplete
  - Search is now instant after initial load, with prefix matching starting at 1 character
  - Removed commented `/compounds/all` endpoint
  - Updated `/history` endpoint limit default to 20

- **Next Steps:**

  - Recently Generated should update on successful generation
  - Database Connection Pooling
  - Auto run tests on Push (GitHub Actions)
  - Integration Tests
  - E2E Tests

### [2025-07-19] Finished new POST endpoint, implemented spectrum table in frontend, rewrote API Documentation, removed unused code, began writing unit tests for new functionality

- **Goals:**

  - Finish new POST endpoint
  - Implement spectrum table in frontend
  - Rewrite API Documentation
  - Remove unused code
  - Begin writing unit tests for new functionality

- **Notes:**

  - Simplified `"spectrum": {"transformed": [...]}` to be `"spectrum": [...]` for JSON Response
  - Implemented spectrum table in dev testing sandbox and frontend
  - Rewrote API documentation for new POST endpoint
  - Removed `generate_combined_wav_bytes`, GET endpoint code, and tests relating to both of those functions
  - Began writing unit tests for new POST endpoint
  - Need to finish out unit tests for new POST endpoint and write unit tests for `generate_combined_wav_bytes_and_data` function

- **Next Steps:**

  - Finish out unit tests
  - Implement autocomplete

### [2025-07-18] Continue implementation of new `/massbank/<algorithm>` POST endpoint

- **Goals:**

  - Continue implementation of new `/massbank/<algorithm>` POST endpoint

- **Notes:**

  - Created new `generate_combined_wav_bytes_and_data` function that mimics `generate_combined_wav_bytes` but also returns transformed data.
  - Updated POST request to utilize the new `generate_combined_wav_bytes_and_data` function and include the spectrum data in the response.
  - Fixed JSON parameter parsing (string to float conversion) (Flask's request.args.get(type=float) vs manual JSON parsing)
  - Implemented the following in dev testing sandbox:
    - Request and response body
    - Transformed values in table
    - Conversion of base64 string to playable and downloadable audio
  - Considerations:
    - Include request URL in dev testing sandbox
    - Include converted decibel values in transformed/spectrum JSON
    - Update history table to include additional fields from new POST endpoint

- **Next Steps:**

  - Simplify `"spectrum": {"transformed": [...]}` to be `"spectrum": [...]` for JSON Response
  - Replace existing GET endpoint in frontend with POST endpoint
  - Display transformed values in frontend (for now just a table, but a visual graph later)
  - Implement autocomplete

### [2025-07-17] Pass audio as base64 string along with spectrum data

- **Goals:**

  - Make a new `generate_audio` function called `generate_audio_with_data` that passes the audio as a base64 string along with the spectrum data.

- **Notes:**

  - Passing the audio as a base64 string is more expensive (~33% larger), but seems like the best approach for simplicity. Considered two API calls, but would be messy, potential race conditions.
  - Creating a new function called `generate_audio_with_data` as a POST request, seems like best option - better semantic fit and allows for more complex requests.
  - Tested with Insomnia, and new endpoint works.
  - Still need to implement transformed spectrum array.

- **Next Steps:**

  - Continue with implementation of passing spectrum data in API call
  - Implement autocomplete

### [2025-07-16] Autocomplete strategy

- **Goals:**

  - Figure out the best strategy for implementing autocomplete

- **Notes:**

  - Found MassBank.sql file (520MB). Need to figure out how to import it so it is useable.
  - Create separate Render database?
  - Import to render using CLI with psql

- **Next Steps:**

  - Display all m/z values and Hz values after transformation in UI
  - Implement autocomplete utilizing compound names in history table (or better yet, get all compound names from massbank)

### [2025-07-15] DB Tests

- **Goals:**

  - Implement unit tests for functions in `queries.py`

- **Notes:**

  - Added unit tests for log_search() and get_search_history() with mocked database connections; achieved 93% test coverage
  - Need to research connection pooling

- **Next Steps:**

  - Display all m/z values and Hz values after transformation in UI
  - Implement autocomplete utilizing compound names in history table (or better yet, get all compound names from massbank)

### [2025-07-14] Backend Tests

- **Goals:**

  - Implement backend unit tests

- **Notes:**

  - Changing to `verify=cafile` to `verify=True` in `massbank.py` still results in error:

```
Error 500: HTTPSConnectionPool(host='massbank.eu', port=443): Max retries exceeded with url: /MassBank-api/records/search?compound_name=test (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1028)')))
```

- **Next Steps:**

  - Display all m/z values and Hz values after transformation in UI
  - Implement autocomplete utilizing compound names in history table

### [2025-07-13] Implement spinner

- **Goals:**

  - Spinner status when fetching/generating audio

### [2025-07-11] Implement global enter key functionality

- **Goals:**

  - Implement global enter key functionality

- **Notes:**

  - Moved handleFetch logic inside useEffect to avoid dependency issues and ESLint warnings
  - Users can now press Enter globally

- **Next Steps:**

  - Find more permanent solution for MassBank certificate handling
  - Display all m/z values and Hz values after transformation in UI
  - Experiment further with algorithm options
  - Integrate additional spectral databases beyond MassBank

### [2025-07-09] object URL cleanup

- **Goals:**

  - Fix memory leak from blob URLs in React audio player

- **Notes:**

  - Added useEffect cleanup and pre-fetch URL revocation to prevent WAV files from accumulating in browser memory during extended usage

- **Next Steps:**

  - Find more permanent solution for MassBank certificate handling
  - Display all m/z values and Hz values after transformation in UI
  - Experiment further with algorithm options
  - Integrate additional spectral databases beyond MassBank

### [2025-07-08] Fix API bug for `sample_rate`, create API Documentation

- **Goals:**

  - Fix API bug where `sample_rate` parameter was incorrectly required
  - Create comprehensive API documentation
  - Update README to include API documentation and algorithm information

- **Notes:**

  - Modified sample rate validation to allow optional parameter while preventing invalid values like "44100.1"
  - Created detailed API docs with real MassBank examples and parameter clarifications
  - Updated README with algorithm descriptions and completed features

- **Next Steps:**

  - Find more permanent solution for MassBank certificate handling
  - Display all m/z values and Hz values after transformation in UI
  - Experiment further with algorithm options
  - Integrate additional spectral databases beyond MassBank

### [2025-07-07] Implement `Recently Generated` in frontend

- **Goals:**

  - Implement `Recently Generated` in frontend

- **Notes:**

  - Ended up using a grid for structuring layout. Still not satisfied with the styling, but it is "good enough" for now.

- **Next Steps:**

  - Find more permanent solution for Massbank Cert
  - Displaying all m/z values, and hz values after transformation.
  - Experiment further with algorithm options
  - Integrate additional spectral databases beyond MassBank

### [2025-07-06] Fix Keyboard responsive design, fix negative number UX issue, implement database

- **Goals:**

  - Fix Keyboard responsive design
  - Fix UX issue with entering negative numbers
  - Create Postgres database on Render
  - Create `search_history` table in database
  - Log searches to database
  - Create query to get searches from database
  - Create /history API endpoint
  - Display recent searches in dev testing sandbox

- **Notes:**

  - Have been stuck on the keyboard not centering on mobile devices. Plan is to experiment further with Responsive design mode in Firefox. Also observed some unexpected layout issues in Firefox, even at standard laptop screen sizes.
  - Massbank cert expires Aug 15, will likely have to download a newer cert. Possible more sustainable solutions: Use Let’s Encrypt Root CA, or (back up plan) auto renew the cert (parse through a live TLS connection)
  - Keyboard plays when entering compound, not too concerning, but ideally should not be doing that. Not an immediate bug to address, but making note of it.
  - Consider help text for explaining what m/z is - end user may not understand what is happening
  - Consider using a different library for keyboard
  - Switched numeric inputs from Number state to string state for smoother typing (e.g. -, empty)
  - Used `ResizeObserver` to clamp and center piano width responsively
  - Settled on `id`, `accession`, `compound`, `timestamp` for `search_history` table
  - Updated `TIMESTAMP` to `TIMESTAMPZ` to reflect accurate timezone

- **Next Steps:**

  - Find more permanent solution for Massbank Cert
  - Displaying all m/z values, and hz values after transformation.
  - Experiment further with algorithm options
  - Integrate additional spectral databases beyond MassBank
  - Implement recently searched in frontend

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
