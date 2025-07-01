import { useState } from "react";
import type { KeyboardEvent } from "react";
import "./App.css";

function App() {
  const [compound, setCompound] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [audioUrl, setAudioUrl] = useState<string>("");
  const [compoundName, setCompoundName] = useState<string>("");
  const [accession, setAccession] = useState<string>("");

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
        `https://mass-spectrum-to-audio-converter.onrender.com/generate?compound=${encodeURIComponent(compound)}`
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
    <div data-theme="corporate" className="hero min-h-screen bg-base-100">
      <div className="hero-content flex-col w-full max-w-xl">
        <div className="card bg-base-200 w-full">
          <div className="card-body">
            <h1 className="text-3xl font-bold text-center mb-2">
              Mass Spectrum to Audio
            </h1>

            <input
              type="text"
              placeholder="Enter compound name..."
              className="input input-bordered w-full mb-4"
              value={compound}
              onChange={(e) => setCompound(e.target.value)}
              onKeyDown={handleKeyDown}
            />

            <button className="btn btn-primary w-full mb-4" onClick={handleFetch}>
              Generate Audio
            </button>

            {status && (
              <p className="text-sm text-info text-center mb-2">{status}</p>
            )}

            {compoundName && accession && (
              <div className="text-center mb-4">
                <p>
                  <span className="font-semibold">Compound:</span> {compoundName}
                  <br />
                  <span className="font-semibold">Accession:</span>{" "}
                  <a
                    href={accessionUrl}
                    className="link"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {accession}
                  </a>
                </p>
              </div>
            )}

            {audioUrl && (
              <div className="flex flex-col items-center gap-2">
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
