from collections import defaultdict
import functools
from typing import Dict
from typing import Sequence

import pandas as pd
import yfinance as yf

from bifolio.database.models import Transaction
from bifolio.database.models import TransactKind


# TODO (qnbhd): temporary solution
@functools.lru_cache(None)
def get_stock_data(
    ticker, start_date=None, end_date=None, interval="1d"
) -> pd.DataFrame:
    """
    Get stock data from yfinance.

    Args:
        ticker (str):
            Ticker symbol.
        interval (str):
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
        start_date (str):
            Download start date string (YYYY-MM-DD) or _datetime.
            Default is 1900-01-01
        end_date (str):
            Download end date string (YYYY-MM-DD) or _datetime.
            Default is now

    Returns:
        Stock data in a pandas DataFrame.
    """

    ticker = yf.Ticker(ticker)
    return ticker.history(
        start=start_date, end=end_date, interval=interval
    )


def get_portfolio_price(
    transactions: Sequence[Transaction],
) -> pd.DataFrame:
    """
    Get portfolio price.

    Args:
        transactions: List of transactions.

    Returns:
        Portfolio price in a pandas DataFrame.

    """
    if not transactions:
        return pd.DataFrame()

    s = sum(
        tx.amount
        * get_stock_data(f"{tx.coin}-USD")
        * (1 if tx.kind == TransactKind.BUY else -1)
        for tx in transactions
    )

    return s if isinstance(s, pd.DataFrame) else pd.DataFrame()


def get_holdings(transactions: Sequence[Transaction]):
    """
    Get holdings.

    Args:
        transactions: List of transactions.

    Returns:
        Holdings in a pandas DataFrame.

    """

    holdings: Dict[str, float] = defaultdict(lambda: 0)

    for tx in transactions:
        holdings[tx.coin] += (
            tx.amount if tx.kind == TransactKind.BUY else -tx.amount
        )

    return holdings


def get_portfolio_profit(transactions: Sequence[Transaction]):
    """
    Get portfolio profit.

    Args:
        transactions: List of transactions.

    Returns:
        Portfolio profit in a pandas DataFrame.

    """

    result = 0

    coin2price = {
        tx.coin: get_stock_data(f"{tx.coin}-USD")["Close"][-1]
        for tx in transactions
    }

    for tx in transactions:
        result += tx.amount * (coin2price[tx.coin] - tx.price)

    rel = get_portfolio_price(transactions)["Close"][-1] / sum(
        tx.amount * tx.price for tx in transactions
    )

    return result, rel * 100
