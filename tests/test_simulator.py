import pandas as pd
import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src", "models"))

from simulator import (
    generate_traders,
    generate_trades,
    generate_transactions,
    validate_simulated_data,
)


@pytest.fixture
def sample_data():
    traders = generate_traders(20)
    trades = generate_trades(traders, 100)
    transactions = generate_transactions(traders, 50)
    return traders, trades, transactions


def test_generate_traders_count(sample_data):
    traders, _, _ = sample_data
    assert len(traders) == 20


def test_generate_traders_unique_ids(sample_data):
    traders, _, _ = sample_data
    assert traders["trader_id"].is_unique


def test_generate_trades_reference_real_traders(sample_data):
    traders, trades, _ = sample_data
    valid_ids = set(traders["trader_id"])
    assert trades["trader_id"].isin(valid_ids).all()


def test_generate_trades_positive_lot_sizes(sample_data):
    _, trades, _ = sample_data
    assert (trades["lot_size"] > 0).all()


def test_generate_trades_valid_durations(sample_data):
    _, trades, _ = sample_data
    assert (trades["close_time"] >= trades["open_time"]).all()


def test_generate_transactions_positive_amounts(sample_data):
    _, _, transactions = sample_data
    assert (transactions["amount"] > 0).all()


def test_validate_simulated_data_all_pass_on_clean_data(sample_data):
    traders, trades, transactions = sample_data
    results = validate_simulated_data(traders, trades, transactions)
    assert all(results.values())


def test_validate_simulated_data_detects_orphan_trades(sample_data):
    traders, trades, transactions = sample_data
    bad_trades = trades.copy()
    bad_trades.loc[0, "trader_id"] = "non-existent-trader-id"
    results = validate_simulated_data(traders, bad_trades, transactions)
    assert results["no_orphan_trades"] is False


def test_validate_simulated_data_detects_negative_duration(sample_data):
    traders, trades, transactions = sample_data
    bad_trades = trades.copy()
    bad_trades.loc[0, "close_time"] = bad_trades.loc[0, "open_time"] - pd.Timedelta(hours=1)
    results = validate_simulated_data(traders, bad_trades, transactions)
    assert results["no_negative_trade_durations"] is False