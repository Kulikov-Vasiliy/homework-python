from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(confidential_info: str) -> str:
    """Функция, которая обрабатывает информацию о картах и о счетах"""
    if confidential_info.count(" ") == 0:
        raise ValueError("некорректный формат продукта или счета")
    else:
        name, number = confidential_info.rsplit(" ", maxsplit=1)
        spaceless_name = ""
        if " " in name:
            spaceless_name += name.replace(" ", "")
        elif " " not in name:
            spaceless_name += name
            if not spaceless_name.isalpha():
                raise ValueError("некорректный формат продукта или счета")

        if name.lower() == "счет":
            masked_number = get_mask_account(number)
        else:
            masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(operation_data: str) -> str:
    """Принимает на вход строку с датой в формате '2024-03-11T02:26:18.671407'
    и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    if "T" not in operation_data:
        raise ValueError("некорректный формат даты")

    else:
        date_str, _ = operation_data.split("T")
        if date_str.count("-") != 2:
            raise ValueError("некорректный формат даты")
        else:
            year, month, day = date_str.split("-")

    return f"{day}.{month}.{year}"
