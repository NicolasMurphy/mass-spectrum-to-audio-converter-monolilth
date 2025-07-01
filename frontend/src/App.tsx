import { useState, KeyboardEvent } from 'react';

function App() {
  const [compound, setCompound] = useState<string>('');
  const [status, setStatus] = useState<string>('');
  const [audioUrl, setAudioUrl] = useState<string>('');
  const [compoundName, setCompoundName] = useState<string>('');
  const [accession, setAccession] = useState<string>('');

  const handleFetch = async () => {
    if (!compound.trim()) {
      setStatus('Please enter a compound name.');
      return;
    }

    setStatus('Fetching audio...');
    setAudioUrl('');
    setCompoundName('');
    setAccession('');

    try {
      const response = await fetch(
        `https://mass-spectrum-to-audio-converter.onrender.com/generate?compound=${encodeURIComponent(compound)}`
      );

      if (!response.ok) {
        const error = await response.json();
        setStatus(`Error: ${error.error}`);
        return;
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);

      setCompoundName(response.headers.get('X-Compound') || compound);
      setAccession(response.headers.get('X-Accession') || 'unknown');
      setAudioUrl(url);
      setStatus('Success!');
    } catch (err: any) {
      setStatus(`Error: ${err.message}`);
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') handleFetch();
  };

  const accessionUrl = `https://massbank.eu/MassBank/RecordDisplay?id=${accession}`;
  const downloadName = `${compoundName}-${accession}.wav`;

  return (
    <div style={{ padding: '1rem' }}>
      <h1>Mass Spectrum to Audio Converter</h1>
      <input
        type="text"
        placeholder="Enter compound name..."
        value={compound}
        onChange={(e) => setCompound(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <button onClick={handleFetch}>Generate Audio</button>

      <p>{status}</p>

      {compoundName && accession && (
        <p>
          Compound: {compoundName} | Accession:{' '}
          <a href={accessionUrl} target="_blank" rel="noopener noreferrer">
            {accession}
          </a>
        </p>
      )}

      {audioUrl && (
        <>
          <audio controls src={audioUrl}></audio>
          <br />
          <a href={audioUrl} download={downloadName}>
            Download WAV
          </a>
        </>
      )}
    </div>
  );
}

export default App;
