def get_mask_card_number(card_number:int)->str:
    """"Функция маскировки номера банковской карты """
    mask = str(card_number)
    first_num = mask[0:5]
    middle_num = mask[5:7]
    last_num = mask[-4:]
    return f"{first_num} {middle_num}** **** {last_num}"


def get_mask_account(client_account:int)->str:
    """"Функция маскировки номера банковского счета"""
    num = str(client_account)
    late_num = num[-4:]
    return f"** {late_num}"
