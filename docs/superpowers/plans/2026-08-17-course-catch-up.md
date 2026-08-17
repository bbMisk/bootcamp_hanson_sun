# FRE 5040 Course Catch-Up Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Align the repository with the current FRE 5040 Drive, complete homework and project Stages 01–05, and produce a verified SPY ingestion/storage pipeline ready for preprocessing.

**Architecture:** The repository has three principal areas: ignored `class_materials/`, self-contained `homework/`, and the single ongoing implementation in `project/`. Production Python separates utilities, acquisition, and storage; notebooks call those tested modules and execute from a clean kernel.

**Tech Stack:** Python 3.11, pandas, NumPy, yfinance, pyarrow, python-dotenv, pytest, nbformat, nbclient/Jupyter.

## Global Constraints

- The current FRE 5040 Google Drive is canonical when older local plans conflict.
- Preserve existing Git history and completed Stage 01–02 content.
- `class_materials/` and `.env` must remain ignored and untracked.
- All ongoing project paths are inside `project/`.
- A successful pipeline must contain real SPY observations that pass validation and a storage round trip; no synthetic fallback may be reported as live data.
- Homework artifacts must disclose AI assistance factually where the course artifact calls for it.
- Production functions follow red-green-refactor test-driven development.
- Every notebook must execute top-to-bottom from a clean kernel.

---

### Task 1: Migrate the Repository to the Canonical Course Layout

**Files:**
- Move: `.env.example` to `project/.env.example`
- Move: `README.md` to `project/README.md`
- Move: `requirements.txt` to `project/requirements.txt`
- Move: `data/` to `project/data/`
- Move: `notebooks/` to `project/notebooks/`
- Move: `src/` to `project/src/`
- Move: `model/` to `project/model/`
- Move: `reports/` to `project/reports/`
- Move: `docs/stakeholder_memo.md` to `project/docs/stakeholder_memo.md`
- Move: `docs/superpowers/` to `project/docs/superpowers/`
- Modify: `.gitignore`

**Interfaces:**
- Consumes: the existing Stage 01–02 repository.
- Produces: a single project root at `project/`, plus ignored `class_materials/` and preserved `homework/`.

- [ ] **Step 1: Record the pre-migration inventory**

Run:

```bash
git status --short
git ls-files | sort
```

Expected: clean worktree; `.env` is absent from tracked files.

- [ ] **Step 2: Move the existing project artifacts without copying them**

Use patch-based file moves so history remains legible. Remove `project/.gitkeep` once real project files exist.

- [ ] **Step 3: Update `.gitignore`**

Ensure these rules exist:

```gitignore
class_materials/
.env
project/.env
__pycache__/
*.pyc
.ipynb_checkpoints/
.venv/
venv/
.DS_Store
tmp/
```

- [ ] **Step 4: Update relocated paths**

Set `project/src/config.py` to resolve `project/.env`, and update notebook/README references so commands run from `project/`.

- [ ] **Step 5: Verify the migration**

Run:

```bash
test -f project/README.md
test -f project/src/config.py
test -f project/notebooks/00_project_setup.ipynb
test -d homework/homework0
git check-ignore -q .env
git check-ignore -q class_materials/example.txt
git diff --check
```

