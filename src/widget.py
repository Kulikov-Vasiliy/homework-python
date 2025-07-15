from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(confidential_info: str) -> str:
    """Функция, которая обрабатывает информацию о картах и о счетах"""
    name, number = confidential_info.rsplit(" ", maxsplit=1)
    if name.lower() == "счет":
        masked_number = get_mask_account(int(number))
    else:
        masked_number = get_mask_card_number(int(number))
    return f"{name} {masked_number}"


def get_date(operation_data: str) -> str:
    """ "Принимает на вход строку с датой в формате
    '2024-03-11T02:26:18.671407'
    и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    date_str, _ = operation_data.split('T')
    year, month, day = date_str.split('-')
    return f"{day}.{month}.{year}"
