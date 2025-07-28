import { useState, useEffect, useCallback } from "react";

interface PopularCompound {
  compound: string;
  search_count: number;
}

export const usePopularCompounds = (limit: number = 20) => {
  const [popularCompounds, setPopularCompounds] = useState<PopularCompound[]>(
    []
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPopularCompounds = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/popular?limit=${limit}`
      );

      if (!res.ok) {
        const errorData = await res.json();
        throw new Error(errorData.error || "Unknown error from server.");
      }

      const data = await res.json();
      setPopularCompounds(data.popular || []);
    } catch (err) {
      console.error("Failed to fetch popular compounds:", err);
      setError("Failed to load popular compounds");
      setPopularCompounds([]);
    } finally {
      setLoading(false);
    }
  }, [limit]);

  useEffect(() => {
    fetchPopularCompounds();
  }, [fetchPopularCompounds]);

  return {
    popularCompounds,
    loading,
    error,
    refetch: fetchPopularCompounds,
  };
};
