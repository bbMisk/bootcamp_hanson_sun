# Homework 05 — Data Storage

## Data Storage

- `data/raw/` stores a timestamped CSV for portable, human-readable exchange.
- `data/processed/` stores the equivalent Parquet file for efficient typed analytics.
- `DATA_DIR_RAW` and `DATA_DIR_PROCESSED` are loaded from the local ignored `.env` file.
- `src/storage.py` routes reads and writes by suffix, creates missing parent directories, parses the `date` column from CSV, and gives a clear Parquet-engine error.
- The executed notebook reloads both files and asserts shape, column, date, and representative-value agreement with the source frame.

AI assistance was used to implement and verify the storage workflow; Hanson Sun reviewed the outputs and documentation.
