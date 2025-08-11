# import redis
# import json
from db import get_connection, return_connection

# redis_client = redis.from_url(
#     "redis url goes here",
#     decode_responses=True,
# )


# def dedupe_peaks(peaks):
#     """Remove duplicate [mz, intensity] pairs"""
#     seen = set()
#     return [
#         peak for peak in peaks if not (tuple(peak) in seen or seen.add(tuple(peak)))
#     ]


def get_massbank_peaks(compound_name):
    """
    Get mass spectrum peaks from local PostgreSQL database
    Two-step search like MassBank API: find compounds first, then get peaks
    Returns: (spectrum, accession, compound_actual)
    """

    # # Try Redis first
    # try:
    #     print(f"Trying Redis for: {compound_name}")
    #     accession = redis_client.get(f"v1:accmap:{compound_name.lower()}")

    #     if accession:
    #         print(f"Found in Redis: {accession}")
    #         spectrum_data = redis_client.get(f"v1:acc:{accession}")
    #         if spectrum_data and isinstance(spectrum_data, str):
    #             print("Using Redis data!")
    #             data = json.loads(spectrum_data)
    #             # Deduplicate peaks on fetch
    #             peaks = dedupe_peaks(data["peaks"])
    #             spectrum = [(float(mz), float(intensity)) for mz, intensity in peaks]
    #             return spectrum, accession, compound_name
    #         else:
    #             print("No spectrum data, falling back to PG")
    #     else:
    #         print(f"'{compound_name}' not in Redis, using PG")

    # except Exception as e:
    #     print(f"Redis error: {e}, falling back to PostgreSQL")

    # print("Using PostgreSQL fallback")

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
