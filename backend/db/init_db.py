import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", 5432),
)
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute(
    #     """
    # DROP TABLE IF EXISTS search_history;
    # """
    """
    CREATE TABLE IF NOT EXISTS search_history (
        id SERIAL PRIMARY KEY,
        accession TEXT NOT NULL,
        compound TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    """
)

conn.commit()
cursor.close()
conn.close()

print("search_history table created or already exists.")
