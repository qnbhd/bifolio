from collections import namedtuple
from pathlib import Path
from unittest import mock

import numpy as np
import numpy.testing
import pandas as pd
import pytest

from bifolio.database.models import TransactKind
from bifolio.domain.finance import get_holdings
from bifolio.domain.finance import get_portfolio_price
from bifolio.domain.finance import get_portfolio_profit


Tx = namedtuple("Tx", ["amount", "coin", "kind", "price"])

STOCK_DATA_FILE = Path(__file__).parent / "stock_data.json"


# noinspection PyTypeChecker
def test_get_portfolio_price():
    transactions = [
        Tx(1, "BTC", "BUY", 20000),
        Tx(2, "ETH", "BUY", 3000),
    ]

    with mock.patch(
        "bifolio.domain.finance.get_stock_data"
    ) as mock_get_stock_data:
        mock_get_stock_data.return_value = pd.read_json(
            STOCK_DATA_FILE
        )

        result = get_portfolio_price(transactions)

        numpy.testing.assert_allclose(
            result["Close"].iloc[0], 64802.712890625
        )

        mock_get_stock_data.assert_has_calls(
            [
                mock.call("BTC-USD"),
                mock.call("ETH-USD"),
            ]
        )


@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
            [
                Tx(1, "BTC", TransactKind.BUY, 20000),
                Tx(2, "ETH", TransactKind.BUY, 3000),
                Tx(1, "BTC", TransactKind.SELL, 21000),
            ],
            {"BTC": 0, "ETH": 2},
        ),
        (
            [
                Tx(1, "BTC", TransactKind.BUY, 20000),
                Tx(2, "ETH", TransactKind.BUY, 3000),
                Tx(1, "BTC", TransactKind.SELL, 21000),
                Tx(1, "ETH", TransactKind.SELL, 3100),
            ],
            {"BTC": 0, "ETH": 1},
        ),
    ],
)
def test_get_holdings(transactions, expected):

    assert "BUY" == TransactKind.BUY
    assert "SELL" == TransactKind.SELL

    # noinspection PyTypeChecker
    result = get_holdings(transactions)

    assert result == expected


# noinspection PyTypeChecker
@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
            [
                Tx(1, "BTC", TransactKind.BUY, 20000),
                Tx(1, "BTC", TransactKind.BUY, 21000),
            ],
            np.array([-2822.894531, 93.114891]),
        ),
        (
            [
                Tx(1, "BTC", TransactKind.BUY, 18000),
                Tx(0.5, "BTC", TransactKind.BUY, 21000),
            ],
            np.array([132.829102, 100.466067]),
        ),
    ],
)
def test_get_portfolio_profit(transactions, expected):
    with mock.patch(
        "bifolio.domain.finance.get_stock_data"
    ) as mock_get_stock_data:
        mock_get_stock_data.return_value = pd.read_json(
            STOCK_DATA_FILE
        )

        result = get_portfolio_profit(transactions)

        numpy.testing.assert_allclose(result, expected)
