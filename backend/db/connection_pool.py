import psycopg2.pool
import os
from dotenv import load_dotenv

load_dotenv()


connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=5,
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", 5432),
)


def get_connection():
    """Get a connection from the pool"""
    return connection_pool.getconn()


def return_connection(conn):
    """Return a connection to the pool"""
    connection_pool.putconn(conn)


def close_all_connections():
    """Close all connections in the pool (for graceful shutdown)"""
    connection_pool.closeall()
