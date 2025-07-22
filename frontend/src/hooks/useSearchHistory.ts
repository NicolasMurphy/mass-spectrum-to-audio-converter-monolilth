import { useEffect, useState } from "react";

interface HistoryEntry {
  compound: string;
  accession: string;
  created_at: string;
}

interface UseSearchHistoryReturn {
  history: HistoryEntry[];
  error: string | null;
  loading: boolean;
  refetchHistory: () => void;
}

export function useSearchHistory(limit: number = 50): UseSearchHistoryReturn {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchHistory = async () => {
    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/history?limit=${limit}`
      );

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Unknown error from server.");
      }

      const data = await res.json();

      // Deduplicate using accession as the unique identifier
      const seen = new Set<string>();
      const uniqueHistory = [];

      for (const entry of data.history) {
        if (!seen.has(entry.accession)) {
          seen.add(entry.accession);
          uniqueHistory.push(entry);
        }
        if (uniqueHistory.length >= 20) break; // limit display to 20
      }

      setHistory(uniqueHistory);
      setError(null);
    } catch (err) {
      // Silent failure for refetch, but show error on initial load
      if (loading) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unknown error occurred.");
        }
      }
    } finally {
      setLoading(false);
    }
  };

  const refetchHistory = () => {
    // Don't show loading state for refetch, just silently update
    fetchHistory();
  };

  useEffect(() => {
    fetchHistory();
  }, [limit]);

  return {
    history,
    error,
    loading,
    refetchHistory,
  };
}
