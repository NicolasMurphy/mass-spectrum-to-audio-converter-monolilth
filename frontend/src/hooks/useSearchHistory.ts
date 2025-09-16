import { useEffect, useState, useCallback } from "react";
import { type UseSearchHistoryReturn, type HistoryEntry } from "../types";

export function useSearchHistory(limit: number = 100): UseSearchHistoryReturn {
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const fetchHistory = useCallback(async () => {
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
        if (uniqueHistory.length >= 20) break;
      }

      setHistory(uniqueHistory);
      setError(null);
    } catch (err) {
      if (loading) {
        console.error("Failed to get recently generated compounds:", err);
        setError("Failed to get recently generated compounds");
      }
    } finally {
      setLoading(false);
    }
  }, [limit, loading]);

  const refetchHistory = () => {
    fetchHistory();
  };

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  return {
    history,
    error,
    loading,
    refetchHistory,
  };
}
