import json
import os

from src.logger import logger

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "operations.json")

operations_filled = []


def json_to_list(path_file: str) -> list:
    """Функция принимает на вход путь до JSON-файла и возвращает список
    словарей с данными о финансовых транзакциях.
    * Если файл пустой, содержит не список или не найден,
    функция возвращает пустой список."""
    try:
        with open(path_file, "r", encoding="utf-8") as f:
            logger.info(f"Получаем файла из {path_file} и перевод  файла в python")
            parsed_operations = json.load(f)

            logger.info("Проверка заполнения файла и является ли он list")
            if parsed_operations is None or type(parsed_operations) is not list:
                logger.error("Не подходящий тип данных или их нет")
                return []

            logger.info('Прогон python-файл по операциям для "отсеивания" пустых')
            for operation in parsed_operations:
                if operation != {}:
                    operations_filled.append(operation)
                elif operation == {}:
                    logger.info("Нет записи об операции(ях)")

    except FileNotFoundError as er:
        logger.error(f"Произошла ошибка {er}")
        return []
    except json.JSONDecodeError as er:
        logger.error(f"Произошла ошибка {er}")
        return []

    finally:
        logger.info('Возврат "чистого" списка операций')
        return operations_filled
