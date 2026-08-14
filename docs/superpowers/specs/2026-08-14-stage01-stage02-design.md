# Stage 01 + Stage 02 Project Design

**Date:** 2026-08-14
**Status:** Approved for specification; implementation pending Hanson review

## Purpose

Create a credible, achievable financial-engineering project foundation that satisfies both the Stage 01 problem-framing work and the Stage 02 tooling work. The project will build toward a five-trading-day SPY volatility forecast for a portfolio risk lead. At these stages, the repository will contain the framing, stakeholder artifact, environment, configuration, notebook check, and durable folder scaffold; data ingestion and modeling remain future lifecycle work.

## Source Requirements

The design combines four course documents:

- Stage 01 homework: scope the problem, identify a stakeholder and useful answer, document assumptions and risks, map goals to lifecycle deliverables, create a stakeholder artifact, and organize the repository.
- Stage 01 project milestone: adapt the framing into the persistent project README and `docs/` materials.
- Stage 02 homework: create a Python 3.11 environment, install `python-dotenv`, `numpy`, and `jupyter`, load a dummy key from `.env`, run a setup notebook, capture dependencies, and keep `.env` out of Git.
- Stage 02 project milestone: add the expanded project scaffold, including raw/processed data, reports, and model folders.

The course syllabus requires submitted work to reflect the student's own understanding and requires brief disclosure of AI assistance. Repository setup and requirement checking may be assisted, but Hanson must review and revise or explicitly confirm the project framing and stakeholder memo before submission.

## Project Framing

### Working title

**SPY 5-Day Volatility Risk Monitor**

### Problem

Equity exposure decisions are harder when near-term market risk changes quickly. The project will estimate the annualized realized volatility of SPY over the next five trading days using only information available at the forecast date. The forecast is intended to turn recent market behavior into a transparent risk signal, not to predict returns or automate trading.

### Primary stakeholder and decision

The primary stakeholder is a portfolio risk lead at a small asset manager. The stakeholder needs to decide whether current equity exposure remains within a normal risk regime or warrants review and possible hedging attention.

The useful answer will eventually contain:

1. A numeric five-day realized-volatility forecast.
2. A transparent low/normal/high risk band based on historical reference levels.
3. A concise action cue such as “continue monitoring” or “review exposure and hedging.”

The output will not prescribe a trade and will not claim that high forecast volatility implies positive or negative returns.

### Predictive target

The target is annualized realized volatility computed from the next five trading days of SPY log returns. All features must be lagged so the pipeline cannot use future information. The exact formula and annualization convention will be fixed and tested during the feature-engineering stage.

### Evaluation plan

Later lifecycle stages will use time-ordered training and holdout periods. A simple rolling historical-volatility forecast will be the baseline. Candidate models will be judged on forecast error, stability across market regimes, and whether they improve on the baseline without adding unjustified complexity. Random train/test splitting is out of scope because it would not represent forward forecasting.

### Assumptions and known risks

- SPY is treated as a practical proxy for broad U.S. equity-market exposure.
- Daily adjusted prices are adequate for a course-scale risk monitor; intraday volatility is out of scope.
- Historical relationships may change across market regimes.
- Volatility estimates depend on the return, window, and annualization definitions.
- A five-day forecast is uncertain and should support human review rather than trigger an automatic decision.
- Data-source revisions, missing trading days, and corporate-action adjustments must be handled explicitly in later stages.
- Implied volatility and options-chain analysis are future extensions, not core requirements.

## Deliverables and Repository Layout

Use a root-integrated layout because the Stage 01 and Stage 02 instructions describe these folders at repository root. Preserve the existing Homework 0 files and the existing `project/.gitkeep`; do not rewrite prior work.

```text
.
├── .env.example
├── .gitignore
├── README.md
├── data/
│   ├── raw/
│   │   └── starter_data.csv
│   └── processed/
│       └── .gitkeep
├── docs/
│   ├── stakeholder_memo.md
│   └── superpowers/specs/...
├── homework/homework0/python_tutorial.ipynb
├── model/.gitkeep
├── notebooks/00_project_setup.ipynb
├── project/.gitkeep
├── reports/.gitkeep
├── requirements.txt
└── src/
│   ├── __init__.py
│   └── config.py
```

The supplied A/B/C `starter_data.csv` is only Stage 02 tooling-test data. It must not be represented as financial portfolio data. Future market data will be added during the acquisition stage under `data/raw/` with source documentation.

## Public README Design

