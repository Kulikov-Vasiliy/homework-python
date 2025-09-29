import numpy as np
import pandas as pd

from src import processing, widget
from src.filtration_of_operations import process_bank_search
from src.generators import filter_by_currency
from src.tables_reader import DATA_PATH_CSV, DATA_PATH_XLSX, read_csv, read_excel
from src.utils import DATA_PATH, json_to_list


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
    choice_ruas: list[dict] = []
    choice_rudes: list[dict] = []
    choice_ru: list[dict] = []
    choice_asc: list[dict] = []
    choice_des: list[dict] = []
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
            result = [
                el
                for el in choice_ruas
                if any(word in el["description"] for word in keywords)
            ]
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
            result = [
                el
                for el in choice_rudes
                if any(word in el["description"] for word in keywords)
            ]
        elif not keywords:
            result = process_bank_search(choice_rudes, search=user_words)

    elif user_choice_4 == "Да" and user_choice_3 == "Да" and user_choice_1 != "Да":
        print("Введите ключевое(ые) слово(а) для поиска")
        user_words = input("Вводить через ',' если несколько ключевых слов ").lower()
        keywords = [
            word.strip() for word in user_words.split(",")
        ]  # Убираем лишние пробелы
        if keywords:
            result = [
                el
                for el in choice_ru
                if any(word in el["description"] for word in keywords)
            ]
        elif not keywords:
            result = process_bank_search(choice_ru, search=user_words)

    elif user_choice_4 == "Да" and user_choice_3 != "Да" and user_choice_1 != "Да":
        print("Введите ключевое(ые) слово(а) для поиска")
        user_words = input("Вводить через ',' если несколько ключевых слов ").lower()
        keywords = [
            word.strip() for word in user_words.split(",")
        ]  # Убираем лишние пробелы
        if keywords:
            result = [
                el
                for el in state_filt
                if any(word in el["description"] for word in keywords)
            ]
        elif not keywords:
            result = process_bank_search(state_filt, search=user_words)

    return result


def main(result: list[dict]):  # type: ignore[return]
    """Функция отвечает за основную логику проекта и связывает функциональности между собой."""
    print("Распечатываю итоговый список транзакций...")

    if not result:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    else:
        to_return = []
        info_from = "" or np.nan
        info_to = "" or np.nan
        info_date = "" or np.nan
        info_desc = "" or np.nan
        info_am = "" or np.nan
        info_name = "" or np.nan
        total_operations = len(result)

        print(f"Всего банковских операций в выборке: {total_operations}")

        for info in result:
            if (
                "from" in info
                and isinstance(info["from"], str)
                and not pd.isna(info["from"])
            ):
                info_from = widget.mask_account_card(info["from"])
            else:
                info_from = None  # type: ignore[assignment]
            if "to" in info and isinstance(info["to"], str) and not pd.isna(info["to"]):
                info_to = widget.mask_account_card(info["to"])
            else:
                info_to = None  # type: ignore[assignment]
            if "date" in info and isinstance(info["date"], str):
                info_date = widget.get_date(info["date"])
            if "description" in info:
                info_desc = info["description"]
            if "operationAmount" not in info:
                info_am = info["amount"]
                info_name = info["currency_name"]
            elif "operationAmount" in info:
                info_am = info["operationAmount"]["amount"]
                info_name = info["operationAmount"]["currency"]["name"]

            if info_from is not None:
                to_return.append(
                    f"""{info_date} {info_desc}
{info_from} -> {info_to}
Сумма: {info_am} {info_name}"""
                )

            elif info_from is None:
                to_return.append(
                    f"""{info_date} {info_desc}
{info_to}
Сумма: {info_am} {info_name}"""
                )

        for el in to_return:
            print(el)


data = main_choice_file()
state_filt = main_choose_status(data)
result = main_extra_choices(state_filt)
main(result)
