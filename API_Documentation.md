# Mass Spectrum to Audio Converter API Documentation

## Overview

The Mass Spectrum to Audio Converter API converts mass spectrometry data into audio files using configurable algorithms and parameters. The API currently retrieves compound spectra from the MassBank database and generates WAV audio files based on the spectral data.

## Base URL

```
https://mass-spectrum-to-audio-converter.onrender.com
```

## Authentication

No authentication required.

## Rate Limiting

- **Rate Limit:** 10 requests per 60-second window per client IP address
- **Sliding Window:** The 60-second window slides with each request
- **Exceeded Limit:** Returns HTTP 429 with `{"error": "Rate limit exceeded. Try again later."}`

---

## Data Source

This API integrates with the MassBank database through their REST API:

- **MassBank API Documentation**: https://massbank.eu/MassBank-api/ui/
- **Search Endpoint**: `/records/search` - Used to find compounds by name
- **Record Endpoint**: `/records/{accession}` - Used to retrieve detailed spectrum data
- **Selection Logic**: The first matching record from search results is automatically selected

---

## Endpoints

### 1. Generate Audio from Compound Spectrum

**Endpoint:** `GET /massbank/<algorithm>`

Generates an audio file from a compound's mass spectrum data using the specified algorithm.

#### Path Parameters

| Parameter   | Type   | Required | Description                                                          |
| ----------- | ------ | -------- | -------------------------------------------------------------------- |
| `algorithm` | string | Yes      | Algorithm for audio generation. Must be either `linear` or `inverse` |

#### Query Parameters

| Parameter     | Type    | Required | Default | Validation  | Description                                                                                          |
| ------------- | ------- | -------- | ------- | ----------- | ---------------------------------------------------------------------------------------------------- |
| `compound`    | string  | Yes      | -       | -           | Name or identifier of the compound to search for                                                     |
| `offset`      | float   | No       | 300     | -           | Offset added to m/z values during conversion to Hz _(linear algorithm only - ignored by inverse)_    |
| `scale`       | float   | No       | 100000  | -           | Scaling factor for frequency calculation _(inverse algorithm only - ignored by linear)_              |
| `shift`       | float   | No       | 1       | -           | Shift value applied to m/z before inverse calculation _(inverse algorithm only - ignored by linear)_ |
| `sample_rate` | integer | No       | 96000   | 3500-192000 | Audio sample rate in Hz                                                                              |
| `duration`    | float   | No       | 5.0     | 0.01-30.0   | Duration of generated audio in seconds                                                               |

#### Response

**Success Response (200 OK)**

- **Content-Type:** `audio/wav`
- **Body:** WAV audio file as binary data
- **Headers:**
  - `X-Compound`: Actual compound name found in MassBank
  - `X-Accession`: MassBank accession number
- **Filename:** `{compound_name}-{accession}.wav` (e.g., `Caffeine-MSBNK-ACES_SU-AS000088.wav`)

**Error Responses**

| Status Code | Description                | Example Response                                                     |
| ----------- | -------------------------- | -------------------------------------------------------------------- |
| 400         | Invalid algorithm          | `{"error": "Unsupported algorithm 'fourier'"}`                       |
| 400         | Missing compound           | `{"error": "No compound provided"}`                                  |
| 400         | Invalid duration           | `{"error": "Duration must be between 0.01 and 30 seconds."}`         |
| 400         | Invalid sample rate        | `{"error": "Sample rate must be between 3500 and 192000"}`           |
| 400         | Invalid sample rate format | `{"error": "Invalid sample rate. Must be an integer."}`              |
| 429         | Rate limit exceeded        | `{"error": "Rate limit exceeded. Try again later."}`                 |
| 500         | Internal server error      | `{"error": "No records found"}`                                      |

#### Example Requests

**Basic Request (Linear Algorithm)**

```
GET https://mass-spectrum-to-audio-converter.onrender.com/massbank/linear?compound=caffeine
```

**Linear Algorithm with Custom Offset**

```
GET https://mass-spectrum-to-audio-converter.onrender.com/massbank/linear?compound=aspirin&offset=250&duration=10&sample_rate=48000
```

**Inverse Algorithm with Custom Scale and Shift**

```
GET https://mass-spectrum-to-audio-converter.onrender.com/massbank/inverse?compound=folate&scale=50000&shift=2&duration=3
```

---

### 2. Get Search History

**Endpoint:** `GET /history`

Retrieves the search history of compounds that have been processed.

#### Query Parameters

| Parameter | Type    | Required | Default | Description                                 |
| --------- | ------- | -------- | ------- | ------------------------------------------- |
| `limit`   | integer | No       | 10      | Maximum number of history entries to return |

#### Response

**Success Response (200 OK)**

```json
{
  "history": [
    {
      "accession": "MSBNK-Antwerp_Univ-METOX_P100302_F638",
      "compound": "Folate",
      "created_at": "2025-07-09T03:45:51.639366+00:00"
    },
    {
      "accession": "MSBNK-ACES_SU-AS000088",
      "compound": "Caffeine",
      "created_at": "2025-07-09T03:45:44.172214+00:00"
    },
    {
      "accession": "MSBNK-ACES_SU-AS000078",
      "compound": "Aspirin",
      "created_at": "2025-07-09T03:45:33.844220+00:00"
    }
  ]
}
```

#### Example Requests

**Get Last 10 Searches**

```
GET https://mass-spectrum-to-audio-converter.onrender.com/history
```

**Get Last 50 Searches**

```
GET https://mass-spectrum-to-audio-converter.onrender.com/history?limit=50
```

---

## Algorithm Types

### Linear Algorithm

- **Frequency Calculation:** `frequency = m/z + offset`
- Converts m/z values to Hz by adding a constant offset
- **Parameters:** `offset` (default: 300)

### Inverse Algorithm

- **Frequency Calculation:** `frequency = scale / (m/z + shift)`
- Converts m/z values to Hz using inverse relationship where higher m/z values produce lower frequencies
- **Parameters:** `scale` (default: 100000), `shift` (default: 1)

---

## Audio Generation Process

1. **Compound Lookup**: The API searches MassBank for the specified compound using the `/records/search` endpoint
2. **Record Selection**: Automatically selects the first matching record from the search results
3. **Spectrum Retrieval**: Mass spectrum data (m/z and intensity values) is retrieved using the `/records/{accession}` endpoint, where m/z represents mass-to-charge ratio
4. **Frequency Conversion**: m/z values are converted to audio frequencies (Hz) using the selected algorithm
5. **Intensity Processing**: Intensity values are used as amplitudes for sine wave generation, then normalized to prevent clipping
6. **Audio Synthesis**: Individual sine waves are generated for each m/z peak and then summed together to create the final audio waveform
7. **WAV Export**: The summed waveform is encoded as 16-bit PCM WAV format with specified sample rate and duration

---

## Response Headers

Successful audio generation responses include additional metadata:

- `X-Compound`: The actual compound name found in MassBank (may differ from search query)
- `X-Accession`: MassBank accession number for the spectrum used
- `Content-Type`: `audio/wav`
- `Content-Disposition`: `attachment; filename="{compound}-{accession}.wav"`
