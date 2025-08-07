import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(confidential_info: str) -> str:
    """Функция, которая обрабатывает информацию о картах и о счетах"""
    if confidential_info.count(" ") < 1:
        raise ValueError("некорректный формат продукта или счета")
    result = []
    pattern = r".*?\d+"
    matches = re.findall(pattern, confidential_info)
    for match in matches:
        name, number = match.rsplit(" ", maxsplit=1)

        if name.lower() == "счет":
            masked_number = get_mask_account(number)
        else:
            masked_number = get_mask_card_number(number)
        result.append(f"{name} {masked_number}")

    return "\n".join(result)


def get_date(operation_data: str) -> str:
    """Принимает на вход строку с датой в формате '2024-03-11T02:26:18.671407'
    и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    if "T" not in operation_data:
        raise ValueError("некорректный формат даты")
    date_str, _ = operation_data.split("T")
    if date_str.count("-") != 2:
        raise ValueError("некорректный формат даты")
    year, month, day = date_str.split("-")

    return f"{day}.{month}.{year}"
