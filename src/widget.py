from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(confidential_info: str) -> str:
    """Функция, которая обрабатывает информацию о картах и о счетах"""
    if confidential_info is None:
        raise ValueError("некорректный формат продукта или счета")

    number = []
    name = []
    if ", " in confidential_info:
        separated = confidential_info.split(", ")
        for el in separated:
            number.append(el.split(" ")[-1])
            name.append(" ".join(el.split()[:-1]))
    else:
        number.append(confidential_info.split()[-1])
        name.append(" ".join(confidential_info.split()[:-1]))

    spaceless_name = ""
    for title in name:
        if " " in title:
            spaceless_name += title.replace(" ", "")
        elif " " not in title:
            spaceless_name += title
    if not spaceless_name.isalpha():
        raise ValueError("некорректный формат продукта или счета")

    result = []
    for i in range(len(number)):
        if name[i].lower() == "счет":
            masked_number = get_mask_account(number[i])
        else:
            masked_number = get_mask_card_number(number[i])
        result.append(f"{name[i]} {masked_number}")

    return ", ".join(result)


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
