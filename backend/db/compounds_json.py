import json
from connection_pool import get_connection, return_connection


def export_compounds_to_json():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT DISTINCT compound_name
            FROM compound_accessions
            ORDER BY compound_name
        """
        )

        compounds = [row[0] for row in cursor.fetchall()]

        with open("compounds.json", "w", encoding="utf-8") as f:
            json.dump(compounds, f, indent=2, ensure_ascii=False)

        print(f"Exported {len(compounds)} compounds to compounds.json")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            return_connection(conn)


if __name__ == "__main__":
    export_compounds_to_json()
