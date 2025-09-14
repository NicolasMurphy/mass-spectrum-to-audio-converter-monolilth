import React from "react";

const InfoModal: React.FC = () => {
  return (
    <dialog id="info_modal" className="modal">
      <div className="modal-box max-w-[80%] max-h-[80%]">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-bold text-lg">How to Use This App</h3>
          <form method="dialog">
            <button
              className="btn btn-sm btn-circle btn-ghost text-lg"
              title="Close"
            >
              ✕
            </button>
          </form>
        </div>
        <div className="space-y-6">
          {/* Section 1: What This App Does */}
          <div>
            <h4 className="font-semibold text-base mb-2">What This App Does</h4>
            <p className="text-sm leading-relaxed">
              Converts mass spectrometry data into audio using sine waves. Mass
              spec data contains m/z values (mass-to-charge ratios of molecules)
              and intensity values (peak heights). This App maps m/z values to
              frequencies (Hz) and intensity values to volume (dB).
            </p>
          </div>

          {/* Section 2: Input Modes */}
          <div>
            <h4 className="font-semibold text-base mb-2">Input Modes</h4>
            <div className="space-y-3 text-sm">
              <div>
                <div className="font-medium">MassBank Tab</div>
                <div className="ml-4 text-xs opacity-80">
                  Search from ~36,000 compounds in the database. Just enter a
                  compound name like "caffeine" or "aspirin".
                </div>
              </div>
              <div>
                <div className="font-medium">Custom Tab</div>
                <div className="ml-4 text-xs opacity-80">
                  Paste your own spectrum data from external sources like HMDB.
                  Useful for compounds not in the MassBank database.
                </div>
                <div className="ml-4 text-xs opacity-80 mt-1">
                  Format: m/z intensity pairs separated by spaces, tabs, or
                  newlines:
                </div>
                <div className="ml-4 mt-1">
                  <code className="text-xs bg-base-200 px-2 py-1 rounded block">
                    73.04018778 16.07433749
                    <br />
                    75.05583784 2.042927662
                  </code>
                </div>
              </div>
            </div>
          </div>

          {/* Section 3: How to Use It */}
          <div>
            <h4 className="font-semibold text-base mb-2">How to Use It</h4>
            <div className="space-y-2 text-sm">
              <div>
                <div className="font-medium mb-1">
                  Step 1: Choose your input
                </div>
                <ul className="text-xs space-y-1 list-disc list-inside ml-4">
                  <li>
                    <strong>MassBank tab:</strong> Enter a compound name (e.g.,
                    "caffeine", "aspirin")
                  </li>
                  <li>
                    <strong>Custom tab:</strong> Paste your m/z intensity pairs
                    in the text area
                  </li>
                </ul>
              </div>
              <div>
                <div className="font-medium mb-1">Step 2: Generate audio</div>
                <ul className="text-xs space-y-1 list-disc list-inside ml-4">
                  <li>Optionally adjust algorithm and parameters</li>
                  <li>Click Generate Audio</li>
                  <li>
                    Play back the audio, play notes on the keyboard, or download
                    the file
                  </li>
                </ul>
              </div>
            </div>
          </div>

          {/* Section 4: Algorithms & Parameters */}
          <div>
            <h4 className="font-semibold text-base mb-2">
              Algorithms & Parameters
            </h4>
            <div className="space-y-3 text-sm">
              <div>
                <div className="font-medium">
                  Linear:{" "}
                  <code className="text-xs bg-base-200 px-1 rounded">
                    frequency = mz + offset
                  </code>
                </div>
                <div className="ml-4 text-xs opacity-80">
                  Offset: Increases/decreases all frequencies up by this amount
                </div>
              </div>
              <div>
                <div className="font-medium">
                  Inverse:{" "}
                  <code className="text-xs bg-base-200 px-1 rounded">
                    frequency = scale / (mz + shift)
                  </code>
                </div>
                <div className="ml-4 text-xs opacity-80">
                  Scale: Controls the frequency range
                </div>
                <div className="ml-4 text-xs opacity-80">
                  Shift: Modifies the m/z input values before division
                </div>
              </div>
              <div>
                <div className="font-medium">
                  Modulo:{" "}
                  <code className="text-xs bg-base-200 px-1 rounded">
                    frequency = ((mz * factor) % modulus) + base
                  </code>
                </div>
                <div className="ml-4 text-xs opacity-80">
                  Factor: Multiplies m/z values before wrapping
                </div>
                <div className="ml-4 text-xs opacity-80">
                  Modulus: Frequency range where values wrap back to the base
                  frequency
                </div>
                <div className="ml-4 text-xs opacity-80">
                  Base: Sets the minimum frequency
                </div>
              </div>
              <div className="pt-2 border-t border-base-300">
                <div className="font-medium">Audio Settings</div>
                <div className="ml-4 text-xs opacity-80">
                  Duration: Length of audio output (seconds)
                </div>
                <div className="ml-4 text-xs opacity-80">
                  Sample Rate: Audio resolution (Hz)
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <form method="dialog" className="modal-backdrop">
        <button>close</button>
      </form>
    </dialog>
  );
};

export default InfoModal;
