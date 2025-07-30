def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    if type(card_number) is not str or not card_number.isdigit():
        raise TypeError("некорректный тип данных")
    if len(card_number) != 16:
        raise ValueError(
            "номер карты должен состоять из 16 символов" " или нет открытых продуктов"
        )
    else:
        first_num = card_number[0:4]
        middle_num = card_number[4:6]
        last_num = card_number[-4:]
    return f"{first_num} {middle_num}** **** {last_num}"


def get_mask_account(client_account: str) -> str:
    """Функция маскировки номера банковского счета"""
    if type(client_account) is not str or not client_account.isdigit():
        raise TypeError("некорректный тип данных или нет открытых счетов")
    if len(client_account) != 20:
        raise ValueError("банковский счет должен состоять из 20 символов")
    else:
        late_num = client_account[-4:]
    return f"** {late_num}"
