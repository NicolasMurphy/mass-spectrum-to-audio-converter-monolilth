interface AudioSettingsProps {
  duration: string;
  sampleRate: string;
  onDurationChange: (value: string) => void;
  onSampleRateChange: (value: string) => void;
}

export default function AudioSettings({
  duration,
  sampleRate,
  onDurationChange,
  onSampleRateChange,
}: AudioSettingsProps) {
  return (
    <>
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
          onChange={(e) => onDurationChange(e.target.value)}
        />
      </div>
      <div className="form-control mb-4">
        <label className="label" htmlFor="sampleRateInput">
          <span className="label-text font-semibold">Sample Rate (Hz)</span>
        </label>
        <input
          id="sampleRateInput"
          type="number"
          placeholder="e.g. 44100"
          className="input input-bordered w-full"
          value={sampleRate}
          onChange={(e) => {
            const value = e.target.value;
            // Only allow empty string or integers (no decimals)
            if (value === "" || /^\d+$/.test(value)) {
              onSampleRateChange(value);
            }
          }}
          min={3500}
          max={192000}
        />
      </div>
    </>
  );
}
