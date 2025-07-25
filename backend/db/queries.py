from .connection_pool import get_connection, return_connection


def log_search(compound, accession):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO search_history (accession, compound)
            VALUES (%s, %s)
            """,
            (accession, compound),
        )

        conn.commit()
        cur.close()

    except Exception as e:
        print(f"Failed to log search: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            return_connection(conn)


def get_search_history(limit):
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT accession, compound, created_at
            FROM search_history
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (limit,),
        )

        rows = cur.fetchall()
        cur.close()

        return [
            {"accession": row[0], "compound": row[1], "created_at": row[2].isoformat()}
            for row in rows
        ]

    except Exception as e:
        print(f"Failed to fetch search history: {e}")
        return []
    finally:
        if conn:
            return_connection(conn)
