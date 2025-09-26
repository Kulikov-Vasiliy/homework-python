from src import masks, processing, widget
from src.decorators import my_function
from src.external_api import currency_to_rubs
from src.filtration_of_operations import process_bank_operations, DATA_PATH_JSON, process_bank_search
from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)
from src.tables_reader import DATA_PATH_CSV, DATA_PATH_XLSX, read_csv, read_excel
from src.utils import DATA_PATH, json_to_list, operations_filled


"""Ожидаемое поведение программы должно быть следующим:

Программа: Распечатываю итоговый список транзакций...

Программа: 
Всего банковских операций в выборке: 4
08.12.2019 Открытие вклада 
Счет **4321
Сумма: 40542 руб. 
12.11.2019 Перевод с карты на карту
MasterCard 7771 27** **** 3727 -> Visa Platinum 1293 38** **** 9203
Сумма: 130 USD
18.07.2018 Перевод организации 
Visa Platinum 7492 65** **** 7202 -> Счет **0034
Сумма: 8390 руб.
03.06.2018 Перевод со счета на счет
Счет **2935 -> Счет **4321
Сумма: 8200 EUR

Если выборка оказалась пустой, программа выводит сообщение:
Программа: Не найдено ни одной транзакции, подходящей под ваши
условия фильтрации"""


def main_choice_file():
    """Выбор файла для работы"""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    data = None
    while True:
        print("""Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла
2. Получить информацию о транзакциях из CSV-файла
3. Получить информацию о транзакциях из XLSX-файла""")

        user_choice = input("Введите что Вы выбрали ").strip()
        if user_choice == "1":
            print("Для обработки выбран JSON-файл")
            data = operations_filled
            break
        elif user_choice == "2":
            print("Для обработки выбран CSV-файл")
            data = read_csv(path_file=DATA_PATH_CSV)
            break
        elif user_choice == "3":
            print("Для обработки выбран XLSX-файл")
            data = read_excel(path_file=DATA_PATH_XLSX)
            break
        else:
            print("Необходимо ввести '1', '2' или '3'")

    return data


def main_choose_status(data):
    """Пользователь выбирает статус интересующих его операций"""
    print("Введите статус, по которому необходимо выполнить фильтрацию.")
    state = None
    while True:
        print("Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING")

        user_choice = input("что Вы выбрали? ").upper().strip()
        if user_choice in ["EXECUTED", "CANCELED", "PENDING"]:
            print(f"Операции отфильтрованы по статусу {user_choice}")
            state = user_choice
            break
        else:
            print(f"Статус операции '{user_choice}' недоступен")

    state_filt = process_bank_search(data, search=state)
    return  state_filt


