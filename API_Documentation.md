# Mass Spectrum to Audio Converter API Documentation

## Overview

The Mass Spectrum to Audio Converter API converts mass spectrometry data into audio files using configurable algorithms and parameters. The API retrieves compound spectra from a dedicated Render database (migrated from MassBank database from [Release 2025.05.1](https://github.com/MassBank/MassBank-data/releases/tag/2025.05.1)) and generates audio data along with detailed spectrum transformation information.

## Base URL

```
https://mass-spectrum-to-audio-converter.onrender.com
```

---

## Endpoints

### 1. Generate Audio and Spectrum Data from Compound

**Endpoint:** `POST /massbank/<algorithm>`

Generates audio data from a compound's mass spectrum data using the specified algorithm and returns both the audio file as base64 and detailed spectrum transformation data.

#### Path Parameters

| Parameter   | Type   | Required | Description                                                                     |
| ----------- | ------ | -------- | ------------------------------------------------------------------------------- |
| `algorithm` | string | Yes      | Algorithm for audio generation. Must be either `linear`, `inverse`, or `modulo` |

#### Request Body

**Content-Type:** `application/json`

| Parameter     | Type    | Required | Default | Validation  | Description                                                        |
| ------------- | ------- | -------- | ------- | ----------- | ------------------------------------------------------------------ |
| `compound`    | string  | Yes      | -       | -           | Name or identifier of the compound to search for                   |
| `offset`      | float   | No       | 300     | -           | `Hz = m/z + offset` _(linear algorithm only)_                      |
| `scale`       | float   | No       | 100000  | -           | `Hz = scale / (m/z + shift)` _(inverse algorithm only)_            |
| `shift`       | float   | No       | 1       | -           | `Hz = scale / (m/z + shift)` _(inverse algorithm only)_            |
| `factor`      | float   | No       | 10      | -           | `Hz = ((m/z * factor) % modulus) + base` _(modulo algorithm only)_ |
| `modulus`     | float   | No       | 500     | -           | `Hz = ((m/z * factor) % modulus) + base` _(modulo algorithm only)_ |
| `base`        | float   | No       | 100     | -           | `Hz = ((m/z * factor) % modulus) + base` _(modulo algorithm only)_ |
| `sample_rate` | integer | No       | 96000   | 3500-192000 | Audio sample rate in Hz                                            |
| `duration`    | float   | No       | 5.0     | 0.01-30.0   | Duration of generated audio in seconds                             |

**Note:** "Required" means the parameter must be provided in the request. Optional parameters will use their default values if not specified.

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
  ]
}
```

**Response Fields:**

| Field                         | Type    | Description                                  |
| ----------------------------- | ------- | -------------------------------------------- |
| `compound`                    | string  | Actual compound name found in database       |
| `accession`                   | string  | MassBank accession number                    |
| `audio_base64`                | string  | Base64-encoded WAV audio file                |
| `spectrum`                    | array   | Array of spectrum transformation data points |
| `spectrum[].mz`               | float   | Original m/z value from mass spectrum        |
| `spectrum[].frequency`        | float   | Converted frequency in Hz                    |
| `spectrum[].intensity`        | integer | Original intensity value from database       |
| `spectrum[].amplitude_linear` | float   | Normalized amplitude (0-1 range)             |
| `spectrum[].amplitude_db`     | float   | Amplitude in decibels                        |
| `algorithm`                   | string  | Algorithm used for conversion                |
| `parameters`                  | object  | Algorithm-specific parameters used           |
| `parameters.offset`           | float   | Offset value (linear algorithm only)         |
| `parameters.scale`            | float   | Scale value (inverse algorithm only)         |
| `parameters.shift`            | float   | Shift value (inverse algorithm only)         |
| `parameters.factor`           | float   | Factor value (modulo algorithm only)         |
| `parameters.modulus`          | float   | Modulus value (modulo algorithm only)        |
| `parameters.base`             | float   | Base value (modulo algorithm only)           |
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

```
POST https://mass-spectrum-to-audio-converter.onrender.com/massbank/linear
```

```json
{
  "compound": "caffeine"
}
```

**Linear Algorithm with Custom Parameters**

```
POST https://mass-spectrum-to-audio-converter.onrender.com/massbank/linear
```

```json
{
  "compound": "aspirin",
  "offset": 250,
  "duration": 10,
  "sample_rate": 48000
}
```

**Inverse Algorithm with Custom Parameters**

```
POST https://mass-spectrum-to-audio-converter.onrender.com/massbank/inverse
```

```json
{
  "compound": "folate",
  "scale": 50000,
  "shift": 2,
  "duration": 3
}
```

**Modulo Algorithm with Custom Parameters**

```
POST https://mass-spectrum-to-audio-converter.onrender.com/massbank/modulo
```

```json
{
  "compound": "glucose",
  "factor": 15,
  "modulus": 600,
  "base": 150,
  "duration": 7,
  "sample_rate": 44100
}
```

---

### 2. Get Recently Generated Compounds

**Endpoint:** `GET /history`

Retrieves recently generated compounds.

#### Query Parameters

| Parameter | Type    | Required | Default | Description                                            |
| --------- | ------- | -------- | ------- | ------------------------------------------------------ |
| `limit`   | integer | No       | 20      | Maximum number of recently generated entries to return |

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

**Get Last 20 Generations**

```
GET https://mass-spectrum-to-audio-converter.onrender.com/history
```

**Get Last 50 Generations**

```
GET https://mass-spectrum-to-audio-converter.onrender.com/history?limit=50
```

### 3. Get Most Generated Compounds

**Endpoint:** `GET /popular`

Retrieves the most frequently generated compounds based on recent generations.

#### Query Parameters

| Parameter | Type    | Required | Default | Description                                        |
| --------- | ------- | -------- | ------- | -------------------------------------------------- |
| `limit`   | integer | No       | 20      | Maximum number of most generated entries to return |

#### Response

**Success Response (200 OK)**

```json
{
  "popular": [
    {
      "compound": "Caffeine",
      "search_count": 147
    },
    {
      "compound": "Mellein",
      "search_count": 33
    },
    {
      "compound": "Methyltestosterone",
      "search_count": 31
    },
    {
      "compound": "BIOTIN",
      "search_count": 26
    },
    {
      "compound": "Choline",
      "search_count": 25
    }
  ]
}
```

#### Example Requests

**Get Top 20 Most Generated Compounds**

```
GET https://mass-spectrum-to-audio-converter.onrender.com/popular
```

**Get Top 10 Most Generated Compounds**

```
GET https://mass-spectrum-to-audio-converter.onrender.com/popular?limit=10
```
