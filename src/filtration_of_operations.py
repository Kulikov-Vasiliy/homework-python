import re

import os

from src.logger import logger

from collections import Counter, defaultdict

from src.utils import operations_filled

from src.tables_reader import read_csv, read_excel

BASE_DIR = os.path.dirname(__file__)
DATA_PATH_JSON = os.path.join(BASE_DIR, "..", "data", "operations.json")
DATA_PATH_CSV = os.path.join(BASE_DIR, "..", "data", "transactions.csv")
DATA_PATH_XLSX = os.path.join(BASE_DIR, "..", "data", "transactions_excel.xlsx")





def process_bank_search(data:list[dict], search:str)->list[dict]:
    """Функция принимает список словарей с данными о банковских операциях и строку поиска,
    и возвращает список словарей, у которых в описании есть данная строка."""
    try:
        re.escape(search)
        result = []

        for operation in data:
            for search in operation:
                desc = operation.get("description")
                if search in desc:
                   wanted_desc = re.findall(search, desc, re.IGNORECASE)
                   print(type(wanted_desc))
                   result.append(operation)
        return result

    except Exception as er:
        print(er)


def process_bank_operations(data:list[dict], categories:list)->dict:
    """Функция принимает список словарей с данными о банковских операциях и список категорий операций,
    и возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.
    (Категории операций хранятся в поле description.)"""
    try:
        sorted_categories = defaultdict(list)

        for operation in data:
            for categories in operation:
                desc = operation.get("description")
                if categories in desc:
                    value = Counter(desc)
                    sorted_categories[desc].append(value)
        return sorted_categories

    except Exception as er:
        print(er)


if __name__ == "__main__":
    print(process_bank_search(data=operations_filled, search="вклад".lower()),logging.NullHandler())
    print(process_bank_search(data=read_csv(path_file=DATA_PATH_CSV), search="вклад".lower()))
    print(process_bank_search(data=read_excel(path_file=DATA_PATH_XLSX), search="вклад".lower()))
    print(process_bank_operations(data=operations_filled, categories=["открытие вклада", "Перевод организации"]))
    print(process_bank_operations(data=read_csv(path_file=DATA_PATH_CSV), categories=["открытие вклада", "Перевод организации"]))
    print(process_bank_operations(data=read_excel(path_file=DATA_PATH_XLSX), categories=["открытие вклада", "Перевод организации"]))
