# PuPrime Trading Analytics

A client trading analytics platform that simulates and analyses trader behaviour, 
P&L performance, and revenue trends for an online forex trading broker.

## Project Overview

This project simulates the kind of analytics infrastructure a trading company 
like PuPrime uses to monitor trader activity, identify top performers, and 
track business revenue.

## Features

- Simulated dataset of 100 traders, 500 trades, 300 transactions
- Trader KPI analytics: P&L, win rate, deposits, withdrawals
- Symbol performance analysis across EUR/USD, GBP/USD, USD/JPY, XAU/USD, BTC/USD
- Monthly deposit revenue tracking
- Interactive Streamlit dashboard with charts and tables
- Unit tested with pytest

## Tech Stack

- **Language:** Python 3.12
- **Libraries:** pandas, streamlit, faker, pytest
- **Version Control:** Git/GitHub

## Project Structure
## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the dashboard:
```bash
streamlit run src/analytics/dashboard.py
```

## Dashboard Preview

- **100 traders** across standard, premium and VIP accounts
- **$928,249** total deposits tracked
- **81 active traders**
- Interactive charts for symbol performance and monthly revenue

## Author

Matthew James — Data Engineer
GitHub: github.com/matthewoke94