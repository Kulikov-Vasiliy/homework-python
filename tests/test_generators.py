import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


def test_filter_by_currency_if_transactions_is_none():
    with pytest.raises(TypeError):
        filter_by_currency()


def test_transaction_descriptions_if_transactions_is_none():
    with pytest.raises(TypeError):
        filter_by_currency()


def test_filter_by_currency(transactions):
    result = filter_by_currency(transactions)
    assert next(result)


@pytest.mark.parametrize(
    "expected_result_usd",
    [
        [
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {"name": "USD", "code": "USD"},
                },
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702",
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {"name": "USD", "code": "USD"},
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188",
            },
            {
                "id": 895315941,
                "state": "EXECUTED",
                "date": "2018-08-19T04:27:37.904916",
                "operationAmount": {
                    "amount": "56883.54",
                    "currency": {"name": "USD", "code": "USD"},
                },
                "description": "Перевод с карты на карту",
                "from": "Visa Classic 6831982476737658",
                "to": "Visa Platinum 8990922113665229",
            },
        ]
    ],
)
def test_filter_by_currency_usd(transactions, expected_result_usd):
    result = list(filter_by_currency(transactions))
    assert result == expected_result_usd


def test_transaction_descriptions(transactions):
    result = transaction_descriptions(transactions)
    assert next(result)


def test_card_number_generator_zero():
    with pytest.raises(ValueError) as e:
        result = card_number_generator(0, 2)
        next(result)
    assert str(e.value) == "ошибка"


def test_card_number_generator_successful_line():
    result = card_number_generator(1, 3)
    assert next(result) == "0000 0000 0000 0001"
    assert next(result) == "0000 0000 0000 0002"
    assert next(result) == "0000 0000 0000 0003"


@pytest.mark.parametrize(
    "start, stop, expected",
    [
        (1, 2, ["0000 0000 0000 0001", "0000 0000 0000 0002"]),
        (
            3,
            6,
            [
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
                "0000 0000 0000 0006",
            ],
        ),
    ],
)
def test_card_number_generator_success(start, stop, expected):
    result = list(card_number_generator(start, stop))
    assert result == expected
