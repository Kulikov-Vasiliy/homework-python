import logging
"""Реализуйте запись логов в файл. Логи должны записываться в папку logs в корне проекта. 
Файлы логов должны иметь расширение .log.
Формат записи лога в файл должен включать метку времени, название модуля, уровень серьезности 
и сообщение, описывающее событие или ошибку, которые произошли.
Лог должен перезаписываться при каждом запуске приложения."""


import json
import os

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "operations.json")

operations_filled = []


def json_to_list(path_file: list[dict]) -> list[dict]:
    """Функция принимает на вход путь до JSON-файла и возвращает список
    словарей с данными о финансовых транзакциях.
    * Если файл пустой, содержит не список или не найден,
    функция возвращает пустой список."""
    try:

        with open(DATA_PATH, "r", encoding="utf-8") as f:
            parsed_operations = json.load(f)

            if parsed_operations is None or type(parsed_operations) is not list:
                return []

            for operation in parsed_operations:
                if operation != {}:
                    operations_filled.append(operation)

    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    finally:
        return operations_filled
