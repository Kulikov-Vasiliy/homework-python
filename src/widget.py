from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(confidential_info: str) -> str:
    """Функция, которая обрабатывает информацию о картах и о счетах"""
    if confidential_info is None:
        raise TypeError("нет открытых продуктов или счетов")
    elif confidential_info.count(" ") == 0:
        raise ValueError("некорректный формат продукта или счета")
    else:
        spaceless_name = ""
        name, number = confidential_info.rsplit(" ", maxsplit=1)
        if " " in name:
            spaceless_name += name.replace(" ", "")
        elif " " not in name:
            spaceless_name += name
        elif not spaceless_name.isalpha():
            raise ValueError("некорректный формат продукта или счета")

        if not number.isdigit():
            raise ValueError("некорректный формат продукта или счета")
        elif name.lower() == "счет":
            masked_number = get_mask_account(number)
        else:
            masked_number = get_mask_card_number(number)
    return f"{name} {masked_number}"


def get_date(operation_data: str) -> str:
    """Принимает на вход строку с датой в формате '2024-03-11T02:26:18.671407'
    и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    if operation_data is None:
        raise TypeError("нет операций")
    elif "T" not in operation_data:
        raise ValueError("некорректный формат даты")
    else:
        date_str, _ = operation_data.split("T")
        if date_str.count("-") != 2:
            raise ValueError("некорректный формат даты")
        else:
            year, month, day = date_str.split("-")
    return f"{day}.{month}.{year}"
