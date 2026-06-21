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
    traders = []
    for _ in range(n):
        registration_date = fake.date_between(start_date="-2y", end_date="today")
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


def generate_transactions(traders_df: pd.DataFrame, n: int = 300) -> pd.DataFrame:
    trader_ids = traders_df["trader_id"].tolist()
    transactions = []
    for _ in range(n):
        transactions.append({
            "transaction_id": str(uuid.uuid4()),
            "trader_id": random.choice(trader_ids),
            "type": random.choice(["deposit", "deposit", "withdrawal"]),
            "amount": round(random.uniform(100, 10000), 2),
            "currency": "USD",
            "timestamp": fake.date_time_between(start_date="-1y", end_date="now"),
            "status": random.choice(["completed", "completed", "pending", "failed"]),
        })
    return pd.DataFrame(transactions)


def validate_simulated_data(traders_df, trades_df, transactions_df) -> dict:
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


def save_to_db(traders_df, trades_df, transactions_df) -> dict:
    import os
    import psycopg2
    from psycopg2.extras import execute_values
    from dotenv import load_dotenv

    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        logger.error("DATABASE_URL not found. Skipping persistence.")
        return {}

    counts = {"traders": 0, "trades": 0, "transactions": 0}

    try:
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sim_traders (
                trader_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                country VARCHAR(100),
                account_type VARCHAR(20),
                registration_date DATE,
                is_active BOOLEAN
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sim_trades (
                trade_id VARCHAR(36) PRIMARY KEY,
                trader_id VARCHAR(36) REFERENCES sim_traders(trader_id),
                symbol VARCHAR(20),
                direction VARCHAR(10),
                lot_size NUMERIC(10,2),
                open_price NUMERIC(10,5),
                close_price NUMERIC(10,5),
                open_time TIMESTAMP,
                close_time TIMESTAMP,
                profit_loss NUMERIC(10,2),
                status VARCHAR(20)
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sim_transactions (
                transaction_id VARCHAR(36) PRIMARY KEY,
                trader_id VARCHAR(36) REFERENCES sim_traders(trader_id),
                type VARCHAR(20),
                amount NUMERIC(10,2),
                currency VARCHAR(10),
                timestamp TIMESTAMP,
                status VARCHAR(20)
            );
        """)
        conn.commit()

        traders_records = list(traders_df[[
            "trader_id", "name", "email", "country",
            "account_type", "registration_date", "is_active"
        ]].itertuples(index=False, name=None))
        execute_values(cur, "INSERT INTO sim_traders VALUES %s ON CONFLICT (trader_id) DO NOTHING;", traders_records)
        counts["traders"] = len(traders_records)

        trades_records = list(trades_df[[
            "trade_id", "trader_id", "symbol", "direction", "lot_size",
            "open_price", "close_price", "open_time", "close_time",
            "profit_loss", "status"
        ]].itertuples(index=False, name=None))
        execute_values(cur, "INSERT INTO sim_trades VALUES %s ON CONFLICT (trade_id) DO NOTHING;", trades_records)
        counts["trades"] = len(trades_records)

        transactions_records = list(transactions_df[[
            "transaction_id", "trader_id", "type", "amount",
            "currency", "timestamp", "status"
        ]].itertuples(index=False, name=None))
        execute_values(cur, "INSERT INTO sim_transactions VALUES %s ON CONFLICT (transaction_id) DO NOTHING;", transactions_records)
        counts["transactions"] = len(transactions_records)

        conn.commit()
        conn.close()
        logger.info(f"Persisted to database (attempted): {counts}")
        return counts

    except Exception as e:
        logger.error(f"Database persistence failed: {e}")
        raise


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

    save_to_db(traders, trades, transactions)

    print("\nSample trader:")
    print(traders.head(2))