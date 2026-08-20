# Homework 06 — Data Preprocessing

The submission notebook builds a seeded sample dataset, applies reusable cleaning functions from `src/cleaning.py`, and writes the reproducible result to `data/processed/sample_data_cleaned.csv`.

## Decisions and assumptions

- Median imputation is limited to numeric analysis columns and assumes the observed values are informative enough for a defensible center. It is robust to isolated extremes but can conceal structured missingness.
- Columns with more than 50% missing values are dropped. The threshold is explicit so the choice can be rerun and challenged.
- `age`, `income`, and `score` are min-max normalized after imputation. Constant columns map to zero rather than dividing by zero.
- Identifier-like and categorical fields are retained without numeric scaling.
- Every transformation returns a copy, preserving the raw input.

Run from this directory:

```bash
python -m jupyter nbconvert --execute --to notebook --inplace --ExecutePreprocessor.kernel_name=fe-course stage06_data-preprocessing_homework-submission.ipynb
```
