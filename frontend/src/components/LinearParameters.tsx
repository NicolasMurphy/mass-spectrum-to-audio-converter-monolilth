interface LinearParametersProps {
  offset: string;
  onChange: (value: string) => void;
}

export default function LinearParameters({
  offset,
  onChange,
}: LinearParametersProps) {
  return (
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
        onChange={(e) => onChange(e.target.value)}
      />
      <p className="text-xs text-gray-500 mt-1">
        Shifts all m/z values before pitch conversion.
      </p>
    </div>
  );
}
