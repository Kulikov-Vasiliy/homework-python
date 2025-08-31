import logging
"""Реализуйте запись логов в файл. Логи должны записываться в папку logs в корне проекта. 
Файлы логов должны иметь расширение .log.
Формат записи лога в файл должен включать метку времени, название модуля, уровень серьезности 
и сообщение, описывающее событие или ошибку, которые произошли.
Лог должен перезаписываться при каждом запуске приложения."""

def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    if not card_number.isdigit():
        raise TypeError("некорректный тип данных")
    if len(card_number) != 16:
        raise ValueError(
            "номер карты должен состоять из 16 символов или нет открытых продуктов"
        )
    first_num = card_number[0:4]
    middle_num = card_number[4:6]
    last_num = card_number[-4:]
    return f"{first_num} {middle_num}** **** {last_num}"


def get_mask_account(client_account: str) -> str:
    """Функция маскировки номера банковского счета"""
    if not client_account.isdigit():
        raise TypeError("некорректный тип данных или нет открытых счетов")
    if len(client_account) != 20:
        raise ValueError("банковский счет должен состоять из 20 символов")
    late_num = client_account[-4:]
    return f"**{late_num}"
