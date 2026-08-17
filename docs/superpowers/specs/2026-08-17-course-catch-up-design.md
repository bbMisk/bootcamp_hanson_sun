# FRE 5040 Course Catch-Up Design

**Date:** 2026-08-17
**Status:** Approved

## Objective

Bring the repository into alignment with the current FRE 5040 Google Drive materials, treating those materials as canonical. Preserve the completed Stage 01–02 work, complete the Stage 01–05 homework sequence, implement project Stages 03–05, and leave a verified pipeline ready for the August 17 data-preprocessing stage.

## Source of Truth

The shared Google Drive folder `Documents(BootCamp)(FRE5040)(Fall 2026)` and its current announcements, curriculum, homework sheets/starters, project milestone instructions, and repository-structure document are authoritative. Local plans written before the instructor's August 17 updates are historical context only when they conflict with the Drive.

## Repository Architecture

The course repository will have three principal work areas:

- `class_materials/`: downloaded course PDFs and starter artifacts. This directory remains ignored by Git.
- `homework/`: self-contained homework workspaces named `homework01` through `homework05`, while preserving `homework0`.
- `project/`: the only source of truth for the ongoing SPY 5-Day Volatility Risk Monitor.

The existing root-level project artifacts will be moved into `project/` and adapted in place. They will not be copied into a second implementation. The project will contain its own README, environment template, dependency file, source package, notebooks, data directories, stakeholder documentation, reports, models, and tests.

## Course-Material Intake

The current Stage 01–05 homework sheets and starter notebooks will be downloaded from the canonical Drive into `class_materials/`. Working copies will be placed in the corresponding homework directories. Project milestone requirements will be implemented directly in `project/`.

Downloaded course material is reference input, not authored submission content, and will not be committed under `class_materials/`.

## Homework Design

Each `homework/homeworkNN/` directory will contain the relevant completed notebook and any stage-specific outputs required by the current homework sheet. Notebooks will preserve the starter's teaching sequence, use bounded examples, include visible checks, and execute top-to-bottom.

The homework sequence covers:

1. Problem framing and scoping.
2. Tooling setup and environment configuration.
3. Python, NumPy, pandas, and reusable utility design.
4. API acquisition and permitted web-table ingestion with validations.
5. CSV/Parquet storage, reload checks, and environment-driven paths.

AI assistance will be disclosed factually where the course artifact calls for it. The notebooks will not claim independent manual work that did not occur.

## Project Stage 03: Python Fundamentals

Stage 03 will add:

- `project/notebooks/python_fundamentals_summary.ipynb`, demonstrating Python, NumPy, and pandas with dummy data.
- `project/src/utils.py`, with focused reusable helpers for column-name normalization and date parsing.
- Unit tests that define and verify the helpers' behavior before implementation.

The notebook will import the real helpers and explain how they will support later acquisition and preprocessing work.

## Project Stage 04: Data Acquisition and Ingestion

The project will use `yfinance` first to retrieve daily SPY data. Acquisition will be isolated in `project/src/ingestion.py` and called by `project/notebooks/project_pipeline.ipynb`.

The raw-data contract is:

- Requested symbol: `SPY`.
- Daily observations over an explicit, documented date range.
- Required market fields normalized to stable snake-case names.
- Dates parsed, ordered ascending, and unique.
- Price fields numeric, positive where present, and not wholly missing.
- The download must contain a meaningful number of rows; an empty or tiny response is a failure.
- The raw snapshot is saved under `project/data/raw/` with a reproducible filename.
- No synthetic or starter dataset may silently substitute for a failed live download.

Source, parameters, observed date range, row count, schema checks, and known limitations will be recorded in the project README and pipeline notebook.

## Project Stage 05: Data Storage

Storage behavior will be isolated in `project/src/storage.py`. It will:

- Resolve paths from `DATA_DIR`, defaulting safely to the project's `data/` directory.
- Save canonical raw CSV and Parquet artifacts.
- Reload both formats and reconcile row counts, columns, dates, and representative numeric values.
- Preserve `data/raw/` and `data/processed/` as distinct lifecycle layers.

The project README will gain a Data Storage section describing the folder structure, formats, path resolution, and reload process. The pipeline notebook will run acquisition, validation, storage, and reconciliation from top to bottom.

## Data Flow

```text
yfinance SPY response
        |
        v
schema/date/value validation
        |
        v
normalized daily DataFrame
        |
        +--> raw CSV
        |
        +--> raw Parquet
        |
        v
reload and reconciliation checks
        |
        v
verified handoff for Stage 06 preprocessing
```

## Failure Handling

The pipeline will fail clearly rather than manufacture success when:

- the live download is empty, unexpectedly small, or missing required fields;
- dates are invalid, duplicated, or not ordered after normalization;
- prices are nonnumeric, nonpositive, or wholly missing;
- an output file is missing or reload reconciliation differs;
- the environment or Parquet engine is unavailable;
- a notebook depends on hidden state or cannot execute from a clean kernel.

Network failures will be reported as network failures. Existing validated raw data may be reloaded for an explicitly offline run, but it will never be described as a fresh download.

## Verification Strategy

Implementation follows test-driven development for production Python functions:

1. Add a focused failing test.
2. Confirm it fails for the intended missing behavior.
3. Add the minimal implementation.
4. Confirm the targeted test and then the full suite pass.

Notebook and pipeline verification will include:

- structural validation with `nbformat`;
- clean top-to-bottom execution with `nbconvert` or `nbclient`;
- bounded live-download preflight before the durable pipeline run;
- raw-output existence and nonempty checks;
- schema, uniqueness, chronology, and numeric sanity checks;
- CSV/Parquet reconciliation;
- Git checks proving `.env` and `class_materials/` are ignored;
- final inspection of the repository tree and diff.

The protected invariant is: **a reported successful pipeline run must correspond to real SPY observations that passed validation and survived a verified storage round trip; command completion alone is insufficient.**

## Git and Change Discipline

The existing history will be preserved. Changes will be made in reviewable phases: structure migration, homework catch-up, Stage 03, Stage 04, Stage 05, and final verification. Secrets will not be printed or committed. Course materials will remain ignored. No Drive content will be edited.

## Completion Criteria

The catch-up is complete when:

- the repository follows the current three-area course structure;
- prior Stage 01–02 project work remains intact under `project/`;
- homework Stages 01–05 are present and executable;
- project Stages 03–05 meet the current Drive milestone requirements;
- the SPY pipeline executes from a clean kernel and produces validated, reconciled raw artifacts;
- all automated tests pass;
- the repository is ready to begin the August 17 preprocessing stage without structural or ingestion debt.
