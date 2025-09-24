import re

import os

from collections import Counter

BASE_DIR = os.path.dirname(__file__)
DATA_PATH_JSON = os.path.join(BASE_DIR, "..", "data", "operations.json")
DATA_PATH_CSV = os.path.join(BASE_DIR, "..", "data", "transactions.csv")
DATA_PATH_XLSX = os.path.join(BASE_DIR, "..", "data", "transactions_excel.xlsx")


def process_bank_search(data:list[dict], search:str)->list[dict]:
    """Функция принимает список словарей с данными о банковских операциях и строку поиска,
    и возвращает список словарей, у которых в описании есть данная строка."""
    try:
        finding = re.escape(search)
        result = []

        for operation in data:
            for search in operation:
                desc = operation["description"]
                if finding  in desc:
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
        counts = Counter()
        for operation in data:
            desc = operation.get("description", "")
            for category in categories:
                if category.lower() in desc.lower():
                    counts[category] += 1

        return dict(counts)

    except Exception as er:
        print(er)
