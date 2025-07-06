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
cur = conn.cursor()

# Create the table if it doesn't exist
cur.execute(
    """
CREATE TABLE IF NOT EXISTS search_history (
    accession TEXT PRIMARY KEY,
    compound TEXT NOT NULL
);
"""
)

conn.commit()
cur.close()
conn.close()

print("search_history table created or already exists.")
