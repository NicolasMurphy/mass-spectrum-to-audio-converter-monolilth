import { useState } from "react";
import type { KeyboardEvent } from "react";
import "./App.css";
import SamplePiano from "./SamplePiano";
//
function App() {
  const [compound, setCompound] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [audioUrl, setAudioUrl] = useState<string>("");
  const [compoundName, setCompoundName] = useState<string>("");
  const [accession, setAccession] = useState<string>("");
  const [algorithm, setAlgorithm] = useState<"linear" | "inverse">("linear");
  const [offset, setOffset] = useState<number>(300);
  const [scale, setScale] = useState<number>(100000);
  const [shift, setShift] = useState<number>(1);
  const [duration, setDuration] = useState<number>(5);
  const [sampleRate, setSampleRate] = useState<number>(96000);

  const handleFetch = async () => {
    if (!compound.trim()) {
      setStatus("Please enter a compound name.");
      return;
    }

    const sampleRateNum = sampleRate;
    if (
      isNaN(sampleRateNum) ||
      sampleRateNum < 3500 ||
      sampleRateNum > 192000
    ) {
      setStatus("Sample rate must be between 3500 and 192000.");
      return;
    }

    const durationNum = duration;
    if (isNaN(durationNum) || durationNum < 0.01 || durationNum > 30) {
      setStatus("Duration must be between 0.01 and 30.");
      return;
    }

    setStatus("Fetching audio...");
    setAudioUrl("");
    setCompoundName("");
    setAccession("");

    try {
      const queryParams = new URLSearchParams({
        compound,
        duration: durationNum.toString(),
        sample_rate: sampleRateNum.toString(),
      });

      if (algorithm === "linear") {
        queryParams.append("offset", offset.toString());
      } else if (algorithm === "inverse") {
        queryParams.append("scale", scale.toString());
        queryParams.append("shift", shift.toString());
      }

      const response = await fetch(
        // `http://localhost:5000/massbank/${algorithm}?${queryParams}`
        `https://mass-spectrum-to-audio-converter.onrender.com/massbank/${algorithm}?${queryParams}`
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
      <div className="justify-items-center p-8 flex-col w-full px-4">
        <div className="card bg-neutral-content w-full max-w-md mx-auto">
          <div className="card-body">
            <h1 className="text-3xl font-bold text-center mb-2">
              Mass Spectrum to Audio Converter
            </h1>

            <div className="form-control mb-4">
              <label className="label" htmlFor="compoundInput">
                <span className="label-text font-semibold">Compound Name</span>
              </label>
              <input
                id="compoundInput"
                type="text"
                placeholder="e.g. biotin"
                className="input input-bordered w-full placeholder-gray-400"
                value={compound}
                onChange={(e) => setCompound(e.target.value)}
                onKeyDown={handleKeyDown}
              />
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
                  onChange={(e) => setOffset(+e.target.value)} // + is shorthand for Number()
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
                    onChange={(e) => setScale(+e.target.value)}
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
                    onChange={(e) => setShift(+e.target.value)}
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
                onChange={(e) => setDuration(+e.target.value)}
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
                onChange={(e) => setSampleRate(+e.target.value)}
                min={3500}
                max={192000}
              />
            </div>

            <button
              className="btn btn-primary w-full mb-4"
              onClick={handleFetch}
              disabled={status === "Fetching audio..."}
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
            <p className="text-xs text-gray-500 mt-2">
              Protip: If you plan to use the .wav in a sampler, download a lower
              pitched sample with a higher sample rate to retain fidelity.
            </p>
          </div>
        </div>
        {audioUrl && <SamplePiano audioUrl={audioUrl} />}
      </div>
    </div>
  );
}

export default App;