The README should serve an outside reader while retaining the rubric's required concepts. It will include:

- Project title and current lifecycle stage.
- Problem statement.
- Stakeholder and user.
- Useful answer and decision.
- Assumptions and constraints.
- Known unknowns and risks.
- Goal-to-stage-to-deliverable lifecycle mapping.
- Repository structure and update cadence.
- Setup instructions for the `fe-course` environment.
- Current status and clearly separated future work.
- A brief, factual AI-assistance disclosure.

It should not reproduce homework directions or imply that forecasting/data ingestion/modeling has already been completed.

## Stakeholder Memo Design

`docs/stakeholder_memo.md` will be a short client-style brief for the portfolio risk lead. It will state the decision, proposed signal, interpretation boundaries, assumptions, planned validation, and next milestone. It will avoid technical implementation detail except where needed to explain why the forecast can or cannot be trusted.

Hanson must review this memo and the README framing in his own words before the work is treated as submission-ready.

## Stage 02 Environment and Configuration

### Environment

- Environment name: `fe-course`
- Python version: 3.11
- Required packages: `python-dotenv`, `numpy`, `jupyter`
- Reproducibility artifact: `requirements.txt` generated from the environment after installation

An existing environment must not be deleted or overwritten. If `fe-course` already exists, verify its Python version and packages before changing it.

### Environment variables

Track `.env.example` with non-secret placeholders. Create a local, ignored `.env` containing:

```dotenv
API_KEY=dummy_key_123
DATA_DIR=./data
```

The dummy key is a course check, not a credential. The notebook may print only whether the key exists, never the value.

### Configuration module

`src/config.py` will expose the handout-required `load_env()` and `get_key()` functions. The implementation should be small and explicit. It should load the repository-root `.env` reliably and return the requested variable without embedding secrets or adding unnecessary configuration abstractions.

### Setup notebook

`notebooks/00_project_setup.ipynb` will execute top-to-bottom and contain:

1. Markdown title: `Environment & Config Check`.
2. Repository-path setup needed to import `src.config` when launched from the notebook directory.
3. An explicit `load_dotenv()` call, as required by the homework, pointed at the repository-root `.env`.
4. A `src.config` check that exercises the reusable configuration module.
5. Output `API_KEY present: True` when the dummy `.env` is configured.
6. A small deterministic NumPy array operation with visible output.

The notebook will not perform the future SPY analysis and will not display the dummy key.

## Testing and Verification

Implementation is complete only after all applicable checks pass:

1. Confirm the root Git worktree is clean before edits and inspect the final diff.
2. Verify `fe-course` reports Python 3.11 and imports the three required packages.
3. Verify configuration loading with an isolated inline check; never depend on a real secret or add a permanent test suite solely for this setup assignment.
4. Execute `00_project_setup.ipynb` from a clean kernel and confirm its expected outputs.
5. Confirm `.env` is ignored and absent from `git ls-files` and the staged diff.
6. Confirm the required directory tree and files exist.
7. Confirm README and memo describe planned work honestly and include the AI-use disclosure.
8. Push only after local verification and confirm the remote branch matches the intended commits.

Keep repository code to the smallest assignment-complete surface: the required configuration module and notebook only. Use bounded shell or inline Python checks instead of committing extra testing utilities.

## Git and External Actions

Preserve existing history. Planned commits are:

1. `Initial commit — project framing` for the Stage 01 README, memo, and framing scaffold. The exact wording comes from the homework instructions even though the repository already has earlier Homework 0 commits.
2. A separate focused Stage 02 tooling commit for the environment, config, notebook, dependency file, tests, and remaining scaffold.

The repository is public, but collaborator access is a separate action. The syllabus identifies Prof. Jason Yarmish and `yarmish@nyu.edu` but provides no verified GitHub username. Do not guess from ambiguous GitHub profiles. Ask the instructor for the exact handle before inviting anyone.

Do not submit the repository URL to Google Classroom or another course channel without Hanson's explicit approval at the time of submission.

## Success Criteria for These Stages

- Every required Stage 01 and Stage 02 homework and project-milestone artifact is present.
- The public README is understandable to an outside reader and accurately states the current project stage.
- The project question, stakeholder, forecast target, and decision are specific and mutually consistent.
- The setup notebook runs from top to bottom and shows the required environment checks.
- No secret or `.env` file is tracked or printed.
- Existing Homework 0 work remains intact.
- Hanson has reviewed the framing and memo for individual understanding and course-policy compliance before submission.
