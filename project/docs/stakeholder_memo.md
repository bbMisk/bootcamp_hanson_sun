# Stakeholder Memo: SPY 5-Day Volatility Risk Monitor

**To:** Portfolio Risk Lead
**From:** Hanson Sun
**Subject:** Framing a near-term equity volatility warning signal

## Decision

The proposed monitor is intended to help decide whether current U.S. equity exposure remains in a normal risk regime or deserves closer review and possible hedging attention.

## Proposed Answer

The project will estimate annualized realized volatility for SPY over the next five trading days. The stakeholder view will pair the numeric forecast with a historically defined low, normal, or high risk band and a concise review cue.

## Interpretation Boundary

A high forecast means larger price movements may be more likely; it does not predict their direction. **Not a trading signal:** the result will support a human risk review and will not automatically recommend or execute a position.

## Validation Standard

The eventual forecast will be evaluated on a time-ordered holdout period and compared with a simple rolling historical-volatility baseline. A more complex model will be retained only if it improves forecast error and remains stable enough to explain.

## Assumptions and Risks

- SPY is being used as a proxy for broad U.S. equity exposure.
- Daily adjusted prices omit intraday volatility information.
- Market-regime changes can weaken patterns learned from historical data.
- Window and annualization choices can materially affect reported volatility.
- Missing or revised data must be detected before the output is trusted.

## Next Milestone

Establish the reproducible Python environment, configuration pattern, and project folders needed for data acquisition and subsequent analysis.

## AI Assistance Disclosure

Hanson Sun authored the decision framing, scope, assumptions, and final wording. AI assistance was used to check the assignment requirements and suggest improvements to the document structure.
