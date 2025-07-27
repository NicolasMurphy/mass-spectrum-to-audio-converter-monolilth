interface RecentlyGeneratedProps {
  searchHistory: Array<{ compound: string }>;
  historyError: string | null;
}

export default function RecentlyGenerated({
  searchHistory,
  historyError,
}: RecentlyGeneratedProps) {
  return (
    <>
      <h2 className="font-bold text-lg mb-2">Recently Generated</h2>
      {historyError ? (
        <p className="text-sm text-red-500">{historyError}</p>
      ) : (
        <ul className="list-disc list-inside space-y-1 text-sm">
          {searchHistory.map((entry, i) => (
            <li key={i}>
              <span className="font-medium">{entry.compound}</span>
            </li>
            // possible future implementation
            // <details key={i}>
            //   <summary className="font-medium">{entry.compound}</summary>
            //   <div className="pl-4 text-xs text-gray-500">
            //     Accession: {entry.accession}
            //     <br />
            //     {new Date(entry.created_at).toLocaleString()}
            //   </div>
            // </details>
          ))}
        </ul>
      )}
    </>
  );
}
