def filter_by_currency(transactions: list[dict], code="USD") -> iter:  # type: ignore
    """Функция, принимающая на вход список словарей(транзакции)
    и возвращает итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной (например, USD)."""
    if transactions is None:
        raise TypeError("нет операций")
    for el in transactions:
        if el["operationAmount"]["currency"]["code"] == code:
            yield el


def transaction_descriptions(transactions: list[dict]) -> iter:  # type: ignore
    """Функция принимает список словарей с транзакциями
    и возвращает описание каждой операции по очереди."""
    if transactions is None:
        raise TypeError("нет операций")
    for el in transactions:
        if el["description"] is not None:
            yield el["description"]


def card_number_generator(start, stop: int, m=9999999999999999) -> iter:  # type: ignore
    """Функция выдает номера банковских карт в формате XXXX XXXX XXXX XXXX,
    где X — цифра номера карты. Генератор может сгенерировать номера карт в
    заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999.
    Генератор принимает начальное и конечное значения для генерации диапазона номеров"""
    if start < 1:
        raise ValueError("ошибка")
    elif start >= 1:
        if stop is None:
            stop = m
        for gen_num in range(start, (stop + 1)):
            less_m = 16 - len(str(gen_num))
            if less_m <= 16:
                card_num = ("0" * less_m) + str(gen_num)
                yield card_num[:4] + " " + card_num[4:8] + (" " "") + card_num[
                    8:12
                ] + " " + card_num[12:]
