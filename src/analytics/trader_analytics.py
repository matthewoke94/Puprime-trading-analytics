import logging
import pandas as pd

logger = logging.getLogger(__name__)


def trader_summary(
    traders_df: pd.DataFrame,
    trades_df: pd.DataFrame,
    transactions_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Build a summary of each trader's activity.

    Returns:
        DataFrame with trader KPIs
    """
    # Total trades per trader
    trade_counts = (
        trades_df.groupby("trader_id")
        .agg(
            total_trades=("trade_id", "count"),
            total_pnl=("profit_loss", "sum"),
            avg_lot_size=("lot_size", "mean"),
            winning_trades=("profit_loss", lambda x: (x > 0).sum()),
        )
        .reset_index()
    )

    # Total deposits and withdrawals
    deposits = (
        transactions_df[transactions_df["type"] == "deposit"]
        .groupby("trader_id")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_deposits"})
    )

    withdrawals = (
        transactions_df[transactions_df["type"] == "withdrawal"]
        .groupby("trader_id")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_withdrawals"})
    )

    # Merge everything
    summary = traders_df.merge(trade_counts, on="trader_id", how="left")
    summary = summary.merge(deposits, on="trader_id", how="left")
    summary = summary.merge(withdrawals, on="trader_id", how="left")

    # Fill nulls
    summary[["total_trades", "winning_trades"]] = summary[
        ["total_trades", "winning_trades"]
    ].fillna(0).astype(int)
    summary[["total_deposits", "total_withdrawals", "total_pnl"]] = summary[
        ["total_deposits", "total_withdrawals", "total_pnl"]
    ].fillna(0.0)

    # Win rate
    summary["win_rate"] = (
        summary["winning_trades"] / summary["total_trades"].replace(0, 1) * 100
    ).round(2)

    logger.info(f"Trader summary built. Shape: {summary.shape}")
    return summary


def top_traders(summary_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Return top N traders by total P&L."""
    return summary_df.nlargest(n, "total_pnl")[
        ["name", "account_type", "total_trades", "total_pnl", "win_rate"]
    ]


def symbol_performance(trades_df: pd.DataFrame) -> pd.DataFrame:
    """Analyse performance by trading symbol."""
    return (
        trades_df.groupby("symbol")
        .agg(
            total_trades=("trade_id", "count"),
            total_pnl=("profit_loss", "sum"),
            avg_pnl=("profit_loss", "mean"),
            win_rate=("profit_loss", lambda x: (x > 0).mean() * 100),
        )
        .round(2)
        .reset_index()
        .sort_values("total_pnl", ascending=False)
    )


def monthly_revenue(transactions_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly deposit revenue."""
    df = transactions_df[transactions_df["type"] == "deposit"].copy()
    df["month"] = pd.to_datetime(df["timestamp"]).dt.to_period("M")
    return (
        df.groupby("month")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_deposits"})
        .sort_values("month")
    )


if __name__ == "__main__":
    import sys
    sys.path.append("/workspaces/puprime-trading-analytics")
    from src.models.simulator import (
        generate_traders,
        generate_trades,
        generate_transactions,
    )

    traders = generate_traders(100)
    trades = generate_trades(traders, 500)
    transactions = generate_transactions(traders, 300)

    summary = trader_summary(traders, trades, transactions)
    print("=== Top 10 Traders by P&L ===")
    print(top_traders(summary))

    print("\n=== Symbol Performance ===")
    print(symbol_performance(trades))

    print("\n=== Monthly Deposits ===")
    print(monthly_revenue(transactions))