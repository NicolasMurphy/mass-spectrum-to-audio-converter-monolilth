from .connection_pool import get_connection, return_connection


def log_search(compound, accession):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO search_history (accession, compound)
            VALUES (%s, %s)
            """,
            (accession, compound),
        )

        conn.commit()

    except Exception as e:
        print(f"Failed to log search: {e}")
        if conn:
            conn.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)


def get_search_history(limit):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT accession, compound, created_at
            FROM search_history
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,),
        )

        rows = cursor.fetchall()

        return [
            {"accession": row[0], "compound": row[1], "created_at": row[2].isoformat()}
            for row in rows
        ]

    except Exception as e:
        print(f"Failed to fetch search history: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)


def get_popular_compounds(limit):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT compound, COUNT(*) as search_count
            FROM search_history
            WHERE compound IS NOT NULL
            GROUP BY compound
            ORDER BY search_count DESC
            LIMIT %s
            """,
            (limit,),
        )

        rows = cursor.fetchall()

        return [{"compound": row[0], "search_count": row[1]} for row in rows]

    except Exception as e:
        print(f"Failed to fetch popular compounds: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)
