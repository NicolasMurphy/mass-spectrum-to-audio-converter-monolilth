import psycopg2
import os


def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432),
    )


def log_search_if_new(compound, accession):
    try:
        conn = get_db_connection()
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
        conn.close()

    except Exception as e:
        print(f"Failed to log search: {e}")


def get_search_history(limit=10):
    try:
        conn = get_db_connection()
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
        conn.close()

        return [
            {"accession": row[0], "compound": row[1], "created_at": row[2].isoformat()}
            for row in rows
        ]

    except Exception as e:
        print(f"Failed to fetch search history: {e}")
        return []
