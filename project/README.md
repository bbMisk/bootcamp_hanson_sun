# SPY 5-Day Volatility Risk Monitor

**Stage:** Outliers, Risk, and Assumptions (Stage 07)

## Problem Statement

Near-term equity-market risk can change faster than a portfolio review cycle. This project will build a reproducible workflow that estimates the annualized realized volatility of SPY over the next five trading days using only information available at the forecast date. The goal is to turn recent market behavior into a transparent risk-monitoring signal; it is not to predict return direction or automate a trade.

## Stakeholder & User

The primary stakeholder is a portfolio risk lead at a small asset manager. The user needs to decide whether current equity exposure remains within a normal risk regime or warrants closer review and possible hedging attention. The result must therefore be timely, interpretable, and explicit about uncertainty.

## Useful Answer & Decision

The intended predictive output is a numeric five-day realized-volatility forecast, a historically defined low/normal/high risk band, and a short action cue. A high-risk flag means “review exposure and hedging”; it does not indicate whether SPY will rise or fall and is not a trading recommendation.

## Assumptions & Constraints

- SPY is a practical proxy for broad U.S. equity exposure.
- Daily adjusted prices are sufficient for this course-scale project; intraday data is out of scope.
- The five-day target will be computed from future log returns and annualized with a documented convention.
- Every feature must be available at the forecast date to prevent look-ahead bias.
- The first usable model should remain simple enough to compare with a rolling-volatility baseline.

## Known Unknowns / Risks

- Market regimes change, so historical relationships may not persist.
- Results will depend on the return, window, and annualization definitions.
- Missing trading days and adjusted-price conventions can affect the target.
- A short-horizon forecast is uncertain and should support human review rather than trigger an automatic decision.
- Implied volatility and options-chain analysis are possible extensions but are outside the core scope.

## Lifecycle Mapping

| Goal | Lifecycle stage | Deliverable |
| --- | --- | --- |
| Define the decision and forecast target | Problem Framing & Scoping | README and stakeholder memo |
| Make the work reproducible | Tooling Setup | Python environment, config module, setup notebook |
| Build a trustworthy price history | Data Acquisition, Storage, and Preprocessing | Versioned raw/processed data and validation checks |
| Create leakage-safe predictors | EDA and Feature Engineering | Time-ordered features and diagnostic notebook |
| Forecast five-day volatility | Modeling | Baseline and candidate time-series/regression models |
| Judge usefulness and communicate uncertainty | Evaluation & Risk Communication | Holdout metrics, risk bands, assumptions, and stakeholder report |

## Repo Plan

- `data/` — raw and processed project data as the lifecycle advances.
- `src/` — reusable configuration, ingestion, feature, and modeling code.
- `notebooks/` — numbered, executable analysis notebooks.
- `docs/` — stakeholder-facing framing and decision documents.
- `reports/` — generated reporting artifacts in future stages.
- `model/` — saved model artifacts in future stages.
- `homework/` — standalone course homework, including Homework 0.

Changes will be committed by lifecycle stage so each project contribution can be reviewed independently.

## Environment Setup

```bash
conda create -n fe-course python=3.11 -y
conda activate fe-course
python -m pip install -r requirements.txt
cp .env.example .env
jupyter notebook
```

For the Stage 02 configuration check, set `API_KEY=dummy_key_123` in the local `.env` as instructed by the handout. Never commit `.env` or place a real secret in the repository. Run `notebooks/00_project_setup.ipynb` from top to bottom; the expected safe check is `API_KEY present: True`.

## Current Status

Stages 01–07 are implemented. The repository now includes framing, a reproducible Python 3.11 environment, reusable Python/pandas utilities, validated SPY acquisition, reconciled CSV/Parquet storage, a deterministic preprocessing contract, and outlier sensitivity analysis. EDA and target construction remain the next lifecycle work.

## Data Acquisition

`notebooks/project_pipeline.ipynb` uses `yfinance` to request SPY daily data from 2015-01-01 through the latest available trading day. `auto_adjust=True` produces adjusted OHLC prices, and the pipeline keeps the stable contract `date`, `open`, `high`, `low`, `close`, `volume`.

Before storage, reusable validation requires at least 20 rows, exact columns, ordered unique dates, nonmissing positive OHLC prices, and nonnegative volume. The notebook reports the source, request parameters, row count, date range, missing values, duplicates, and a bounded preview.

## Data Storage

- `data/raw/` holds the immutable acquisition snapshot in CSV and Parquet.
- `data/processed/` is reserved for Stage 06 cleaning and feature-ready outputs.
- `DATA_DIR` in `.env` controls the data root; relative values resolve inside `project/`.
- CSV is portable and human-readable. Parquet preserves types efficiently for analysis.
- `src/storage.py` reloads both formats and reconciles every row and column against the validated source frame.

Run the full pipeline from `project/`:

```bash
python -m jupyter nbconvert --execute --to notebook --inplace --ExecutePreprocessor.kernel_name=fe-course notebooks/project_pipeline.ipynb
```

Yahoo Finance is suitable for this course workflow but is not a contractual institutional feed. Availability, schemas, adjustments, and historical values can change, so the acquisition and reconciliation checks must be rerun before relying on a refreshed snapshot.

## Data Preprocessing

- `src/cleaning.py` enforces the OHLCV schema, parses dates and numerics, sorts and deduplicates observations, rejects invalid prices or volume, and derives close-to-close log returns.
- Missing volume is median-imputed only after the choice is explicit; rows missing required prices are dropped because prices cannot be reconstructed safely from the available fields.
- `data/processed/spy_daily_clean.csv` and `.parquet` are regenerated by the cumulative pipeline and retain one ordered observation per date.

## Outlier Sensitivity

- `src/outliers.py` provides parameterized IQR and Z-score detection, winsorization, flags, and side-by-side sensitivity summaries.
- `reports/outlier_sensitivity.csv` compares untreated, IQR-filtered, and winsorized log returns.
- `reports/outlier_log_return_boxplot.png` visualizes the distribution without altering the canonical series.
- The policy and modeling risk are documented in `docs/outliers.md`; market extremes may be real information, so no outlier treatment silently replaces the raw or processed data.

## Canonical Course Materials

The requirements for this repository were reconciled on 2026-08-20 against the signed-in NYU Google Drive folder `Documents(BootCamp)(FRE5040)(Fall 2026)`. Local reference copies of the Stage 01–07 homework sheets, starter notebooks, project-milestone instructions, and Stage 06–10a readings are stored under the ignored `class_materials/` directory and are not committed.

## AI Assistance

AI assistance was used to compare the course requirements, draft the project documentation, and create and verify the tooling setup. Hanson Sun reviewed the project objective, stakeholder, assumptions, and final text for accuracy and individual understanding.
