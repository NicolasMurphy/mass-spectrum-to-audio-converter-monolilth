export default function SkeletonSpectrumTables() {
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
            <tr>
              <td>
                <div className="skeleton h-8 w-full"></div>
              </td>
              <td>
                <div className="skeleton h-8 w-full"></div>
              </td>
            </tr>
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
            <tr>
              <td>
                <div className="skeleton h-8 w-full"></div>
              </td>
              <td>
                <div className="skeleton h-8 w-full"></div>
              </td>
              <td>
                <div className="skeleton h-8 w-full"></div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </>
  );
}
