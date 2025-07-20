def filter_by_state(my_list: list,state='EXECUTED') -> list:
    """Функция принимает список словарей и опционально значение для ключа 'state'(по умолчанию 'EXECUTED')
    и возвращает новый список словарей, содержащий только те словари,
    у которых ключ 'state' соответствует указанному значению."""

    return  [el for el in my_list if el["state"] == state]
