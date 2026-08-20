# Stage 07 Outlier Policy

Daily SPY log returns are flagged with both the 1.5×IQR rule and a population Z-score threshold of 3.0. These are transparent diagnostics, not proof that an observation is erroneous.

The pipeline preserves every raw and processed observation. It reports raw, IQR-filtered, and 5th/95th-percentile winsorized summaries side by side so downstream conclusions can be checked for sensitivity. No treatment silently replaces the canonical return series.

Large returns can be authentic market shocks. Removing them may understate tail risk and produce an artificially stable volatility model. A treatment should therefore be selected only for a stated modeling reason, and core risk reporting should retain an untreated comparison.
