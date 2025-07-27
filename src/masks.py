def get_mask_card_number(card_number: int=None) -> str:
    """ "Функция маскировки номера банковской карты"""
    if card_number is None:
        raise TypeError("нет открытых продуктов")
    elif type(card_number) != int:
        raise TypeError("некорректный тип данных")
    else:
        mask = str(card_number)
        if 16 < len(mask) or 1 < len(mask) < 16:
            raise ValueError("номер карты должен состоять из 16 символов")
        else:
            first_num = mask[0:4]
            middle_num = mask[4:6]
            last_num = mask[-4:]
    return f"{first_num} {middle_num}** **** {last_num}"


def get_mask_account(client_account: int=None) -> str:
    """ "Функция маскировки номера банковского счета"""
    if client_account is None:
        raise TypeError("нет открытых счетов")
    elif type(client_account) != int:
        raise TypeError("некорректный тип данных")
    else:
        num = str(client_account)
        if 20 < len(num) or 1 < len(num) < 20:
            raise ValueError("банковский счет должен состоять из 20 символов")
        late_num = num[-4:]
    return f"** {late_num}"
