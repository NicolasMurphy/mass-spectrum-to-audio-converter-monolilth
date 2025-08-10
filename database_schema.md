# Mass Spectrum Database Schema

This document covers how the backend uses the `mass_spectrum_db` database hosted on Render. The database has four tables, but the current code only uses three of them. Only the `search_history` table gets written to - everything else is read-only.

## Active tables and indexes

These tables and indexes are referenced by the backend to serve requests. Unused structures are listed separately at the end of this document.

### `compound_accessions`

| Column          | Type           | Nullable | Notes                                                  |
| --------------- | -------------- | -------- | ------------------------------------------------------ |
| `compound_name` | `varchar(500)` | No       | Compound name. Case-insensitive lookups are supported. |
| `accession`     | `varchar(50)`  | No       | MassBank accession associated with the compound.       |

**Used index**

- `idx_compound_accessions_name_lower` - B-tree index on `lower(compound_name)`. The backend performs case-insensitive equality searches for compounds using this index.

### `search_history`

| Column       | Type                       | Nullable | Default                            | Notes                            |
| ------------ | -------------------------- | -------- | ---------------------------------- | -------------------------------- |
| `id`         | `int`                      | No       | `nextval('search_history_id_seq')` | Primary key. Auto-incremented.   |
| `accession`  | `text`                     | No       |                                    | Accession looked up by the user. |
| `compound`   | `text`                     | No       |                                    | Compound name looked up.         |
| `created_at` | `timestamp with time zone` | Yes      | `CURRENT_TIMESTAMP`                | Time of search.                  |

**Used index**

- Primary key `search_history_pkey` on `id` - supports efficient retrieval and ordering of search history entries.

This table is appended to whenever a user performs a search; it is the only mutable table in the database.

### `spectrum_data`

| Column          | Type            | Nullable | Notes                                           |
| --------------- | --------------- | -------- | ----------------------------------------------- |
| `accession`     | `varchar(50)`   | No       | Foreign key to `compound_accessions.accession`. |
| `compound_name` | `varchar(500)`  | No       | Redundant; stored for convenience.              |
| `mz`            | `numeric(12,4)` | No       | Mass-to-charge ratio (m/z).                     |
| `intensity`     | `numeric(15,2)` | No       | Peak intensity.                                 |

**Used index**

- `idx_accession` - B-tree index on `accession` for fast retrieval of peaks by accession. The backend queries this table by accession and orders results by `mz`.

## Data volumes

- `spectrum_data` contains approximately 6.33 million rows.
- `compound_accessions` contains roughly 217 k rows.

`search_history` grows over time as users perform searches; the other tables remain static unless MassBank data is reimported.

## Unused tables and indexes

The following tables and indexes exist in the schema but are **not** referenced by the current backend code. They remain in the database for potential future use (e.g., regenerating JSON files) but have no effect on current functionality.

### Unused table

- **`compounds`** - This table holds two columns (`id`, `name`) but is not read by the backend. The front-end uses a pre-generated `compounds.json` file for auto-complete suggestions, and compound names required for peak lookups come from `compound_accessions`.

### Unused indexes

These indexes are not used because the current queries do not search on the corresponding columns or patterns:

- `idx_compound_accessions_name` and `idx_compound_accessions_name_ilike` on `compound_accessions.compound_name` - the backend relies on the `lower(compound_name)` index instead.
- `idx_compounds_name` and `idx_compounds_name_prefix` on `compounds.name` - the `compounds` table itself is unused.
- `idx_compound_name_exact` and `idx_compound_name_prefix` on `spectrum_data.compound_name` - queries filter `spectrum_data` by `accession` and do not search by `compound_name`.
- `idx_compound_name_lower`: 0 scans under normal traffic; one scan on 2025-08-10 likely maintenance/ad-hoc. Monitor; treat as unused.

These unused structures consume some storage and slightly slow down write operations. However, because the tables are static and writes are rare, the overhead is negligible. They can be dropped to simplify the schema, but retaining them poses no significant downside in the current setup.
