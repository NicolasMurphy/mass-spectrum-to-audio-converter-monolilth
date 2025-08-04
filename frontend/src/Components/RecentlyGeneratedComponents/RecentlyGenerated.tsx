import { type RecentlyGeneratedProps } from "../../types";

export default function RecentlyGenerated({
  searchHistory,
  historyError,
  onCompoundClick,
}: RecentlyGeneratedProps) {
  return (
    <>
      <h2 className="font-bold text-lg mb-4">Recently Generated</h2>
      {historyError ? (
        <div className="alert alert-error">
          <p className="text-sm">{historyError}</p>
        </div>
      ) : (
        <div className="flex flex-wrap gap-2">
          {searchHistory.map((entry, i) => (
            <div
              key={i}
              onClick={() => onCompoundClick(entry.compound)}
              className="badge badge-outline badge-sm p-3 cursor-pointer hover:badge-primary transition-colors"
            >
              <span className="truncate max-w-[120px]" title={entry.compound}>
                {entry.compound}
              </span>
            </div>
          ))}
        </div>
      )}
    </>
  );
}
