# Homework 04 — Data Acquisition and Ingestion

The executed notebook downloads adjusted SPY daily prices with `yfinance`, scrapes the permitted Wikipedia S&P 500 constituents table with BeautifulSoup, validates both datasets, and saves timestamped raw CSV files under `data/raw/`.

No API secret is required for the chosen sources. `.env` remains local and ignored. AI assistance was used to implement and verify the workflow; Hanson Sun reviewed the sources, assumptions, and outputs.
