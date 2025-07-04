import { useState } from "react";
import type { KeyboardEvent } from "react";
import "./App.css";
//
function App() {
  const [compound, setCompound] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [audioUrl, setAudioUrl] = useState<string>("");
  const [compoundName, setCompoundName] = useState<string>("");
  const [accession, setAccession] = useState<string>("");
  const [sampleRate, setSampleRate] = useState<string>("96000");

  const handleFetch = async () => {
    if (!compound.trim()) {
      setStatus("Please enter a compound name.");
      return;
    }

    setStatus("Fetching audio...");
    setAudioUrl("");
    setCompoundName("");
    setAccession("");

    try {
      const response = await fetch(
        // `http://localhost:5000/massbank?compound=${encodeURIComponent(
        //   compound
        // )}&sample_rate=${sampleRate}`
        `https://mass-spectrum-to-audio-converter.onrender.com/massbank?compound=${encodeURIComponent(
          compound
        )}&sample_rate=${sampleRate}`
      );

      if (!response.ok) {
        const error = await response.json();
        setStatus(`Error: ${error.error}`);
        return;
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      setCompoundName(response.headers.get("X-Compound") || compound);
      setAccession(response.headers.get("X-Accession") || "unknown");
      setAudioUrl(url);
      setStatus("Success!");
    } catch (err) {
      if (err instanceof Error) {
        setStatus(`Error: ${err.message}`);
      } else {
        setStatus("An unknown error occurred.");
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleFetch();
  };

  const accessionUrl = `https://massbank.eu/MassBank/RecordDisplay?id=${accession}`;
  const downloadName = `${compoundName}-${accession}.wav`;

  return (
    <div data-theme="corporate" className="min-h-screen bg-base-200">
      <div className="justify-items-center pt-8 flex-col w-full px-4">
        <div className="card bg-neutral-content w-full max-w-md">
          <div className="card-body">
            <h1 className="text-3xl font-bold text-center mb-2">
              Mass Spectrum to Audio Converter
            </h1>

            <div className="form-control mb-4">
              <label className="label">
                <span className="label-text font-semibold">Compound Name</span>
              </label>
              <input
                type="text"
                placeholder="e.g. biotin"
                className="input input-bordered w-full"
                value={compound}
                onChange={(e) => setCompound(e.target.value)}
                onKeyDown={handleKeyDown}
              />
            </div>

            <div className="form-control mb-4">
              <label className="label">
                <span className="label-text font-semibold">
                  Sample Rate (Hz)
                </span>
              </label>
              <input
                type="number"
                placeholder="e.g. 96000"
                className="input input-bordered w-full"
                value={sampleRate}
                onChange={(e) => setSampleRate(e.target.value)}
              />
            </div>

            <button
              className="btn btn-primary w-full mb-4"
              onClick={handleFetch}
            >
              Generate Audio
            </button>

            {status && <p className="text-sm text-center mb-2">{status}</p>}

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
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
