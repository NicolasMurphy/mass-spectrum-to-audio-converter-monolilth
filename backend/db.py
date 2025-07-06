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