def main_extra_choices(state_filt):
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
        elif user_choice_2 == "по убыванию"or user_choice_2 == "убыванию":
            choice_des = processing.sort_by_date(state_filt, ascending=True)

    print("Выводить только рублевые транзакции?")
    user_choice_3 = input("Да/Нет ").title()
    if user_choice_3 == "Да" and user_choice_1 == "Да" and "воз" in user_choice_2:
        choice_ruas = filter_by_currency(transactions=choice_asc, code="RUB")
    elif user_choice_3 == "Да" and user_choice_1 == "Да" and "убыв" in user_choice_2:
        choice_rudes = filter_by_currency(transactions=choice_des, code="RUB")
    elif user_choice_3 == "Да" and user_choice_1 != "Да":
        choice_ru =  filter_by_currency(transactions=state_filt)

    print("Отфильтровать список транзакций по определенному слову в описании?")
    categories = []
    user_choice_4 = input("Да/Нет ").title()
    if user_choice_4 == "Да" and user_choice_3 == "Да" and user_choice_1 == "Да" and "воз" in user_choice_2:
        print("Введите ключевое(ые) слово(а) для поиска")
        user_words = input("Вводить через ',' если несколько ключевых слов ").lower()
        if  ", " in user_words:
            user_words.split(", ")
            categories.append(user_words)
            result = process_bank_operations(choice_ruas, categories)
        elif  "," in user_words:
            user_words.split(",")
            categories.append(user_words)
            result = process_bank_operations(choice_ruas, categories)
        elif "," and ", " not in user_words:
            result = process_bank_search(choice_ruas,search=user_words)

    elif user_choice_4 == "Да" and user_choice_3 == "Да" and user_choice_1 == "Да" and "убыв" in user_choice_2:
        print("Введите ключевое(ые) слово(а) для поиска")
        user_words = input("Вводить через ',' если несколько ключевых слов ").lower()
        if  ", " in user_words:
            user_words.split(", ")
            categories.append(user_words)
            result = process_bank_operations(choice_rudes, categories)
        elif  "," in user_words:
            user_words.split(",")
            categories.append(user_words)
            result = process_bank_operations(choice_rudes, categories)
        elif "," and ", " not in user_words:
            result = process_bank_search(choice_rudes,search=user_words)

    elif user_choice_4 == "Да" and user_choice_3 == "Да" and user_choice_1 != "Да":
        print("Введите ключевое(ые) слово(а) для поиска")
        user_words = input("Вводить через ',' если несколько ключевых слов ").lower()
        if  ", " in user_words:
            user_words.split(", ")
            categories.append(user_words)
            result = process_bank_operations(choice_ru, categories)
        elif  "," in user_words and user_choice_3 == "Да" and user_choice_1 != "Да":
            user_words.split(",")
            categories.append(user_words)
            result = process_bank_operations(choice_ru, categories)
        elif "," and ", " not in user_words:
            result = process_bank_search(choice_ru,search=user_words)

    elif user_choice_4 == "Да" and user_choice_3 != "Да" and user_choice_1 != "Да":
        print("Введите ключевое(ые) слово(а) для поиска")
        user_words = input("Вводить через ',' если несколько ключевых слов ").lower()
        if ", " in user_words:
            user_words.split(", ")
            categories.append(user_words)
            result = process_bank_operations(state_filt, categories)
        elif "," in user_words:
            user_words.split(",")
            categories.append(user_words)
            result = process_bank_operations(state_filt, categories)
        elif "," and ", " not in user_words:
            result = process_bank_search(state_filt,search=user_words)

    return result


def main(result):
    """Функция отвечает за основную логику проекта и связывает функциональности между собой."""

    print("Распечатываю итоговый список транзакций...")
    print(widget.mask_account_card(result))






data = main_choice_file()
state_filt = main_choose_status(data)
result = main_extra_choices(state_filt)
main(result)

