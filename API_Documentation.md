# Mass Spectrum to Audio Converter API Documentation

## Overview

The Mass Spectrum to Audio Converter API converts mass spectrometry data into audio files using configurable algorithms and parameters. The API retrieves compound spectra from the MassBank database and generates audio data along with detailed spectrum transformation information.

## Base URL

```
https://mass-spectrum-to-audio-converter.onrender.com
```

## Data Source

This API integrates with the MassBank database through their REST API:

- **MassBank API Documentation**: https://massbank.eu/MassBank-api/ui/
- **Search Endpoint**: `/records/search` - Used to find compounds by name
- **Record Endpoint**: `/records/{accession}` - Used to retrieve detailed spectrum data
- **Selection Logic**: The first matching record from search results is automatically selected

---

## Endpoints

### 1. Generate Audio and Spectrum Data from Compound

**Endpoint:** `POST /massbank/<algorithm>`

Generates audio data from a compound's mass spectrum data using the specified algorithm and returns both the audio file as base64 and detailed spectrum transformation data.

#### Path Parameters

| Parameter   | Type   | Required | Description                                                          |
| ----------- | ------ | -------- | -------------------------------------------------------------------- |
| `algorithm` | string | Yes      | Algorithm for audio generation. Must be either `linear` or `inverse` |

#### Request Body

**Content-Type:** `application/json`

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

**Content-Type:** `application/json`

```json
{
  "accession": "MSBNK-ACES_SU-AS000088",
  "algorithm": "linear",
  "audio_base64": "UklGRiSmDgBXQVZFZm10IBAAAAABAAEA...",
  "audio_settings": {
    "duration": 5.0,
    "sample_rate": 96000
  },
  "compound": "Caffeine",
  "parameters": {
    "offset": 300.0
  },
  "spectrum": [
    {
      "amplitude_db": -39.67184178472352,
      "amplitude_linear": 0.010385033713897209,
      "frequency": 356.0498390197754,
      "intensity": 5501836,
      "mz": 56.04983901977539
    },
    {
      "amplitude_db": -27.48478053530794,
      "amplitude_linear": 0.042243605014416714,
      "frequency": 369.04469299316406,
      "intensity": 22380032,
      "mz": 69.04469299316406
    },
    {
      "amplitude_db": -25.765718624084222,
      "amplitude_linear": 0.051488953951078366,
      "frequency": 383.06038665771484,
      "intensity": 27278080,
      "mz": 83.06038665771484
    }
    // Additional spectrum data...
  ]
}
```

**Response Fields:**

| Field                         | Type    | Description                                  |
| ----------------------------- | ------- | -------------------------------------------- |
| `compound`                    | string  | Actual compound name found in MassBank       |
| `accession`                   | string  | MassBank accession number                    |
| `audio_base64`                | string  | Base64-encoded WAV audio file                |
| `spectrum`                    | array   | Array of spectrum transformation data points |
| `spectrum[].mz`               | float   | Original m/z value from mass spectrum        |
| `spectrum[].frequency`        | float   | Converted frequency in Hz                    |
| `spectrum[].intensity`        | integer | Original intensity value from MassBank       |
| `spectrum[].amplitude_linear` | float   | Normalized amplitude (0-1 range)             |
| `spectrum[].amplitude_db`     | float   | Amplitude in decibels                        |
| `algorithm`                   | string  | Algorithm used for conversion                |
| `parameters`                  | object  | Algorithm-specific parameters used           |
| `parameters.offset`           | float   | Offset value (linear algorithm only)         |
| `parameters.scale`            | float   | Scale value (inverse algorithm only)         |
| `parameters.shift`            | float   | Shift value (inverse algorithm only)         |
| `audio_settings`              | object  | Audio generation settings                    |
| `audio_settings.duration`     | float   | Duration of generated audio in seconds       |
| `audio_settings.sample_rate`  | integer | Audio sample rate in Hz                      |

**Error Responses**

| Status Code | Description                | Example Response                                             |
| ----------- | -------------------------- | ------------------------------------------------------------ |
| 400         | Invalid algorithm          | `{"error": "Unsupported algorithm 'fourier'"}`               |
| 400         | Missing compound           | `{"error": "No compound provided"}`                          |
| 400         | Invalid duration           | `{"error": "Duration must be between 0.01 and 30 seconds."}` |
| 400         | Invalid sample rate        | `{"error": "Sample rate must be between 3500 and 192000"}`   |
| 400         | Invalid sample rate format | `{"error": "Invalid sample rate. Must be an integer."}`      |
| 400         | Invalid JSON               | `{"error": "No JSON data provided"}`                         |
| 429         | Rate limit exceeded        | `{"error": "Rate limit exceeded. Try again later."}`         |
| 500         | Internal server error      | `{"error": "No records found"}`                              |

#### Example Requests

**Basic Request (Linear Algorithm)**

```bash
curl -X POST https://mass-spectrum-to-audio-converter.onrender.com/massbank/linear \
  -H "Content-Type: application/json" \
  -d '{
    "compound": "caffeine"
  }'
```

**Linear Algorithm with Custom Parameters**

```bash
curl -X POST https://mass-spectrum-to-audio-converter.onrender.com/massbank/linear \
  -H "Content-Type: application/json" \
  -d '{
    "compound": "aspirin",
    "offset": 250,
    "duration": 10,
    "sample_rate": 48000
  }'
```

**Inverse Algorithm with Custom Parameters**

```bash
curl -X POST https://mass-spectrum-to-audio-converter.onrender.com/massbank/inverse \
  -H "Content-Type: application/json" \
  -d '{
    "compound": "folate",
    "scale": 50000,
    "shift": 2,
    "duration": 3
  }'
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

```bash
curl https://mass-spectrum-to-audio-converter.onrender.com/history
```

**Get Last 50 Searches**

```bash
curl https://mass-spectrum-to-audio-converter.onrender.com/history?limit=50
```
