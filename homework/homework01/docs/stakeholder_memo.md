# Stakeholder Brief — SPY 5-Day Volatility Risk Monitor

**Audience:** Portfolio risk lead  
**Cadence:** Daily data refresh; weekly risk review  
**Decision supported:** Decide whether equity exposure warrants closer review or hedging attention.

## Context

Recent market behavior can imply a different near-term risk regime before the next formal portfolio review. The stakeholder needs an interpretable signal that summarizes expected five-day realized volatility without pretending to predict return direction.

## What You Will Receive

- A numeric five-trading-day annualized realized-volatility forecast.
- A historically defined low, normal, or high risk band.
- A short plain-language action cue and stated assumptions.
- Holdout evidence comparing the forecast with a simple rolling-volatility baseline.

## Decision Boundary

A high-risk signal prompts human review. It never places a trade, prescribes a hedge, or represents investment advice.

## Assumptions and Risks

- SPY proxies broad U.S. equity exposure.
- Adjusted daily prices are adequate for the first version.
- Regime shifts and abrupt events can reduce forecast usefulness.
- All evaluation must be time ordered and leakage safe.
