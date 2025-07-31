import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number_if_none():
    with pytest.raises(TypeError):
        get_mask_card_number()


def test_get_mask_account_if_none():
    with pytest.raises(TypeError):
        get_mask_account()


def test_get_mask_card_number_if_not_str():
    with pytest.raises(TypeError):
        get_mask_card_number("none")


def test_get_mask_card_number_if_not_digit():
    with pytest.raises(TypeError):
        get_mask_card_number("none")


def test_get_mask_account_if_not_str():
    with pytest.raises(TypeError):
        get_mask_account("none")


def test_get_mask_account_if_not_digit():
    with pytest.raises(TypeError):
        get_mask_account("none")


@pytest.fixture
def mask():
    return "7000792289606", "70007922896063611"


@pytest.mark.parametrize(
    "mask",
    [
        "7000792289606",
        "700079228960636111",
    ],
)
def test_mask_card_number_if_not_sixteen(mask):
    with pytest.raises(ValueError, match="номер карты должен состоять из 16 символов"):
        get_mask_card_number(mask)


@pytest.fixture
def account():
    return "736541084301358743", "7365410843013587430555"


@pytest.mark.parametrize(
    "account",
    [
        "736541084301358743",
        "7365410843013587430555",
    ],
)
def test_get_mask_account_if_not_twenty(account):
    with pytest.raises(
        ValueError, match="банковский счет должен состоять из 20 символов"
    ):
        get_mask_account(account)


assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"
assert get_mask_account("73654108430135874305") == "**4305"
