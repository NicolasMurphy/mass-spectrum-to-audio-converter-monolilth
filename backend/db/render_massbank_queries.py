from db.connection_pool import get_connection, return_connection


def get_massbank_peaks(compound_name):
    """
    Get mass spectrum peaks from local PostgreSQL database
    Two-step search like MassBank API: find compounds first, then get peaks
    Returns: (spectrum, accession, compound_actual)
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Step 1: Search the fast compound_accessions table (case-insensitive)
        search_query = """
        SELECT accession, compound_name
        FROM compound_accessions
        WHERE LOWER(compound_name) = LOWER(%s)
        ORDER BY accession
        LIMIT 1
        """

        cursor.execute(search_query, (compound_name,))
        result = cursor.fetchone()

        if not result:
            raise ValueError("No records found")

        # Use the first result
        accession, compound_actual = result

        # Step 2: Get all peaks for this specific accession (with DISTINCT to handle any duplicates)
        peaks_query = """
        SELECT DISTINCT mz, intensity
        FROM spectrum_data
        WHERE accession = %s
        ORDER BY mz
        """

        cursor.execute(peaks_query, (accession,))
        peak_data = cursor.fetchall()

        # Convert to the format expected by converter.py
        spectrum = [(float(mz), float(intensity)) for mz, intensity in peak_data]

        return spectrum, accession, compound_actual

    except Exception as e:
        raise ValueError(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)


def search_compounds(query, limit=10):
    """
    Search for compounds matching the query
    Returns list of (accession, compound_name, peak_count)
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        search_query = """
        SELECT accession, compound_name,
               COUNT(*) as peak_count
        FROM spectrum_data
        WHERE LOWER(compound_name) LIKE LOWER(%s)
        GROUP BY accession, compound_name
        ORDER BY peak_count DESC, compound_name
        LIMIT %s
        """

        cursor.execute(search_query, (f"%{query}%", limit))
        results = cursor.fetchall()

        return results

    except Exception as e:
        print(f"Search error: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)


if __name__ == "__main__":
    pass
