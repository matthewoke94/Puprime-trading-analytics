# PuPrime Trading Analytics Dashboard


## Business problem

Forex brokers need visibility into how their client base is actually performing — which traders are profitable, which currency pairs drive the most activity, and whether deposit revenue is growing or shrinking month over month. Without this, business decisions (marketing spend, account manager focus, risk flagging) are made blind.

## Solution

An analytics layer that simulates a realistic trader/trade/transaction dataset, validates its internal consistency, computes key business metrics, and surfaces them through an interactive Streamlit dashboard — built so the same analytics functions could be pointed at a real production database with no changes to the analytics logic itself.

## Outcome

The solution generates and validates a realistic trading dataset consisting of **100 traders, 500 trades, and 300 financial transactions**, representing over **$928K in simulated deposits**. Before any analytics are produced, every dataset passes **six automated data quality validations** to ensure referential integrity and business rule compliance. The project is further supported by **15 automated unit tests**, providing confidence in both the data generation process and the analytical calculations.

=======
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Pytest](https://img.shields.io/badge/Pytest-Tested-yellow)
![License](https://img.shields.io/badge/License-MIT-lightgrey)
>>>>>>> 21a1095 (Improve project documentation)

---

# Overview

The **PuPrime Trading Analytics Dashboard** is an end-to-end analytics project that simulates a realistic forex trading environment, validates data quality, computes business-critical KPIs, and presents them through an interactive Streamlit dashboard.

The project demonstrates how a data engineering workflow can transform raw trading activity into meaningful business intelligence for brokers, risk teams, and management.

---

# Business Problem

Forex brokers generate large volumes of transactional data every day.

Without a centralized analytics layer, it becomes difficult to answer important business questions such as:

- Which traders are the most profitable?
- Which trading instruments generate the highest activity?
- Are client deposits increasing over time?
- Which traders require retention efforts?
- Are there suspicious or invalid trading records?

This project addresses these challenges by building an analytics pipeline capable of supporting production-ready reporting.

---

# Solution

The project simulates a complete trading ecosystem consisting of:

- Traders
- Trades
- Financial Transactions

The pipeline validates every dataset, calculates key trading metrics, and visualizes performance through an interactive Streamlit dashboard.

The analytics layer is designed so that simulated data can easily be replaced with production database tables without changing the business logic.

---

# Project Architecture

```text
Generate Data
      │
      ▼
Data Validation
      │
      ▼
Business Analytics
      │
      ▼
Interactive Dashboard
```

---

# Dataset

Synthetic data is generated using **Faker** with a fixed random seed for reproducibility.

The project creates:

- 100 Traders
- 500 Trades
- 300 Transactions

The schema closely mirrors a real-world forex trading platform.

---

# ETL Workflow

## Step 1 — Data Generation

`simulator.py`

Creates:

- Trader Accounts
- Trade History
- Deposits
- Withdrawals

Every trade references a valid trader.

---

## Step 2 — Data Validation

The validation layer performs automated quality checks before analytics begin.

### Data Quality Checks

| Validation | Purpose |
|------------|---------|
| No orphan trades | Every trade references an existing trader |
| No orphan transactions | Every transaction references an existing trader |
| Positive lot sizes | Prevent invalid trading volume |
| Positive transaction amounts | Prevent invalid deposits |
| No duplicate trader IDs | Maintain uniqueness |
| No negative trade duration | Ensure logical timestamps |

---

## Step 3 — Analytics

`trader_analytics.py`

Calculates:

- Trader profitability
- Win rate
- Total P&L
- Deposit totals
- Withdrawal totals
- Currency pair performance
- Monthly deposit trends

---

## Step 4 — Dashboard

`dashboard.py`

Interactive Streamlit dashboard containing:

- Executive KPIs
- Top Traders
- Currency Pair Performance
- Monthly Deposit Trend
- Raw Dataset Explorer

---

# Dashboard Preview

> Dashboard screenshots will be added here.

Future screenshots:

- Executive Dashboard
- KPI Cards
- Top Traders
- Symbol Performance
- Monthly Deposits

---

# Business Metrics

The dashboard reports:

- Total Traders
- Active Traders
- Total Deposits
- Total Withdrawals
- Net Revenue
- Win Rate
- Trader Profitability
- Symbol Performance
- Monthly Deposit Growth

---

# Reliability Features

| Feature | Description |
|----------|-------------|
| Referential Integrity | Prevents orphan records |
| Business Rule Validation | Detects invalid trading data |
| Reproducibility | Fixed random seed |
| Automated Testing | 15 unit tests |
| Cached Dashboard | Faster Streamlit performance |

---

# Technology Stack

## Language

- Python 3.12

## Libraries

- Pandas
- Streamlit
- Faker
- Pytest

## Development

- Git
- GitHub
- GitHub Actions

---

# Project Structure

```text
puprime-trading-analytics/

├── src/
│   ├── analytics/
│   ├── models/
│   └── pipeline/
│
├── tests/
│   ├── test_analytics.py
│   └── test_simulator.py
│
├── requirements.txt
├── README.md
└── .env.example
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/matthewoke94/puprime-trading-analytics.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the dashboard

```bash
streamlit run src/analytics/dashboard.py
```

---

# Testing

<<<<<<< HEAD
## Business Value

This project demonstrates how data engineering and analytics can transform raw trading activity into actionable business intelligence. By consolidating trader performance, symbol profitability, and deposit trends into a single analytics layer, brokers can make more informed decisions around client retention, revenue growth, risk monitoring, and operational performance. The modular architecture also allows the analytics layer to transition from simulated data to a production database with minimal code changes.
=======
Run all unit tests

```bash
pytest
```
>>>>>>> 21a1095 (Improve project documentation)

---

<<<<<<< HEAD
Matthew James

Data Engineer | Python | SQL | ETL | Data Pipelines
=======
# Future Improvements

- PostgreSQL integration
- Docker containerization
- Apache Airflow orchestration
- Azure deployment
- AWS deployment
- Real-time trading API integration
- Power BI reporting layer

---

# Business Value

This project demonstrates how modern analytics can transform raw trading data into actionable business insights.

The solution enables organizations to:

- Monitor trader performance
- Improve customer retention
- Track business revenue
- Identify profitable instruments
- Support data-driven decision making

---

# Author

**Matthew James**

**Data Engineer**

### GitHub

https://github.com/matthewoke94

---

# License

This project is released under the MIT License.
>>>>>>> 21a1095 (Improve project documentation)
