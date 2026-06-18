import pandas as pd
import pytest
import sys
sys.path.append("/workspaces/puprime-trading-analytics")

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


@pytest.fixture
def sample_data():
    traders = generate_traders(20)
    trades = generate_trades(traders, 100)
    transactions = generate_transactions(traders, 50)
    return traders, trades, transactions


def test_generate_traders(sample_data):
    traders, _, _ = sample_data
    assert len(traders) == 20
    assert "trader_id" in traders.columns


def test_generate_trades(sample_data):
    _, trades, _ = sample_data
    assert len(trades) == 100
    assert "profit_loss" in trades.columns


def test_trader_summary_columns(sample_data):
    traders, trades, transactions = sample_data
    summary = trader_summary(traders, trades, transactions)
    for col in ["total_trades", "total_pnl", "win_rate", "total_deposits"]:
        assert col in summary.columns


def test_top_traders_returns_n(sample_data):
    traders, trades, transactions = sample_data
    summary = trader_summary(traders, trades, transactions)
    result = top_traders(summary, n=5)
    assert len(result) == 5


def test_symbol_performance(sample_data):
    _, trades, _ = sample_data
    result = symbol_performance(trades)
    assert "symbol" in result.columns
    assert "total_pnl" in result.columns


def test_monthly_revenue(sample_data):
    _, _, transactions = sample_data
    result = monthly_revenue(transactions)
    assert "total_deposits" in result.columns