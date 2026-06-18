import sys
sys.path.append("/workspaces/puprime-trading-analytics")

import streamlit as st
import pandas as pd
from src.models.simulator import (
    generate_traders,
    generate_trades,
    generate_transactions,
)
from src.analytics.trader_analytics import (
    trader_summary,
    top_traders,
    symbol_performance,
    monthly_revenue,
)

st.set_page_config(
    page_title="PuPrime Trading Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 PuPrime Trading Analytics Dashboard")
st.markdown("Real-time insights into trader activity, performance and revenue.")

# Generate data
@st.cache_data
def load_data():
    traders = generate_traders(100)
    trades = generate_trades(traders, 500)
    transactions = generate_transactions(traders, 300)
    summary = trader_summary(traders, trades, transactions)
    return traders, trades, transactions, summary

traders, trades, transactions, summary = load_data()

# KPI Metrics
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Traders", len(traders))
col2.metric("Total Trades", len(trades))
col3.metric("Total Deposits", f"${transactions[transactions['type']=='deposit']['amount'].sum():,.0f}")
col4.metric("Active Traders", traders["is_active"].sum())

st.divider()

# Top Traders
st.subheader("🏆 Top 10 Traders by P&L")
st.dataframe(top_traders(summary), use_container_width=True)

st.divider()

# Symbol Performance
st.subheader("📊 Symbol Performance")
sym_perf = symbol_performance(trades)
st.bar_chart(sym_perf.set_index("symbol")["total_pnl"])
st.dataframe(sym_perf, use_container_width=True)

st.divider()

# Monthly Revenue
st.subheader("💰 Monthly Deposits")
monthly = monthly_revenue(transactions)
monthly["month"] = monthly["month"].astype(str)
st.line_chart(monthly.set_index("month")["total_deposits"])

st.divider()

# Raw Data
st.subheader("🗃️ Raw Trader Data")
st.dataframe(summary[[
    "name", "account_type", "country",
    "total_trades", "total_pnl", "win_rate",
    "total_deposits", "total_withdrawals"
]], use_container_width=True)