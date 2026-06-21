import logging
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict
import pandas as pd
from faker import Faker

fake = Faker()
random.seed(42)

logger = logging.getLogger(__name__)


def generate_traders(n: int = 100) -> pd.DataFrame:
    """
    Generate simulated trader accounts.

    Args:
        n: Number of traders to generate

    Returns:
        DataFrame of trader accounts
    """
    traders = []
    for _ in range(n):
        registration_date = fake.date_between(
            start_date="-2y", end_date="today"
        )
        traders.append({
            "trader_id": str(uuid.uuid4()),
            "name": fake.name(),
            "email": fake.email(),
            "country": fake.country(),
            "account_type": random.choice(["standard", "premium", "vip"]),
            "registration_date": registration_date,
            "is_active": random.choice([True, True, True, False]),
        })
    return pd.DataFrame(traders)


def generate_trades(traders_df: pd.DataFrame, n: int = 500) -> pd.DataFrame:
    """
    Generate simulated trade records.

    Args:
        traders_df: DataFrame of trader accounts
        n: Number of trades to generate

    Returns:
        DataFrame of trade records
    """
    trader_ids = traders_df["trader_id"].tolist()
    symbols = ["EUR/USD", "GBP/USD", "USD/JPY", "XAU/USD", "BTC/USD"]
    trades = []

    for _ in range(n):
        open_time = fake.date_time_between(start_date="-1y", end_date="now")
        duration = timedelta(minutes=random.randint(5, 1440))
        trades.append({
            "trade_id": str(uuid.uuid4()),
            "trader_id": random.choice(trader_ids),
            "symbol": random.choice(symbols),
            "direction": random.choice(["buy", "sell"]),
            "lot_size": round(random.uniform(0.01, 5.0), 2),
            "open_price": round(random.uniform(1.0, 200.0), 5),
            "close_price": round(random.uniform(1.0, 200.0), 5),
            "open_time": open_time,
            "close_time": open_time + duration,
            "profit_loss": round(random.uniform(-500, 500), 2),
            "status": random.choice(["closed", "closed", "closed", "open"]),
        })
    return pd.DataFrame(trades)


def generate_transactions(
    traders_df: pd.DataFrame, n: int = 300
) -> pd.DataFrame:
    """
    Generate simulated deposit/withdrawal transactions.

    Args:
        traders_df: DataFrame of trader accounts
        n: Number of transactions to generate

    Returns:
        DataFrame of transactions
    """
    trader_ids = traders_df["trader_id"].tolist()
    transactions = []

    for _ in range(n):
        transactions.append({
            "transaction_id": str(uuid.uuid4()),
            "trader_id": random.choice(trader_ids),
            "type": random.choice(["deposit", "deposit", "withdrawal"]),
            "amount": round(random.uniform(100, 10000), 2),
            "currency": "USD",
            "timestamp": fake.date_time_between(
                start_date="-1y", end_date="now"
            ),
            "status": random.choice(["completed", "completed", "pending", "failed"]),
        })
    return pd.DataFrame(transactions)


def validate_simulated_data(
    traders_df: pd.DataFrame,
    trades_df: pd.DataFrame,
    transactions_df: pd.DataFrame
) -> dict:
    """
    Run data quality checks on simulated datasets before they're used
    downstream. Catches internal inconsistencies that would otherwise
    silently produce misleading analytics.

    Returns:
        Dict of {check_name: passed (bool)} for every check run.
    """
    results = {}

    valid_trader_ids = set(traders_df["trader_id"])

    orphan_trades = ~trades_df["trader_id"].isin(valid_trader_ids)
    results["no_orphan_trades"] = not orphan_trades.any()

    orphan_transactions = ~transactions_df["trader_id"].isin(valid_trader_ids)
    results["no_orphan_transactions"] = not orphan_transactions.any()

    invalid_duration = trades_df["close_time"] < trades_df["open_time"]
    results["no_negative_trade_durations"] = not invalid_duration.any()

    results["positive_lot_sizes"] = (trades_df["lot_size"] > 0).all()
    results["positive_transaction_amounts"] = (transactions_df["amount"] > 0).all()
    results["no_duplicate_traders"] = not traders_df["trader_id"].duplicated().any()

    failed = [k for k, v in results.items() if not v]
    if failed:
        logger.error(f"Data quality checks failed: {failed}")
    else:
        logger.info("All data quality checks passed.")

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    traders = generate_traders(100)
    trades = generate_trades(traders, 500)
    transactions = generate_transactions(traders, 300)

    print(f"Traders: {len(traders)}")
    print(f"Trades: {len(trades)}")
    print(f"Transactions: {len(transactions)}")

    validation_results = validate_simulated_data(traders, trades, transactions)
    print("\nData quality checks:")
    for check, passed in validation_results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {check}")

    print("\nSample trader:")
    print(traders.head(2))