from pprint import pprint

import numpy as np

from src import processing, widget
from src.filtration_of_operations import process_bank_search, process_bank_operations, DATA_PATH_JSON
from src.generators import filter_by_currency
from src.tables_reader import DATA_PATH_CSV, read_csv, read_excel, DATA_PATH_XLSX
from src.utils import json_to_list, DATA_PATH


def main_choice_file():
    """Выбор файла для работы"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    while True:
        data = None
        print(
            """Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла"""
        )

        user_choice = input("Введите что Вы выбрали ").strip()
        if user_choice == "1":
            data = json_to_list(path_file=DATA_PATH)
            print("Для обработки выбран JSON-файл")
            break
        elif user_choice == "2":
            data = read_csv(path_file=DATA_PATH_CSV)
            print("Для обработки выбран CSV-файл")
            break
        elif user_choice == "3":
            data = read_excel(path_file=DATA_PATH_XLSX)
            print("Для обработки выбран XLSX-файл")
            break
        else:
            print("Необходимо ввести '1', '2' или '3'")

    return data


def main_choose_status(data: list[dict]) -> list[dict]:
    """Пользователь выбирает статус интересующих его операций"""
    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    state_filt = []
    while True:
        state = None
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        user_choice = input("что Вы выбрали? ").upper().strip()
        if user_choice in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f"Операции отфильтрованы по статусу {user_choice}")
            state = user_choice
            break
        else:
            print(f"Статус операции '{user_choice}' недоступен")

    for el in data:
        if state == el["state"]:
            state_filt.append(el)

    return state_filt


def main_extra_choices(state_filt: list[dict]) -> list[dict]:
    """После фильтрации программа уточняет выборку операций, необходимых пользователю,
    и выводит в консоль операции, соответствующие выборке пользователя"""
    choice_asc = None
    choice_des = None
    choice_ruas = None
    choice_rudes = None
    result = state_filt

    print("Отсортировать операции по дате?")
    user_choice_1 = input("Да/Нет ").title()
    if user_choice_1 == "Да":
        print("Отсортировать по возрастанию или по убыванию?")
        user_choice_2 = input("по возрастанию/по убыванию ").lower()
        if user_choice_2 == "по возрастанию" or user_choice_2 == "возрастанию":
            choice_asc = processing.sort_by_date(state_filt)
        elif user_choice_2 == "по убыванию" or user_choice_2 == "убыванию":
            choice_des = processing.sort_by_date(state_filt, ascending=True)

    print("Выводить только рублевые транзакции?")
    user_choice_3 = input("Да/Нет ").title()
    if user_choice_3 == "Да" and user_choice_1 == "Да" and "воз" in user_choice_2:
        choice_ruas = filter_by_currency(transactions=choice_asc, code="RUB")
    elif user_choice_3 == "Да" and user_choice_1 == "Да" and "убыв" in user_choice_2:
        choice_rudes = filter_by_currency(transactions=choice_des, code="RUB")
    elif user_choice_3 == "Да" and user_choice_1 != "Да":
        choice_ru = filter_by_currency(transactions=state_filt)

    print("Отфильтровать список транзакций по определенному слову в описании?")
    categories = []
    user_choice_4 = input("Да/Нет ").title()
    if (
        user_choice_4 == "Да"
        and user_choice_3 == "Да"
        and user_choice_1 == "Да"
        and "воз" in user_choice_2
    ):
        print("Введите ключевое(ые) слово(а) для поиска")
        user_words = input("Вводить через ',' если несколько ключевых слов ").lower()
        keywords = [
            word.strip() for word in user_words.split(",")
        ]  # Убираем лишние пробелы
        if keywords:
            categories.extend(keywords)
            result = process_bank_operations(choice_ruas, categories)
        elif not keywords:
            result = process_bank_search(choice_ruas, search=user_words)

    elif (
        user_choice_4 == "Да"
        and user_choice_3 == "Да"
        and user_choice_1 == "Да"
        and "убыв" in user_choice_2
    ):
        print("Введите ключевое(ые) слово(а) для поиска")
        user_words = input("Вводить через ',' если несколько ключевых слов ").lower()
        keywords = [
            word.strip() for word in user_words.split(",")
        ]  # Убираем лишние пробелы
        if keywords:
            categories.extend(keywords)
            result = process_bank_operations(choice_rudes, categories)
        elif not keywords:
            result = process_bank_search(choice_rudes, search=user_words)

    elif user_choice_4 == "Да" and user_choice_3 == "Да" and user_choice_1 != "Да":
        print("Введите ключевое(ые) слово(а) для поиска")
        user_words = input("Вводить через ',' если несколько ключевых слов ").lower()
        keywords = [
            word.strip() for word in user_words.split(",")
        ]  # Убираем лишние пробелы
        if keywords:
            categories.extend(user_words)
            result = process_bank_operations(choice_ru, categories)
        elif not keywords:
            result = process_bank_search(choice_ru, search=user_words)

    elif user_choice_4 == "Да" and user_choice_3 != "Да" and user_choice_1 != "Да":
        print("Введите ключевое(ые) слово(а) для поиска")
        user_words = input("Вводить через ',' если несколько ключевых слов ").lower()
        keywords = [
            word.strip() for word in user_words.split(",")
        ]  # Убираем лишние пробелы
        if keywords:
            categories.extend(user_words)
            result = process_bank_operations(state_filt, categories)
        elif not keywords:
            result = process_bank_search(state_filt, search=user_words)

    return result


def main(result: list[dict]):
    """Функция отвечает за основную логику проекта и связывает функциональности между собой."""
    print("Распечатываю итоговый список транзакций...")
    info_from = np.nan
    info_to = np.nan
    info_date = np.nan
    info_desc = np.nan
    info_am = np.nan
    info_name = np.nan

    if result is not None:
        total_operations = len(result)
        for info in result:
            if "from" in info:
                info_from = widget.mask_account_card(info["from"])
            if "to" in info:
                info_to = widget.mask_account_card(info["to"])
            if "date" in info:
                info_date = widget.get_date(info["date"])
            if "description" in info:
                info_desc = info["description"]
            if "amount" in info:
                info_am = info["operationAmount"]["amount"]
            if "name" in info:
                info_name = info["operationAmount"]["currency"]["name"]

        if info_from is not None:
            print(
                f"""Всего банковских операций в выборке: {total_operations}
{info_date} {info_desc}
{info_from} -> {info_to}
Сумма: {info_am} {info_name}"""
            )

        elif info_from is None:
            print(
                f"""Всего банковских операций в выборке: {total_operations}
{info_date} {info_desc}
{info_to}
Сумма: {info_am} {info_name}"""
            )

        else:
            print(
                "Не найдено ни одной транзакции, подходящей под ваши условия фильтрации"
            )


data = main_choice_file()
state_filt = main_choose_status(data)
end = main_extra_choices(state_filt)
main(end)
