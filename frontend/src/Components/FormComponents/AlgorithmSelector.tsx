import { type AlgorithmSelectorProps } from "../../types";

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
            required
            type="radio"
            name="algorithm"
            className="radio radio-primary"
            checked={algorithm === "linear"}
            onChange={() => onChange("linear")}
          />
          <span className="label-text">Linear: mz + offset</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            required
            type="radio"
            name="algorithm"
            className="radio radio-primary"
            checked={algorithm === "inverse"}
            onChange={() => onChange("inverse")}
          />
          <span className="label-text">Inverse: scale / (mz + shift)</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer">
          <input
            required
            type="radio"
            name="algorithm"
            className="radio radio-primary"
            checked={algorithm === "modulo"}
            onChange={() => onChange("modulo")}
          />
          <span className="label-text">
            Modulo: ((mz * factor) % modulus) + base
          </span>
        </label>
      </div>
    </fieldset>
  );
}
