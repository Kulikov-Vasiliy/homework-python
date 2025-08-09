import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


def test_filter_by_currency_if_transactions_is_none():
    with pytest.raises(TypeError):
        filter_by_currency()


def test_transaction_descriptions_if_transactions_is_none():
    with pytest.raises(TypeError):
        filter_by_currency()


def test_filter_by_currency(transactions):
    result = filter_by_currency(transactions)
    assert next(result)


def test_transaction_descriptions(transactions):
    result = transaction_descriptions(transactions)
    assert next(result)


def test_card_number_generator():
    result = card_number_generator(1, 9)
    assert next(result) == "0000 0000 0000 0001"
    assert next(result) == "0000 0000 0000 0002"
    assert next(result) == "0000 0000 0000 0003"
