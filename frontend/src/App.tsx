import { useEffect, useState, useCallback, useRef } from "react";
import "./App.css";
import SamplePiano from "./SamplePiano";
import { useSearchHistory } from "./hooks/useSearchHistory";
import RecentlyGenerated from "./components/RecentlyGenerated";
import CompoundSearch from "./components/CompoundSearch";
import AudioPlayer from "./components/AudioPlayer";
import NameAndAccession from "./components/NameAndAccession";
import StatusMessage from "./components/StatusMessage";
import base64ToBlob from "./utils";
import SpectrumTables from "./components/SpectrumTables";
import AlgorithmSelector from "./components/AlgorithmSelector";
import LinearParameters from "./components/LinearParameters";

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

  const handleFetch = useCallback(async () => {
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

  const handleFetchRef = useRef(handleFetch);
  handleFetchRef.current = handleFetch;

  useEffect(() => {
    const handleGlobalKeyDown = (e: globalThis.KeyboardEvent) => {
      if (e.key === "Enter") {
        handleFetchRef.current();
      }
    };

    document.addEventListener("keydown", handleGlobalKeyDown);

    return () => {
      document.removeEventListener("keydown", handleGlobalKeyDown);
    };
  }, []);

  const triggerFetch = () => {
    handleFetch();
  };

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
            {spectrumData && <SpectrumTables spectrumData={spectrumData} />}
          </div>
          {/* column 2 - form, audio player, keyboard - "app core" */}
          <div className="order-1 lg:order-2">
            <div className="card bg-neutral-content w-full max-w-md mx-auto">
              <div className="card-body">
                <h1 className="text-3xl font-bold text-center mb-2">
                  Mass Spectrum to Audio Converter
                </h1>
                <CompoundSearch
                  compound={compound}
                  onCompoundChange={setCompound}
                />
                <AlgorithmSelector
                  algorithm={algorithm}
                  onChange={setAlgorithm}
                />
                {algorithm === "linear" && (
                  <LinearParameters offset={offset} onChange={setOffset} />
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
                    onChange={(e) => {
                      const value = e.target.value;
                      if (value === "" || /^\d+$/.test(value)) {
                        setSampleRate(value);
                      }
                    }}
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
                {status && <StatusMessage status={status} />}
                {compoundName && accession && (
                  <NameAndAccession
                    compoundName={compoundName}
                    accession={accession}
                  />
                )}
                {audioUrl && (
                  <AudioPlayer
                    audioUrl={audioUrl}
                    downloadName={downloadName}
                  />
                )}
              </div>
            </div>
            {audioUrl && <SamplePiano audioUrl={audioUrl} />}
          </div>
          {/* column 3 - Search history */}
          <div className="mx-auto m-4 order-3 lg:order-3">
            <RecentlyGenerated
              searchHistory={searchHistory}
              historyError={historyError}
            />
          </div>
          {/* end column 3 */}
        </div>
      </div>
    </div>
  );
}

export default App;
