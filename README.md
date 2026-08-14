# SPY 5-Day Volatility Risk Monitor

**Stage:** Problem Framing & Scoping (Stage 01)

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

## Current Status

Stage 01 defines the project scope. Data ingestion, feature engineering, forecasting, and model evaluation have not yet been completed.

## AI Assistance

AI assistance was used to compare the course requirements, scaffold the repository design, and review the wording for clarity. Hanson Sun reviewed the project objective, stakeholder, assumptions, and final text for accuracy and individual understanding.
