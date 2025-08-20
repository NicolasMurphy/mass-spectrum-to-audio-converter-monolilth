#!/bin/bash
set -e

echo "Initializing mass spectrum database..."

# Create the user that the dump expects
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER mass_spectrum_db_user WITH SUPERUSER;
    SELECT 'Database and user ready for import';
EOSQL

# Import the full database dump (ignore permission errors at the end)
echo "Importing full database dump (this may take a few minutes)..."
psql -v ON_ERROR_STOP=0 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" < /docker-entrypoint-initdb.d/mass_spectrum_db.sql

echo "Database initialization complete!"
echo "Note: Some permission errors at the end are normal and can be ignored"
