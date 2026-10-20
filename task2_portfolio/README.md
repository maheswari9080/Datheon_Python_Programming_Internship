# Task 02: Stock Portfolio Performance Tracker

Part of the **Datheon Python Internship Project Suite**.

## Overview
A financial tracking and valuation utility built in pure Python. The tool supports multi-asset holdings, evaluates capital investment, computes current market values, and tracks dollar and percentage gains/losses. Summaries are exported in standard RFC 4180 CSV format.

> **EDUCATIONAL DISCLAIMER**: This application is strictly an educational tool designed to demonstrate algorithmic valuation and file persistence. It does not provide investment advice or real-time trading feeds.

---

## Financial Calculation Formulas
For any position with Purchase Price ($P$), Current Price ($C$), and Share Quantity ($Q$):
- **Invested Capital**: $P \times Q$
- **Current Market Value**: $C \times Q$ (if $C$ is known)
- **Absolute Gain / Loss**: $(C - P) \times Q$
- **Percentage Gain / Loss**: $\frac{C - P}{P} \times 100$

If a holding lacks a current quote, its valuation and gain/loss are marked `N/A`, and portfolio-level totals explicitly indicate a partial valuation.

---

## Market Data & Provider Architecture
The included `data/constituents.csv` file contains S&P 500 company constituent records, not live prices. Pricing is provider-independent:
1. **Offline Sample Feed**: `sample_prices.json` provides verified reference prices.
2. **Manual Entry**: Users can input current prices directly.
3. **Optional Live Provider**: `yfinance` is supported when installed, but is never required.

---

## CSV Export Specification
Exported to `portfolio_summary.csv` with the following columns:
- `timestamp`: UTC ISO 8601 timestamp
- `ticker`: Stock symbol
- `company`: Resolved corporate name
- `quantity`: Number of shares held
- `buy_price`: Initial cost per share
- `current_price`: Market price used in valuation
- `invested_value`: Total cost basis
- `market_value`: Current total position value
- `gain_loss`: Dollar gain or loss
- `gain_loss_percent`: Percentage return
- `price_source`: Explicit source label (`Offline Sample Feed`, `User Entry`, `Live Market (yfinance)`)

---

## How to Run

### Interactive Menu
```bash
python task2_portfolio/portfolio.py
```

### Automated Demo Run
```bash
python task2_portfolio/portfolio.py --demo
```

### Export to Custom CSV File
```bash
python task2_portfolio/portfolio.py --demo --export-csv custom_report.csv
```

---

## Automated Testing
Run the 14 automated unit tests:
```bash
python -m unittest discover -s task2_portfolio/tests -p "test_*.py" -v
```
All tests are 100% self-contained and run offline without live API calls.
