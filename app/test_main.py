import datetime
from unittest.mock import patch

import pytest

from app.main import outdated_products


class NewDate(datetime.date):
    @classmethod
    def today(cls):
        return cls(2010, 1, 1)


datetime.date = NewDate


@pytest.fixture
def products():
    return [
        {
            "name": "salmon",
            "expiration_date": datetime.date(2022, 2, 10),
            "price": 600
        },
        {
            "name": "chicken",
            "expiration_date": datetime.date(2022, 2, 5),
            "price": 120
        },
        {
            "name": "duck",
            "expiration_date": datetime.date(2022, 2, 1),
            "price": 160
        }
    ]


@pytest.mark.parametrize(
    "year, month, day, result",
    [
        (2023, 1, 1, ["salmon", "chicken", "duck"]),
        (2022, 2, 11, ["salmon", "chicken", "duck"]),
        (2022, 2, 10, ["chicken", "duck"]),
        (2022, 2, 3, ["duck"]),
        (2022, 1, 10, []),
        (2022, 2, 1, [])
    ],
    ids=[
        "all outdated in the next year",
        "all outdated next day after the last expired",
        "one product is not outdated in the last expiration date",
        "one product is expired",
        "all products are good",
        "all products are good in the smallest expiration date",
    ]

)
def test_outdated_products(year, month, day, result, products):
    with patch("datetime.date.today") as patched_today:
        patched_today.return_value = datetime.date(year, month, day)
        assert outdated_products(products) == result
