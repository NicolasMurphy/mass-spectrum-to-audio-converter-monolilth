interface AlgorithmSelectorProps {
  algorithm: "linear" | "inverse";
  onChange: (algorithm: "linear" | "inverse") => void;
}

export default function AlgorithmSelector({
  algorithm,
  onChange,
}: AlgorithmSelectorProps) {
  return (
    <fieldset className="form-control mb-4">
      <legend className="label-text font-semibold mb-1">Algorithm</legend>
      <div className="flex flex-col gap-2">
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            name="algorithm"
            className="radio radio-primary"
            checked={algorithm === "linear"}
            onChange={() => onChange("linear")}
          />
          <span className="label-text">Linear (m/z + offset)</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            type="radio"
            name="algorithm"
            className="radio radio-primary"
            checked={algorithm === "inverse"}
            onChange={() => onChange("inverse")}
          />
          <span className="label-text">Inverse (scale / (m/z + shift))</span>
        </label>
      </div>
    </fieldset>
  );
}