# if __name__ == "__main__":
#     print(main)
    # print(masks.get_mask_card_number("7000792289606361"))
    # print(masks.get_mask_account("73654108430135874305"))
    # print(
    #     widget.mask_account_card(
    #         "Maestro 1596837868705199"
    #         "MasterCard 7158300734726758"
    #         "Счет 35383033474447895560"
    #         "Visa Classic 6831982476737658"
    #         "Visa Platinum 8990922113665229"
    #         "Visa Gold 5999414228426353"
    #     )
    # )
    # print(widget.get_date("2024-03-11T02:26:18.671407"))
    # print(
    #     processing.filter_by_state(
    #         [
    #             {
    #                 "id": 41428829,
    #                 "state": "EXECUTED",
    #                 "date": "2019-07-03T18:35:29.512364",
    #             },
    #             {
    #                 "id": 939719570,
    #                 "state": "EXECUTED",
    #                 "date": "2018-06-30T02:08:58.425572",
    #             },
    #             {
    #                 "id": 594226727,
    #                 "state": "CANCELED",
    #                 "date": "2018-09-12T21:27:25.241689",
    #             },
    #             {
    #                 "id": 615064591,
    #                 "state": "CANCELED",
    #                 "date": "2018-10-14T08:21:33.419441",
    #             },
    #         ]
    #     )
    # )
    # print(
    #     processing.sort_by_date(
    #         [
    #             {
    #                 "id": 41428829,
    #                 "state": "EXECUTED",
    #                 "date": "2019-07-03T18:35:29.512364",
    #             },
    #             {
    #                 "id": 939719570,
    #                 "state": "EXECUTED",
    #                 "date": "2018-06-30T02:08:58.425572",
    #             },
    #             {
    #                 "id": 594226727,
    #                 "state": "CANCELED",
    #                 "date": "2018-09-12T21:27:25.241689",
    #             },
    #             {
    #                 "id": 615064591,
    #                 "state": "CANCELED",
    #                 "date": "2018-10-14T08:21:33.419441",
    #             },
    #         ]
    #     )
    # )
    # transactions = [
    #     {
    #         "id": 939719570,
    #         "state": "EXECUTED",
    #         "date": "2018-06-30T02:08:58.425572",
    #         "operationAmount": {
    #             "amount": "9824.07",
    #             "currency": {"name": "USD", "code": "USD"},
    #         },
    #         "description": "Перевод организации",
    #         "from": "Счет 75106830613657916952",
    #         "to": "Счет 11776614605963066702",
    #     },
    #     {
    #         "id": 142264268,
    #         "state": "EXECUTED",
    #         "date": "2019-04-04T23:20:05.206878",
    #         "operationAmount": {
    #             "amount": "79114.93",
    #             "currency": {"name": "USD", "code": "USD"},
    #         },
    #         "description": "Перевод со счета на счет",
    #         "from": "Счет 19708645243227258542",
    #         "to": "Счет 75651667383060284188",
    #     },
    #     {
    #         "id": 873106923,
    #         "state": "EXECUTED",
    #         "date": "2019-03-23T01:09:46.296404",
    #         "operationAmount": {
    #             "amount": "43318.34",
    #             "currency": {"name": "руб.", "code": "RUB"},
    #         },
    #         "description": "Перевод со счета на счет",
    #         "from": "Счет 44812258784861134719",
    #         "to": "Счет 74489636417521191160",
    #     },
    #     {
    #         "id": 895315941,
    #         "state": "EXECUTED",
    #         "date": "2018-08-19T04:27:37.904916",
    #         "operationAmount": {
    #             "amount": "56883.54",
    #             "currency": {"name": "USD", "code": "USD"},
    #         },
    #         "description": "Перевод с карты на карту",
    #         "from": "Visa Classic 6831982476737658",
    #         "to": "Visa Platinum 8990922113665229",
    #     },
    #     {
    #         "id": 594226727,
    #         "state": "CANCELED",
    #         "date": "2018-09-12T21:27:25.241689",
    #         "operationAmount": {
    #             "amount": "67314.70",
    #             "currency": {"name": "руб.", "code": "RUB"},
    #         },
    #         "description": "Перевод организации",
    #         "from": "Visa Platinum 1246377376343588",
    #         "to": "Счет 14211924144426031657",
    #     },
    # ]
    # usd_transactions = filter_by_currency(transactions, "USD")
    # for _ in range(2):
    #     print(next(usd_transactions))
    # descriptions = transaction_descriptions(transactions)
    # for _ in range(5):
    #     print(next(descriptions))
    # for card_number in card_number_generator(1, 3):  # type: ignore[attr-defined]
    #     print(card_number)
    # # my_function(1.1, 2.1)
    # for operation in json_to_list(path_file=DATA_PATH):
    #     print(currency_to_rubs(operation))
    # for row in read_csv(path_file=DATA_PATH_CSV):
    #     print(row)
    # print(process_bank_search(data=operations_filled, search="вклад"))
    # print(process_bank_search(data=read_csv(path_file=DATA_PATH_CSV), search="вклад"))
    # print(process_bank_search(data=read_excel(path_file=DATA_PATH_XLSX), search="вклад"))
    # print(read_excel(path_file=DATA_PATH_XLSX))
    # print(process_bank_operations(data=operations_filled,
    #                               categories=["открытие вклада", "Перевод организации"]))
    # print(process_bank_operations(data=read_csv(path_file=DATA_PATH_CSV),
    #                               categories=["открытие вклада", "Перевод организации"]))
    # print(process_bank_operations(data=read_excel(path_file=DATA_PATH_XLSX),
    #                               categories=["открытие вклада", "Перевод организации"]))
