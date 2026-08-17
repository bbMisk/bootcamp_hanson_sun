# SPY 5-Day Volatility Risk Monitor

**Stage:** Problem Framing & Scoping (Stage 01)

## Problem Statement

Near-term equity-market risk can change faster than a portfolio review cycle. This project will build a reproducible workflow that estimates SPY's annualized realized volatility over the next five trading days using only information available at the forecast date. Success means producing a leakage-safe forecast that improves on a rolling-volatility baseline on a time-ordered holdout set and can be translated into a clear low/normal/high risk band.

The project supports risk review rather than return-direction trading. It will combine a numeric forecast, uncertainty-aware context, and a short action cue so a portfolio risk lead can decide whether current equity exposure deserves closer review or hedging attention.

## Stakeholder & User

The decision owner and primary user is a portfolio risk lead at a small asset manager. The output is reviewed on a daily or weekly risk cadence before exposure and hedging discussions. Other portfolio staff may consume the report, but the risk lead decides whether to escalate review.

## Useful Answer & Decision

The useful answer is predictive: a five-trading-day realized-volatility forecast, a historical risk band, and a concise monitoring note. A high-risk flag means “review exposure and hedging”; it is not a prediction of price direction or an automated trade instruction.

## Assumptions & Constraints

- SPY is a practical proxy for broad U.S. equity exposure.
- Adjusted daily prices are sufficient for this course-scale project; intraday data is out of scope.
- Every feature must be observable at the forecast date to avoid look-ahead bias.
- The first model must remain interpretable and comparable with a rolling-volatility baseline.
- The result supports human judgment and is not investment advice.

## Known Unknowns / Risks

- Market regimes can change, weakening historical relationships.
- Results depend on the return, target-window, and annualization conventions.
- Yahoo Finance availability, schemas, and adjusted history may change.
- A five-day forecast is uncertain and may not capture abrupt event risk.

## Lifecycle Mapping

- Decision definition → Problem Framing & Scoping (Stage 01) → README and stakeholder memo
- Reproducibility → Tooling Setup (Stage 02) → Python environment, config, and setup notebook
- Trustworthy history → Acquisition and Storage (Stages 04–05) → validated raw CSV/Parquet
- Leakage-safe modeling table → Preprocessing and Features → processed dataset and diagnostics
- Useful forecast → Modeling and Evaluation → baseline comparison, holdout metrics, and risk bands

## Repo Plan

The working implementation lives in the repository's `project/` directory with `data/`, `src/`, `notebooks/`, `docs/`, `reports/`, and `model/` subdirectories. Homework remains self-contained under `homework/`. Changes are committed by lifecycle stage.

## AI Assistance

AI assistance was used to reconcile the course requirements, draft and organize this submission, and run validation checks. Hanson Sun reviewed the scope, assumptions, and final artifact for accuracy and individual understanding.
