interface SpectrumData {
  mz: number;
  frequency: number;
  intensity: number;
  amplitude_linear: number;
  amplitude_db: number;
}

interface SpectrumTablesProps {
  spectrumData: SpectrumData[] | null;
}

export default function SpectrumTables({ spectrumData }: SpectrumTablesProps) {
  if (!spectrumData) return null;

  return (
    <>
      {/* Original Mass Spectrum Data */}
      <h2 className="font-bold text-lg mb-2">Mass Spectrum Data</h2>
      <div className="overflow-x-auto mb-6">
        <table className="table table-compact table-zebra text-xs">
          <thead>
            <tr>
              <th>m/z</th>
              <th>Intensity</th>
            </tr>
          </thead>
          <tbody>
            {spectrumData.map((item, index) => (
              <tr key={index}>
                <td>{item.mz.toFixed(4)}</td>
                <td>{item.intensity.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Transformed Audio Data */}
      <h2 className="font-bold text-lg mb-2">Audio Transformation Data</h2>
      <div className="overflow-x-auto">
        <table className="table table-compact table-zebra text-xs">
          <thead>
            <tr>
              <th>Frequency (Hz)</th>
              <th>Amplitude</th>
              <th>Amplitude (dB)</th>
            </tr>
          </thead>
          <tbody>
            {spectrumData.map((item, index) => (
              <tr key={index}>
                <td>{item.frequency.toFixed(4)}</td>
                <td>{item.amplitude_linear.toFixed(4)}</td>
                <td>{item.amplitude_db.toFixed(4)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
