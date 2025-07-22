import { useEffect, useState } from "react";
import "./App.css";
import SamplePiano from "./SamplePiano";
import { useSearchHistory } from "./hooks/useSearchHistory";

function base64ToBlob(base64String: string, contentType = "audio/wav"): Blob {
  const byteCharacters = atob(base64String);
  const byteNumbers = new Array(byteCharacters.length);

  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }

  const byteArray = new Uint8Array(byteNumbers);
  return new Blob([byteArray], { type: contentType });
}

function App() {
  const [compound, setCompound] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [audioUrl, setAudioUrl] = useState<string>("");
  const [compoundName, setCompoundName] = useState<string>("");
  const [accession, setAccession] = useState<string>("");
  const [algorithm, setAlgorithm] = useState<"linear" | "inverse">("linear");
  const [offset, setOffset] = useState<string>("300");
  const [scale, setScale] = useState<string>("100000");
  const [shift, setShift] = useState<string>("1");
  const [duration, setDuration] = useState<string>("5");
  const [sampleRate, setSampleRate] = useState<string>("96000");
  const {
    history: searchHistory,
    error: historyError,
    refetchHistory,
  } = useSearchHistory();
  const [spectrumData, setSpectrumData] = useState<Array<{
    mz: number;
    frequency: number;
    intensity: number;
    amplitude_linear: number;
    amplitude_db: number;
  }> | null>(null);
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [compounds, setCompounds] = useState<string[]>([]);

  useEffect(() => {
    fetch("/compounds.json")
      .then((res) => res.json())
      .then((data) => setCompounds(data))
      .catch((err) => console.error("Failed to load compounds:", err));
  }, []);

  useEffect(() => {
    const handleFetch = async () => {
      if (!compound.trim()) {
        setStatus("Please enter a compound name.");
        return;
      }

      const sampleRateNum = Number(sampleRate);
      if (
        isNaN(sampleRateNum) ||
        sampleRateNum < 3500 ||
        sampleRateNum > 192000
      ) {
        setStatus("Sample rate must be between 3500 and 192000.");
        return;
      }

      const durationNum = Number(duration);
      if (isNaN(durationNum) || durationNum < 0.01 || durationNum > 30) {
        setStatus("Duration must be between 0.01 and 30.");
        return;
      }

      setStatus("Fetching audio...");
      setAudioUrl("");
      setCompoundName("");
      setAccession("");

      // Cleanup previous URL before setting new one
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }

      try {
        const requestBody: Record<string, string | number> = {
          compound,
          duration: durationNum,
          sample_rate: sampleRateNum,
        };

        if (algorithm === "linear") {
          requestBody.offset = offset;
        } else if (algorithm === "inverse") {
          requestBody.scale = scale;
          requestBody.shift = shift;
        }

        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/massbank/${algorithm}`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
          }
        );

        if (!response.ok) {
          const errorData = await response.json();
          setStatus(`Error: ${errorData.error}`);
          return;
        }

        const data = await response.json();

        // Convert base64 audio to blob
        const audioBlob = base64ToBlob(data.audio_base64);
        const url = URL.createObjectURL(audioBlob);

        setCompoundName(data.compound);
        setAccession(data.accession);
        setAudioUrl(url);
        setSpectrumData(data.spectrum);
        setStatus("Success!");
        refetchHistory();
      } catch (err) {
        if (err instanceof Error) {
          setStatus(`Error: ${err.message}`);
        } else {
          setStatus("An unknown error occurred.");
        }
      }
    };

    const handleGlobalKeyDown = (e: globalThis.KeyboardEvent) => {
      if (e.key === "Enter") {
        handleFetch();
      }
    };

    document.addEventListener("keydown", handleGlobalKeyDown);

    return () => {
      document.removeEventListener("keydown", handleGlobalKeyDown);
    };
  }, [
    compound,
    algorithm,
    offset,
    scale,
    shift,
    duration,
    sampleRate,
    audioUrl,
    refetchHistory,
  ]);

  const triggerFetch = () => {
    const event = new KeyboardEvent("keydown", { key: "Enter" });
    document.dispatchEvent(event);
  };

  const accessionUrl = `https://massbank.eu/MassBank/RecordDisplay?id=${accession}`;
  const downloadName = `${compoundName}-${accession}.wav`;

  useEffect(() => {
    // Cleanup function to revoke object URLs and prevent memory leaks
    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
    };
  }, [audioUrl]);

  return (
    <div data-theme="corporate" className="min-h-screen bg-base-200">
      <div className="justify-items-center p-8 flex-col w-full px-4">
        <div className="grid grid-cols-1 lg:grid-cols-3">
          {/* column 1 - spectrum data tables */}
          <div className="mx-auto m-4 order-2 lg:order-1">
            {spectrumData && (
              <>
                {/* Original Mass Spectrum Data */}
                <h2 className="font-bold text-lg mb-2">Mass Spectrum Data</h2>
                <div className="overflow-x-auto mb-6">
                  <table className="table table-compact table-zebra text-xs">
                    <thead>
                      <tr>
                        <th>m/z</th>
                        <th>Intensity</th>
                      </tr>
                    </thead>
                    <tbody>
                      {spectrumData.map((item, index) => (
                        <tr key={index}>
                          <td>{item.mz.toFixed(4)}</td>
                          <td>{item.intensity.toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Transformed Audio Data */}
                <h2 className="font-bold text-lg mb-2">
                  Audio Transformation Data
                </h2>
                <div className="overflow-x-auto">
                  <table className="table table-compact table-zebra text-xs">
                    <thead>
                      <tr>
                        <th>Frequency (Hz)</th>
                        <th>Amplitude</th>
                        <th>Amplitude (dB)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {spectrumData.map((item, index) => (
                        <tr key={index}>
                          <td>{item.frequency.toFixed(4)}</td>
                          <td>{item.amplitude_linear.toFixed(4)}</td>
                          <td>{item.amplitude_db.toFixed(4)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}
          </div>
          {/* column 2 - form, audio player, keyboard - "app core" */}
          <div className="order-1 lg:order-2">
            <div className="card bg-neutral-content w-full max-w-md mx-auto">
              <div className="card-body">
                <h1 className="text-3xl font-bold text-center mb-2">
                  Mass Spectrum to Audio Converter
                </h1>
                <div className="form-control mb-4 relative">
                  <label className="label" htmlFor="compoundInput">
                    <span className="label-text font-semibold">
                      Compound Name
                    </span>
                  </label>
                  <input
                    id="compoundInput"
                    type="text"
                    placeholder="e.g. biotin"
                    className="input input-bordered w-full placeholder-gray-400"
                    autoComplete="off"
                    value={compound}
                    onChange={(e) => {
                      const value = e.target.value;
                      setCompound(value);

                      // Update suggestions
                      if (value.length >= 1) {
                        const filtered = compounds
                          .filter((name) =>
                            name.toLowerCase().startsWith(value.toLowerCase())
                          )
                          .slice(0, 10);
                        setSuggestions(filtered);
                        setShowSuggestions(true);
                      } else {
                        setShowSuggestions(false);
                      }
                    }}
                    onBlur={() => {
                      // Hide suggestions after a delay to allow clicking
                      setTimeout(() => setShowSuggestions(false), 200);
                    }}
                    onFocus={() => {
                      if (compound.length >= 1) {
                        setShowSuggestions(true);
                      }
                    }}
                  />

                  {/* Suggestions dropdown */}
                  {showSuggestions && suggestions.length > 0 && (
                    <div className="absolute top-full left-0 right-0 bg-white border border-gray-300 rounded-md shadow-lg z-50 max-h-60 overflow-y-auto">
                      {suggestions.map((suggestion, index) => (
                        <div
                          key={index}
                          className="px-4 py-2 hover:bg-gray-100 cursor-pointer text-sm"
                          onClick={() => {
                            setCompound(suggestion);
                            setShowSuggestions(false);
                          }}
                        >
                          {suggestion}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
                <fieldset className="form-control mb-4">
                  <legend className="label-text font-semibold mb-1">
                    Algorithm
                  </legend>
                  <div className="flex flex-col gap-2">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="algorithm"
                        className="radio radio-primary"
                        checked={algorithm === "linear"}
                        onChange={() => setAlgorithm("linear")}
                      />
                      <span className="label-text">Linear (m/z + offset)</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="radio"
                        name="algorithm"
                        className="radio radio-primary"
                        checked={algorithm === "inverse"}
                        onChange={() => setAlgorithm("inverse")}
                      />
                      <span className="label-text">
                        Inverse (scale / (m/z + shift))
                      </span>
                    </label>
                  </div>
                </fieldset>
                {algorithm === "linear" && (
                  <div className="form-control mb-4">
                    <label className="label" htmlFor="offsetInput">
                      <span className="label-text font-semibold">
                        Offset (m/z) (Linear only)
                      </span>
                    </label>
                    <input
                      id="offsetInput"
                      type="number"
                      placeholder="e.g. 300"
                      className="input input-bordered w-full"
                      value={offset}
                      onChange={(e) => setOffset(e.target.value)}
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Shifts all m/z values before pitch conversion.
                    </p>
                  </div>
                )}
                {algorithm === "inverse" && (
                  <>
                    <div className="form-control mb-4">
                      <label className="label" htmlFor="scaleInput">
                        <span className="label-text font-semibold">
                          Scale (Inverse only)
                        </span>
                      </label>
                      <input
                        id="scaleInput"
                        type="number"
                        placeholder="e.g. 100000"
                        className="input input-bordered w-full"
                        value={scale}
                        onChange={(e) => setScale(e.target.value)}
                      />
                    </div>

                    <div className="form-control mb-4">
                      <label className="label" htmlFor="shiftInput">
                        <span className="label-text font-semibold">
                          Shift (Inverse only)
                        </span>
                      </label>
                      <input
                        id="shiftInput"
                        type="number"
                        placeholder="e.g. 1"
                        className="input input-bordered w-full"
                        value={shift}
                        onChange={(e) => setShift(e.target.value)}
                      />
                    </div>
                  </>
                )}
                <div className="form-control mb-4">
                  <label className="label" htmlFor="durationInput">
                    <span className="label-text font-semibold">Duration</span>
                  </label>
                  <input
                    id="durationInput"
                    type="number"
                    placeholder="e.g. 5"
                    className="input input-bordered w-full"
                    value={duration}
                    onChange={(e) => setDuration(e.target.value)}
                  />
                </div>
                <div className="form-control mb-4">
                  <label className="label" htmlFor="sampleRateInput">
                    <span className="label-text font-semibold">
                      Sample Rate (Hz)
                    </span>
                  </label>
                  <input
                    id="sampleRateInput"
                    type="number"
                    placeholder="e.g. 96000"
                    className="input input-bordered w-full"
                    value={sampleRate}
                    onChange={(e) => setSampleRate(e.target.value)}
                    min={3500}
                    max={192000}
                  />
                </div>
                <button
                  className="btn btn-primary w-full mb-4"
                  onClick={triggerFetch}
                  disabled={status === "Fetching audio..."}
                >
                  Generate Audio
                </button>

                {status && (
                  <div className="text-sm text-center mb-2">
                    {status === "Fetching audio..." ? (
                      <>
                        <span className="loading loading-spinner text-primary"></span>
                      </>
                    ) : (
                      <span>{status}</span>
                    )}
                  </div>
                )}

                {compoundName && accession && (
                  <div className="text-center mb-4">
                    <p>
                      <span className="font-semibold">Compound:</span>{" "}
                      {compoundName}
                      <br />
                      <span className="font-semibold">Accession:</span>{" "}
                      <a
                        href={accessionUrl}
                        className="link text-info"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {accession}
                      </a>
                    </p>
                  </div>
                )}
                {audioUrl && (
                  <div className="flex flex-col items-center gap-6">
                    <audio controls src={audioUrl} className="w-full" />
                    <a
                      href={audioUrl}
                      download={downloadName}
                      className="btn btn-outline btn-sm"
                    >
                      Download WAV
                    </a>
                  </div>
                )}
                <p className="text-xs text-gray-500 mt-2">
                  Protip: If you plan to use the .wav in a sampler, download a
                  lower pitched sample with a higher sample rate to retain
                  fidelity.
                </p>
              </div>
            </div>
            {audioUrl && <SamplePiano audioUrl={audioUrl} />}
          </div>
          {/* column 3 - Search history */}
          <div className="mx-auto m-4 order-3 lg:order-3">
            <h2 className="font-bold text-lg mb-2">Recently Generated</h2>
            {historyError ? (
              <p className="text-sm text-red-500">{historyError}</p>
            ) : (
              <ul className="list-disc list-inside space-y-1 text-sm">
                {searchHistory.map((entry, i) => (
                  <li key={i}>
                    <span className="font-medium">{entry.compound}</span>
                  </li>
                  // possible future implementation
                  // <details key={i}>
                  //   <summary className="font-medium">{entry.compound}</summary>
                  //   <div className="pl-4 text-xs text-gray-500">
                  //     Accession: {entry.accession}
                  //     <br />
                  //     {new Date(entry.created_at).toLocaleString()}
                  //   </div>
                  // </details>
                ))}
              </ul>
            )}
          </div>
          {/* end column 3 */}
        </div>
      </div>
    </div>
  );
}

export default App;
