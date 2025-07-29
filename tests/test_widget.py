import pytest

from src.widget import get_date, mask_account_card


def test_mask_account_card_if_none():
    with pytest.raises(TypeError):
        mask_account_card()


def test_get_date_if_none():
    with pytest.raises(TypeError):
        get_date()


@pytest.fixture
def spaceless():
    return [
        "Maestro1596837868705199,"
        "MasterCard7158300734726758,"
        "Счет35383033474447895560,"
        "VisaClassic6831982476737658,"
        "VisaPlatinum8990922113665229,"
        "VisaGold5999414228426353,"
    ]


@pytest.fixture
def spaceless_digit():
    return [
        "1596837868705199,"
        "7158300734726758,"
        "35383033474447895560,"
        "6831982476737658,"
        "8990922113665229,"
        "5999414228426353,"
    ]


@pytest.fixture
def number():
    return [
        "Maestro," "MasterCard," "Счет," "Visa Classic," "Visa Platinum," "Visa Gold,"
    ]


@pytest.mark.parametrize(
    "spaceless",
    [
        ("Maestro1596837868705199,", ["некорректный формат продукта или счета"]),
        ("MasterCard7158300734726758,", ["некорректный формат продукта или счета"]),
        ("Счет35383033474447895560,", ["некорректный формат продукта или счета"]),
        ("VisaClassic6831982476737658,", ["некорректный формат продукта или счета"]),
        ("VisaPlatinum8990922113665229,", ["некорректный формат продукта или счета"]),
        ("VisaGold5999414228426353", ["некорректный формат продукта или счета"]),
    ],
)
def test_mask_account_card_if_no_whitespace(spaceless):
    with pytest.raises(ValueError, match="некорректный формат продукта или счета"):
        mask_account_card(spaceless)


@pytest.mark.parametrize(
    "spaceless_digit",
    [
        ("1596837868705199,", ["некорректный формат продукта или счета"]),
        ("7158300734726758,", ["некорректный формат продукта или счета"]),
        ("35383033474447895560,", ["некорректный формат продукта или счета"]),
        ("6831982476737658,", ["некорректный формат продукта или счета"]),
        ("8990922113665229,", ["некорректный формат продукта или счета"]),
        ("5999414228426353", ["некорректный формат продукта или счета"]),
    ],
)
def test_mask_account_card_if_no_name(spaceless_digit):
    with pytest.raises(ValueError, match="некорректный формат продукта или счета"):
        mask_account_card(spaceless_digit)


@pytest.mark.parametrize(
    "number",
    [
        ("Maestro,", ["некорректный формат продукта или счета"]),
        ("MasterCard,", ["некорректный формат продукта или счета"]),
        ("Счет,", ["некорректный формат продукта или счета"]),
        ("Visa Classic,", ["некорректный формат продукта или счета"]),
        ("Visa Platinum,", ["некорректный формат продукта или счета"]),
        ("Visa Gold", ["некорректный формат продукта или счета"]),
    ],
)
def test_mask_account_card_if_no_numbers(number):
    with pytest.raises(ValueError, match="некорректный формат продукта или счета"):
        mask_account_card(number)


@pytest.fixture
def date_formats():
    return [
        "2024.03.11T02:26:18.671407",
        "2024-03.11 02:26:18.671407",
        "2024.03.11 02:26:18.671407",
    ]


@pytest.mark.parametrize(
    "date_format",
    [
        ("2024.03.11T02:26:18.671407", ["некорректный формат даты"]),
        ("2024-03.11 02:26:18.671407", ["некорректный формат даты"]),
        ("2024.03.11 02:26:18.671407", ["некорректный формат даты"]),
    ],
)
def test_get_date_if_incorrect_format(date_format):
    with pytest.raises(ValueError, match="некорректный формат даты"):
        get_date(date_format)


assert mask_account_card("Maestro 1596837868705199") == "Maestro 1596 83** **** 5199"
assert (
    mask_account_card("MasterCard 7158300734726758") == "MasterCard 7158 30** **** 6758"
)
assert mask_account_card("Счет 35383033474447895560") == "Счет ** 5560"
assert (
    mask_account_card("Visa Classic 6831982476737658")
    == "Visa Classic 6831 98** **** 7658"
)
assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
