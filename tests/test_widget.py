import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "spaceless",
    [
        "Maestro1596837868705199,",
        "MasterCard7158300734726758,",
        "Счет35383033474447895560,",
        "VisaClassic6831982476737658,",
        "VisaPlatinum8990922113665229,",
        "VisaGold5999414228426353",
    ],
)
def test_mask_account_card_if_no_space(spaceless):
    with pytest.raises(ValueError, match="некорректный формат продукта или счета"):
        mask_account_card(spaceless)


@pytest.mark.parametrize(
    "spaceless_digit",
    [
        "1596837868705199,",
        "7158300734726758,",
        "35383033474447895560,",
        "6831982476737658,",
        "VisaPlatinum123asdasdad",
        "5999414228426353",
    ],
)
def test_mask_account_card_if_no_name(spaceless_digit):
    with pytest.raises(ValueError, match="некорректный формат продукта или счета"):
        mask_account_card(spaceless_digit)


@pytest.mark.parametrize(
    "entry_info, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
    ],
)
def test_mask_account_card(entry_info, expected):
    assert mask_account_card(entry_info) == expected


@pytest.mark.parametrize(
    "date_format",
    [
        "2024.03.11T02:26:18.671407",
        "2024-03.11 02:26:18.671407",
        "2024.03.11 02:26:18.671407",
    ],
)
def test_get_date_if_incorrect_format(date_format):
    with pytest.raises(ValueError, match="некорректный формат даты"):
        get_date(date_format)


def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"


# если передается что-то одно
def test_mask_account_card_if_card():
    assert mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"


def test_mask_account_card_if_account():
    assert mask_account_card("Счет 35383033474447895560") == "Счет **5560"
