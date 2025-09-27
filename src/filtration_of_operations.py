import os
import re
from collections import Counter


BASE_DIR = os.path.dirname(__file__)
DATA_PATH_JSON = os.path.join(BASE_DIR, "..", "data", "operations.json")
DATA_PATH_CSV = os.path.join(BASE_DIR, "..", "data", "transactions.csv")
DATA_PATH_XLSX = os.path.join(BASE_DIR, "..", "data", "transactions_excel.xlsx")


def process_bank_search(data: list[dict], search: str) -> list[dict]:  # type: ignore[return]
    """Функция принимает список словарей с данными о банковских операциях и строку поиска,
    и возвращает список словарей, у которых в описании есть данная строка."""
    try:
        sample = re.compile(pattern=search, flags=re.IGNORECASE)
        result = []

        for operation in data:
            desc = operation.get("description").lower()
            finding = re.findall(sample, string=desc)
            if finding:  # Проверяем, не пустой ли список
                result.append(operation)

        return result

    except Exception as er:
        print(er)


def process_bank_operations(data: list[dict], categories: list) -> dict:  # type: ignore[return]
    """Функция принимает список словарей с данными о банковских операциях и список категорий операций,
    и возвращает словарь, в котором ключи — это названия категорий,
    а значения — это количество операций в каждой категории.
    (Категории операций хранятся в поле description.)"""
    try:
        counts = Counter()  # type: ignore[var-annotated]
        for operation in data:
            desc = operation.get("description", "")
            for category in categories:
                if category.lower() in desc.lower():
                    counts[category] += 1

        return dict(counts)

    except Exception as er:
        print(er)
