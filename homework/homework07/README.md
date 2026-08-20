# Homework 07 — Outliers, Risk, and Assumptions

The submission notebook creates a seeded financial-style return dataset, compares parameterized IQR and Z-score flags, and measures how filtering and winsorization change descriptive and regression results. Reusable functions live in `src/outliers.py`; the sensitivity table is saved under `data/processed/`.

Outliers are not automatically errors. In market data they can represent genuine shocks and carry much of the risk signal, so the raw series is always preserved. Filtering and winsorization are presented as sensitivity cases, not as a universally correct cleaned dataset.

Run from this directory:

```bash
python -m jupyter nbconvert --execute --to notebook --inplace --ExecutePreprocessor.kernel_name=fe-course homework07_outliers-risk-assumptions_submission.ipynb
```
