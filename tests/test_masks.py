import pytest

from src.masks import get_mask_card_number
from src.masks import get_mask_account


def test_mask_card_number_if_none():
    with pytest.raises(TypeError) as exc_info:
        get_mask_card_number()


def test_get_mask_account_if_none():
    with pytest.raises(TypeError) as exc_info:
        get_mask_account()


def test_mask_card_number_if_not_int():
    with pytest.raises(TypeError) as exc_info:
        get_mask_card_number("7000792289606361")


def test_get_mask_account_if_not_int():
    with pytest.raises(TypeError) as exc_info:
        get_mask_account("73654108430135874305")


def test_mask_card_number_if_not_sixteen():
    with pytest.raises(ValueError ) as exc_info:
        get_mask_card_number(70007922896063)


def test_get_mask_account_if_not_twenty():
    with pytest.raises(ValueError ) as exc_info:
        get_mask_account(36541084301358743)


assert get_mask_card_number(7000792289606361) == "7000 79** **** 6361"
assert get_mask_account(73654108430135874305) == "** 4305"
