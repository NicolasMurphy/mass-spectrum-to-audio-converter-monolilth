interface ModuloParametersProps {
  factor: string;
  modulus: string;
  constant: string;
  onFactorChange: (value: string) => void;
  onModulusChange: (value: string) => void;
  onConstantChange: (value: string) => void;
}

export default function ModuloParameters({
  factor,
  modulus,
  constant,
  onFactorChange,
  onModulusChange,
  onConstantChange,
}: ModuloParametersProps) {
  return (
    <>
      <div className="form-control mb-4">
        <label className="label" htmlFor="factorInput">
          <span className="label-text font-semibold">Factor (Modulo only)</span>
        </label>
        <input
          id="factorInput"
          type="number"
          placeholder="e.g. 10"
          className="input input-bordered w-full"
          value={factor}
          onChange={(e) => onFactorChange(e.target.value)}
        />
      </div>

      <div className="form-control mb-4">
        <label className="label" htmlFor="modulusInput">
          <span className="label-text font-semibold">
            Modulus (Modulo only)
          </span>
        </label>
        <input
          id="modulusInput"
          type="number"
          placeholder="e.g. 500"
          className="input input-bordered w-full"
          value={modulus}
          onChange={(e) => onModulusChange(e.target.value)}
        />
      </div>
      <div className="form-control mb-4">
        <label className="label" htmlFor="constantInput">
          <span className="label-text font-semibold">
            Constant (Modulo only)
          </span>
        </label>
        <input
          id="constantInput"
          type="number"
          placeholder="e.g. 100"
          className="input input-bordered w-full"
          value={constant}
          onChange={(e) => onConstantChange(e.target.value)}
        />
      </div>
    </>
  );
}
