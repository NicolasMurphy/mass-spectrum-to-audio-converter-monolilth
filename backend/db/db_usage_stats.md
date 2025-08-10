# Database Usage Statistics

This document captures usage metrics for the Render-hosted mass-spectrum database as observed via PostgreSQL's `pg_stat_user_indexes` and `pg_stat_all_tables` views on August 10, 2025. These statistics provide insight into which indexes and tables are actively used by the backend and which remain idle.

## Index scans (`pg_stat_user_indexes`)

The table below shows the number of times each index has been scanned (`idx_scan`), the last time it was used, and how many index entries and table rows were read.

| Table               | Index name                         | idx_scan | Last used (UTC)               | idx_tup_read | idx_tup_fetch |
| ------------------- | ---------------------------------- | -------- | ----------------------------- | ------------ | ------------- |
| compound_accessions | idx_compound_accessions_name       | 0        | -                             | 0            | 0             |
| compound_accessions | idx_compound_accessions_name_ilike | 0        | -                             | 0            | 0             |
| compound_accessions | idx_compound_accessions_name_lower | 296      | 2025-08-10 16:25:42.626322+00 | 11 374       | 811           |
| compounds           | compounds_pkey                     | 0        | -                             | 0            | 0             |
| compounds           | idx_compounds_name                 | 0        | -                             | 0            | 0             |
| compounds           | idx_compounds_name_prefix          | 0        | -                             | 0            | 0             |
| search_history      | search_history_pkey                | 0        | -                             | 0            | 0             |
| spectrum_data       | idx_accession                      | 291      | 2025-08-10 16:25:42.626322+00 | 42 517       | 10 539        |
| spectrum_data       | idx_compound_name_exact            | 0        | -                             | 0            | 0             |
| spectrum_data       | idx_compound_name_lower            | 1        | 2025-08-10 19:10:44.322229+00 | 6 331 892    | 0             |
| spectrum_data       | idx_compound_name_prefix           | 0        | -                             | 0            | 0             |

- `idx_compound_name_lower`: 0 scans under normal traffic; one scan on 2025-08-10 likely maintenance/ad-hoc. Monitor; treat as unused.

## Table row counts (`pg_stat_all_tables`)

| Table               | Approximate row count |
| ------------------- | --------------------- |
| compound_accessions | 217 053               |
| compounds           | 226 822               |
| spectrum_data       | 6 330 291             |
| search_history      | 1 112                 |
