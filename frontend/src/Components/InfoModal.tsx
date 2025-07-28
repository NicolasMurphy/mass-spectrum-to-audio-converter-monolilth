import React from "react";

const InfoModal: React.FC = () => {
  return (
    <dialog id="info_modal" className="modal">
      <div className="modal-box max-w-2xl max-h-[90%]">
        <div className="flex justify-between items-center mb-4">
          <h3 className="font-bold text-lg">How to Use This App</h3>
          <form method="dialog">
            <button className="btn btn-sm btn-circle btn-ghost">✕</button>
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

          {/* Section 2: How to Use It */}
          <div>
            <h4 className="font-semibold text-base mb-2">How to Use It</h4>
            <ul className="text-sm space-y-1 list-disc list-inside">
              <li>Enter a compound name (e.g., "caffeine", "aspirin")</li>
              <li>Click Generate Audio</li>
              <li>Optionally try different algorithms and parameters</li>
              <li>
                Play back the audio, play notes on the keyboard, or download the
                file
              </li>
            </ul>
          </div>

          {/* Section 3: Algorithms & Parameters */}
          <div>
            <h4 className="font-semibold text-base mb-2">
              Algorithms & Parameters
            </h4>
            <div className="space-y-3 text-sm">
              <div>
                <div className="font-medium">
                  Linear:{" "}
                  <code className="text-xs bg-base-200 px-1 rounded">
                    frequency = m/z + offset
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
                    frequency = scale / (m/z + shift)
                  </code>
                </div>
                <div className="ml-4 text-xs opacity-80">
                  Scale: Controls the frequency range
                </div>
                <div className="ml-4 text-xs opacity-80">
                  Shift: Modifies the m/z input values before division
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