Expected: all commands exit 0.

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "refactor: align repository with course layout"
```

---

### Task 2: Intake the Canonical Stage 01–05 Course Materials

**Files:**
- Create ignored files under: `class_materials/homework/`
- Create ignored files under: `class_materials/project_milestones/`
- Create ignored file: `class_materials/course_git-repository-structure.pdf`

**Interfaces:**
- Consumes: the signed-in canonical Google Drive.
- Produces: local, ignored reference copies used to create the homework artifacts and verify project requirements.

- [ ] **Step 1: Download the current homework folder contents**

Download the Stage 01–05 homework sheets and starter notebooks from Drive into `class_materials/homework/`. Retain the Drive filenames exactly.

- [ ] **Step 2: Download the current project milestone PDFs and structure PDF**

Store the five milestone PDFs under `class_materials/project_milestones/` and the repository-structure PDF at the class-materials root.

- [ ] **Step 3: Verify intake completeness**

Run:

```bash
find class_materials/homework -maxdepth 1 -type f | sort
find class_materials/project_milestones -maxdepth 1 -type f | sort
git check-ignore -v class_materials/homework/*
```

Expected: homework sheets/starters for Stages 01–05, five project PDFs, and every file ignored.

- [ ] **Step 4: Record a non-secret manifest in the project README**

Document the canonical Drive folder name and retrieval date without committing the downloaded course files.

---

### Task 3: Implement and Test Stage 03 Reusable Utilities

**Files:**
- Create: `project/tests/test_utils.py`
- Create: `project/src/utils.py`
- Create: `project/src/__init__.py` if absent

**Interfaces:**
- Produces: `clean_column_name(name: str) -> str`, `clean_columns(frame: pandas.DataFrame) -> pandas.DataFrame`, and `parse_date_column(frame: pandas.DataFrame, column: str) -> pandas.DataFrame`.

- [ ] **Step 1: Write failing utility tests**

```python
import pandas as pd
import pytest

from src.utils import clean_column_name, clean_columns, parse_date_column


def test_clean_column_name_normalizes_spacing_and_symbols():
    assert clean_column_name(" Adj Close ($) ") == "adj_close"


def test_clean_columns_returns_copy_with_normalized_columns():
    source = pd.DataFrame({"Trade Date": ["2026-01-02"], "Adj Close": [100.0]})
    result = clean_columns(source)
    assert result.columns.tolist() == ["trade_date", "adj_close"]
    assert source.columns.tolist() == ["Trade Date", "Adj Close"]


def test_parse_date_column_parses_and_sorts_dates():
    source = pd.DataFrame({"date": ["2026-01-03", "2026-01-02"]})
    result = parse_date_column(source, "date")
    assert result["date"].dt.strftime("%Y-%m-%d").tolist() == ["2026-01-02", "2026-01-03"]


def test_parse_date_column_rejects_invalid_values():
    with pytest.raises(ValueError, match="invalid dates"):
        parse_date_column(pd.DataFrame({"date": ["not-a-date"]}), "date")
```

- [ ] **Step 2: Run tests and confirm the intended failure**

Run:

```bash
(cd project && python -m pytest tests/test_utils.py -v)
```

Expected: collection fails because `src.utils` does not exist.

- [ ] **Step 3: Implement the minimal utilities**

```python
import re

import pandas as pd


def clean_column_name(name: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "_", str(name).strip().lower())
    return normalized.strip("_")


def clean_columns(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result.columns = [clean_column_name(column) for column in result.columns]
    return result


def parse_date_column(frame: pd.DataFrame, column: str) -> pd.DataFrame:
    result = frame.copy()
    parsed = pd.to_datetime(result[column], errors="coerce")
    if parsed.isna().any():
        raise ValueError(f"{column} contains invalid dates")
    result[column] = parsed
    return result.sort_values(column).reset_index(drop=True)
```

- [ ] **Step 4: Run the targeted and full suites**

```bash
(cd project && python -m pytest tests/test_utils.py -v)
(cd project && python -m pytest -v)
```

Expected: all tests pass.

- [ ] **Step 5: Commit**

```bash
git add project/src project/tests
git commit -m "feat: add Stage 03 data utilities"
```

---

### Task 4: Build and Execute the Stage 03 Summary Notebook

**Files:**
- Create: `project/notebooks/python_fundamentals_summary.ipynb`

**Interfaces:**
- Consumes: `clean_columns` and `parse_date_column` from Task 3.
- Produces: an executed tutorial notebook demonstrating Python, NumPy, pandas, and reusable project utilities.

- [ ] **Step 1: Scaffold the notebook with `nbformat`**

Create cells in this order:

1. `# Python Fundamentals Summary` and `## Goal`.
2. Path-safe setup that changes from `project/notebooks` to `project` and adds it to `sys.path`.
3. `## Python and NumPy` with deterministic list and array operations.
4. `## pandas` with a small dated price DataFrame.
5. `## Reusable Utilities` importing and exercising Task 3 functions.
6. `## Checks` with assertions on normalized columns, sorted dates, and row count.
7. `## Next Steps` explaining acquisition/preprocessing reuse.

- [ ] **Step 2: Validate notebook structure**

```bash
python -m json.tool project/notebooks/python_fundamentals_summary.ipynb >/dev/null
```

- [ ] **Step 3: Execute from a clean kernel**

```bash
(cd project && python -m jupyter nbconvert --execute --to notebook --inplace notebooks/python_fundamentals_summary.ipynb)
```

Expected: exit 0 with visible bounded outputs and no traceback.

- [ ] **Step 4: Commit**

```bash
git add project/notebooks/python_fundamentals_summary.ipynb
git commit -m "feat: complete Stage 03 project notebook"
```

---

### Task 5: Implement and Test Stage 04 SPY Acquisition

**Files:**
- Create: `project/tests/test_ingestion.py`
- Create: `project/src/ingestion.py`
- Modify: `project/requirements.txt`

**Interfaces:**
- Produces: `normalize_yfinance_frame(frame: pandas.DataFrame) -> pandas.DataFrame`, `validate_market_data(frame: pandas.DataFrame, min_rows: int = 20) -> None`, and `download_daily_prices(symbol: str, start: str, end: str | None = None) -> pandas.DataFrame`.
- Data contract columns: `date`, `open`, `high`, `low`, `close`, `volume`.

- [ ] **Step 1: Write failing normalization and validation tests**

```python
import pandas as pd
import pytest

from src.ingestion import normalize_yfinance_frame, validate_market_data


def sample_frame(rows: int = 25) -> pd.DataFrame:
    dates = pd.date_range("2026-01-01", periods=rows, freq="B")
    return pd.DataFrame(
        {
            "Open": range(100, 100 + rows),
            "High": range(101, 101 + rows),
            "Low": range(99, 99 + rows),
            "Close": range(100, 100 + rows),
            "Volume": [1_000] * rows,
        },
        index=dates,
    )


def test_normalize_yfinance_frame_creates_stable_schema():
    result = normalize_yfinance_frame(sample_frame())
    assert result.columns.tolist() == ["date", "open", "high", "low", "close", "volume"]
    assert result["date"].is_monotonic_increasing


def test_validate_market_data_accepts_valid_frame():
    validate_market_data(normalize_yfinance_frame(sample_frame()))


def test_validate_market_data_rejects_small_response():
    with pytest.raises(ValueError, match="at least 20 rows"):
        validate_market_data(normalize_yfinance_frame(sample_frame(3)))


def test_validate_market_data_rejects_duplicate_dates():
    frame = normalize_yfinance_frame(sample_frame())
    frame.loc[1, "date"] = frame.loc[0, "date"]
    with pytest.raises(ValueError, match="duplicate dates"):
        validate_market_data(frame)


def test_validate_market_data_rejects_nonpositive_prices():
    frame = normalize_yfinance_frame(sample_frame())
    frame.loc[0, "close"] = 0
    with pytest.raises(ValueError, match="positive"):
        validate_market_data(frame)
```

- [ ] **Step 2: Run tests and confirm the intended failure**

```bash
(cd project && python -m pytest tests/test_ingestion.py -v)
```

Expected: collection fails because `src.ingestion` does not exist.

- [ ] **Step 3: Implement normalization and validation**

Implementation requirements:

```python
REQUIRED_COLUMNS = ["date", "open", "high", "low", "close", "volume"]
PRICE_COLUMNS = ["open", "high", "low", "close"]
```

`normalize_yfinance_frame` must flatten a possible ticker-level `MultiIndex`, reset the date index, normalize names, select the required columns, parse dates, and reset row indices. `validate_market_data` must enforce the schema, minimum row count, unique ordered dates, non-null numeric price values, positive prices, and nonnegative volume.

- [ ] **Step 4: Run tests and confirm green**

```bash
(cd project && python -m pytest tests/test_ingestion.py -v)
```

- [ ] **Step 5: Add the network boundary**

Implement:

```python
def download_daily_prices(symbol: str, start: str, end: str | None = None) -> pd.DataFrame:
    raw = yf.download(
        symbol,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        actions=False,
        threads=False,
    )
    normalized = normalize_yfinance_frame(raw)
    validate_market_data(normalized)
    return normalized
```

Add `yfinance` to `project/requirements.txt`.

- [ ] **Step 6: Run the full suite**

```bash
(cd project && python -m pytest -v)
```

- [ ] **Step 7: Run a bounded live preflight**

```bash
(cd project && python -c "from src.ingestion import download_daily_prices; x=download_daily_prices('SPY','2026-01-01'); print(len(x), x.date.min().date(), x.date.max().date(), x.columns.tolist())")
```

Expected: at least 20 real rows, a plausible 2026 date range, and the stable six-column schema.

- [ ] **Step 8: Commit**

```bash
git add project/src/ingestion.py project/tests/test_ingestion.py project/requirements.txt
git commit -m "feat: add validated SPY ingestion"
```

---

### Task 6: Implement and Test Stage 05 Storage

**Files:**
- Create: `project/tests/test_storage.py`
- Create: `project/src/storage.py`
- Modify: `project/requirements.txt`

**Interfaces:**
- Produces: `resolve_data_dir(project_root: pathlib.Path) -> pathlib.Path`, `save_raw_snapshot(frame: pandas.DataFrame, symbol: str, data_dir: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path]`, and `verify_storage_round_trip(source: pandas.DataFrame, csv_path: pathlib.Path, parquet_path: pathlib.Path) -> None`.

- [ ] **Step 1: Write failing storage tests**

```python
from pathlib import Path

import pandas as pd
import pytest

from src.storage import resolve_data_dir, save_raw_snapshot, verify_storage_round_trip


def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=3, freq="B"),
            "open": [100.0, 101.0, 102.0],
            "high": [101.0, 102.0, 103.0],
            "low": [99.0, 100.0, 101.0],
            "close": [100.5, 101.5, 102.5],
            "volume": [1000, 1100, 1200],
        }
    )


def test_resolve_data_dir_defaults_inside_project(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.delenv("DATA_DIR", raising=False)
    assert resolve_data_dir(tmp_path) == tmp_path / "data"


def test_resolve_data_dir_uses_environment_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATA_DIR", "custom_data")
    assert resolve_data_dir(tmp_path) == tmp_path / "custom_data"


def test_save_and_verify_round_trip(tmp_path: Path):
    csv_path, parquet_path = save_raw_snapshot(sample_frame(), "SPY", tmp_path)
    assert csv_path.name == "spy_daily.csv"
    assert parquet_path.name == "spy_daily.parquet"
    verify_storage_round_trip(sample_frame(), csv_path, parquet_path)
```

- [ ] **Step 2: Run tests and confirm the intended failure**

```bash
(cd project && python -m pytest tests/test_storage.py -v)
```

Expected: collection fails because `src.storage` does not exist.

- [ ] **Step 3: Implement minimal path resolution and storage**

`resolve_data_dir` resolves relative `DATA_DIR` values under `project_root`. `save_raw_snapshot` creates the target directory and writes `symbol.lower() + '_daily.csv'` and `.parquet` without the DataFrame index.

- [ ] **Step 4: Implement strict reconciliation**

`verify_storage_round_trip` reloads CSV with parsed dates and Parquet, normalizes column order, and uses `pandas.testing.assert_frame_equal(..., check_dtype=False, rtol=1e-10, atol=1e-12)` against the source for both formats. Missing files must raise `FileNotFoundError`.

- [ ] **Step 5: Add Parquet support and run tests**

Add `pyarrow` to `project/requirements.txt`, then run:

```bash
(cd project && python -m pytest tests/test_storage.py -v)
(cd project && python -m pytest -v)
```

Expected: all tests pass.

- [ ] **Step 6: Commit**

```bash
git add project/src/storage.py project/tests/test_storage.py project/requirements.txt
git commit -m "feat: add reproducible raw-data storage"
```

---

### Task 7: Build and Execute the Stage 04–05 Project Pipeline Notebook

**Files:**
- Create: `project/notebooks/project_pipeline.ipynb`
- Modify: `project/README.md`
- Modify: `project/.env.example`

**Interfaces:**
- Consumes: `download_daily_prices`, `resolve_data_dir`, `save_raw_snapshot`, and `verify_storage_round_trip`.
- Produces: executed `project/notebooks/project_pipeline.ipynb`, `project/data/raw/spy_daily.csv`, and `project/data/raw/spy_daily.parquet`.

- [ ] **Step 1: Add visible pipeline parameters and setup**

Start the notebook with the canonical path-safe cell from the Stage 04 milestone. Define:

```python
SYMBOL = "SPY"
START_DATE = "2015-01-01"
END_DATE = None
```

- [ ] **Step 2: Add focused acquisition and validation cells**

Download with `download_daily_prices`, then display only row count, date range, columns, missing-value counts, duplicate-date count, and a five-row preview.

- [ ] **Step 3: Add storage and reconciliation cells**

Resolve the project data directory, save into `data/raw/`, run `verify_storage_round_trip`, and print the two paths and their byte sizes.

- [ ] **Step 4: Update project documentation**

Add to `project/README.md`:

- current status through Stage 05;
- source (`yfinance`, SPY, daily auto-adjusted prices);
- acquisition parameters and validations;
- Data Storage folder structure, formats, environment-driven paths, and reload behavior;
- known limitations of Yahoo Finance and adjusted daily data;
- exact pipeline execution command.

Set `DATA_DIR=./data` in `project/.env.example`.

- [ ] **Step 5: Execute the notebook top-to-bottom**

```bash
(cd project && python -m jupyter nbconvert --execute --to notebook --inplace notebooks/project_pipeline.ipynb)
```

Expected: exit 0; real SPY rows downloaded; CSV/Parquet outputs created; reconciliation confirmation visible.

- [ ] **Step 6: Run independent post-run QC**

```bash
(cd project && python -c "import pandas as pd; x=pd.read_csv('data/raw/spy_daily.csv',parse_dates=['date']); assert len(x)>1000; assert x.date.is_monotonic_increasing; assert x.date.is_unique; assert (x[['open','high','low','close']]>0).all().all(); print(len(x), x.date.min().date(), x.date.max().date())")
```

- [ ] **Step 7: Commit**

```bash
git add project/notebooks/project_pipeline.ipynb project/data/raw/spy_daily.csv project/data/raw/spy_daily.parquet project/README.md project/.env.example
git commit -m "feat: complete Stage 04 and Stage 05 pipeline"
```

---

### Task 8: Complete Homework Stages 01–05

**Files:**
- Create: `homework/homework01/`
- Create: `homework/homework02/`
- Create: `homework/homework03/`
- Create: `homework/homework04/`
- Create: `homework/homework05/`

**Interfaces:**
- Consumes: the exact canonical starter notebooks and homework sheets downloaded in Task 2.
- Produces: five self-contained, executed homework workspaces that preserve starter intent and satisfy their current sheets.

- [ ] **Step 1: Copy each starter notebook into its matching homework directory**

Use the original filename without `-starter` for the completed working copy. Preserve any non-empty starter prompts and cell order.

- [ ] **Step 2: Complete Stage 01**

Answer every framing prompt using the SPY 5-Day Volatility Risk Monitor: stakeholder, decision, useful answer, assumptions, risks, scope boundary, lifecycle mapping, and AI disclosure. Assertions or a final checklist must confirm no required prompt is blank.

- [ ] **Step 3: Complete Stage 02**

Use a local ignored `.env`, `python-dotenv`, NumPy, and the environment/config checks required by the sheet. Never print a key value. The notebook must visibly show key presence, Python version, package imports, and a deterministic NumPy result.

- [ ] **Step 4: Complete Stage 03**

Demonstrate Python, NumPy, pandas, column cleaning, date parsing, and reusable function behavior with toy data. Include assertions for expected columns, values, and dates.

- [ ] **Step 5: Complete Stage 04**

Perform a bounded `yfinance` API pull plus the permitted public-table exercise required by the canonical sheet. Validate HTTP/data success, schemas, row counts, nulls, and duplicates; save outputs inside `homework/homework04/data/`.

- [ ] **Step 6: Complete Stage 05**

Save and reload CSV and Parquet data, reconcile results, and demonstrate an environment-driven data path. Include assertions for file existence, row/column equality, and representative values.

- [ ] **Step 7: Execute all five notebooks from clean kernels**

For each notebook:

```bash
python -m jupyter nbconvert --execute --to notebook --inplace <path-to-notebook>
```

Expected: every command exits 0 with no traceback.

- [ ] **Step 8: Commit**

```bash
git add homework/homework01 homework/homework02 homework/homework03 homework/homework04 homework/homework05
git commit -m "feat: complete homework Stages 01 through 05"
```

---

### Task 9: Final Trusted Verification and Preprocessing Handoff

**Files:**
- Modify only if verification reveals a defect in an in-scope artifact.

**Interfaces:**
- Consumes: all previous tasks.
- Produces: a trust verdict and a repository ready for Stage 06 preprocessing.

- [ ] **Step 1: Verify the repository tree and ignore rules**

```bash
find project homework -maxdepth 3 -type f | sort
git check-ignore -q .env
git check-ignore -q project/.env
git check-ignore -q class_materials/example.txt
test -z "$(git ls-files | grep -E '(^|/)\.env$|^class_materials/' || true)"
```

- [ ] **Step 2: Run the full automated suite**

```bash
(cd project && python -m pytest -v)
```

Expected: all tests pass without warnings caused by project code.

- [ ] **Step 3: Validate every notebook artifact**

Use `nbformat.read(..., as_version=4)` on every tracked `.ipynb`; assert each code cell has a non-null execution count after execution and no output with `output_type == 'error'`.

- [ ] **Step 4: Reconcile raw artifacts independently**

Reload CSV and Parquet outside the notebook, compare shape, columns, dates, and values, and report byte sizes and SHA-256 hashes.

- [ ] **Step 5: Inspect Git state and final diff**

```bash
git status --short
git log --oneline --decorate -10
git diff --check HEAD~1..HEAD
```

- [ ] **Step 6: State the verdict**

Report `Verdict: Trusted` only if the tests, notebooks, real-data checks, storage reconciliation, ignore rules, and Git inspection all pass. Otherwise report `Verdict: Not trusted` or `Verdict: Unknown` with the exact missing evidence.
