import csv
import os

# noinspection PyUnresolvedReferences
import pandas as pd

BASE_DIR = os.path.dirname(__file__)
DATA_PATH_CSV = os.path.join(BASE_DIR, "..", "data", "transactions.csv")
DATA_PATH_XLSX = os.path.join(BASE_DIR, "..", "data", "transactions_excel.xlsx")


def read_csv(path_file: str) -> list | str:
    """Функция принимает на вход путь до csv-файла и выводит список без пустых строк"""
    try:
        with open(path_file, "r", newline="", encoding="utf-8") as file:
            lines = file.readlines()
            delimiter = ";"

            if not lines:
                return "Пустой файл"

            # Проверка на делимитер во всех строках
            for line in lines:
                if delimiter not in line:
                    raise ValueError(f"Неверный делимитер в строке: '{line.strip()}'. Ожидался: {delimiter}")

            # Проверка на количество столбцов во всех строках
            for line in lines:
                if line.strip() and line.count(delimiter) != 8:
                    raise ValueError("должно быть 9 столбцов")

            file.seek(0)
            parsed = csv.DictReader(file, delimiter=delimiter)

            filtered_rows = [
                row for row in parsed if any(field.strip() for field in row.values())
            ]

            return filtered_rows

    except FileNotFoundError:
        return "Файл не найден"
    except csv.Error as er:
        return f"Произошла ошибка {er}"


def read_excel(path_file: str) -> list | str:
    """Функция принимает на вход путь до xlsx-файла и выводит список без пустых строк"""
    try:
        file = pd.read_excel(path_file)
        if file.empty:
            return "Пустой файл"

        excel_data = pd.read_excel(path_file, sheet_name="Лист 1")
        excel_data_clear = excel_data.dropna(how="all")
        excel_list = excel_data_clear.to_dict(orient='records')

        return excel_list

    except FileNotFoundError:
        return "Файл не найден"
    except ValueError as er:
        return f"Произошла ошибка {er}"
