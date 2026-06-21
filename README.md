# PuPrime Trading Analytics Dashboard

## Business problem

Forex brokers need visibility into how their client base is actually performing — which traders are profitable, which currency pairs drive the most activity, and whether deposit revenue is growing or shrinking month over month. Without this, business decisions (marketing spend, account manager focus, risk flagging) are made blind.

## Solution

An analytics layer that simulates a realistic trader/trade/transaction dataset, validates its internal consistency, computes key business metrics, and surfaces them through an interactive Streamlit dashboard — built so the same analytics functions could be pointed at a real production database with no changes to the analytics logic itself.

## Outcome

Tracks 100 traders, 500 trades, 300 transactions, $928K in simulated deposits. Every dataset passes 6 automated data quality checks (no orphan records, no negative durations, no invalid amounts) before it's used. 15 unit tests cover both the data generation and the analytics calculations.

---

## Architecture
The simulator and validator are decoupled from the analytics functions — in a production setting, `trader_analytics.py` would read from a real `traders`/`trades`/`transactions` database instead of simulated DataFrames, with no changes needed to the KPI logic itself.

## Data source

Simulated using [Faker](https://faker.readthedocs.io/), seeded for reproducibility (`random.seed(42)`). This is explicitly a synthetic dataset — in production this would be replaced by PuPrime's actual trading platform database. The schema (trader_id, trade_id, transaction_id as foreign keys) mirrors what a real CRM + trading engine would produce.

## ETL / data process, step by step

**1. Generation (`simulator.py`)**
- `generate_traders()` — 100 trader accounts: name, country, account tier (standard/premium/vip), registration date, active status
- `generate_trades()` — 500 trades referencing real trader IDs: symbol, direction, lot size, open/close price and time, profit/loss
- `generate_transactions()` — 300 deposits/withdrawals referencing real trader IDs

**2. Validation (`validate_simulated_data()`)**
Six automated checks run before any data is trusted downstream:
| Check | Catches |
|---|---|
| `no_orphan_trades` | Trades referencing a trader_id that doesn't exist |
| `no_orphan_transactions` | Transactions referencing a trader_id that doesn't exist |
| `no_negative_trade_durations` | A trade closing before it opened |
| `positive_lot_sizes` | Zero or negative lot sizes |
| `positive_transaction_amounts` | Zero or negative deposit/withdrawal amounts |
| `no_duplicate_traders` | Duplicate trader_id values |

**3. Analytics (`trader_analytics.py`)**
- `trader_summary()` — joins traders with their trade and transaction history; computes total trades, win rate, total P&L, total deposits/withdrawals per trader
- `top_traders()` — ranks traders by total P&L
- `symbol_performance()` — aggregates P&L, win rate, and trade count per currency pair
- `monthly_revenue()` — sums deposits by calendar month to show revenue trend

**4. Presentation (`dashboard.py`)**
- Streamlit app with cached data generation (`@st.cache_data`) so the dashboard doesn't regenerate data on every interaction
- KPI cards, top traders table, symbol performance bar chart, monthly deposits line chart, raw data explorer

## Key metrics surfaced

- **Total traders:** 100 (81 active)
- **Total deposits tracked:** $928,249
- **Symbol performance:** P&L breakdown across EUR/USD, GBP/USD, USD/JPY, XAU/USD, BTC/USD
- **Top 10 traders by profitability**, with win rate per trader

## Reliability features

| Feature | Implementation |
|---|---|
| Referential integrity checks | Validates every trade/transaction references a real trader |
| Business rule validation | Rejects negative durations, zero/negative amounts |
| Reproducibility | Seeded random generation (`seed=42`) for consistent test data |
| Test coverage | 15 tests across data generation and analytics functions |
| Caching | Streamlit `@st.cache_data` avoids redundant computation |

## Tech stack

- **Language:** Python 3.12
- **Libraries:** pandas, streamlit, faker, pytest
- **Version Control:** Git/GitHub
- **CI:** GitHub Actions

## Project structure
## Setup

```bash
pip install -r requirements.txt
streamlit run src/analytics/dashboard.py
```

## Known gaps / next steps

- Data is simulated, not connected to a live database — the natural next step is pointing `trader_analytics.py` at a real Postgres instance (the schema already mirrors [Project 1's](https://github.com/matthewoke94/puprime-market-pipeline) database conventions)
- No authentication on the dashboard — fine for a portfolio demo, would need access control in production
- Dashboard regenerates simulated data on cold start rather than persisting it

## Business value

This is the layer that turns raw trading activity into decisions: which traders to prioritize for retention, which currency pairs are most/least profitable for the business, and whether deposit revenue is trending up or down month over month.

## Author

Matthew James — Data Engineer
GitHub: github.com/matthewoke94