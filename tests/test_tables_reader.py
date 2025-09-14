import csv
import os
import pandas as pd
from unittest.mock import mock_open, patch, Mock

from src.tables_reader import *

BASE_DIR = os.path.dirname(__file__)
DATA_PATH_CSV = os.path.join(BASE_DIR, "..", "data", "transactions.csv")
DATA_PATH_XLSX = os.path.join(BASE_DIR, "..", "data", "transactions_excel.xlsx")



# @patch()
# def test_read_csv_if_file_not_found_error(path_file=DATA_PATH_CSV):
#     with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
#         mocked_file.side_effect = FileNotFoundError
#         # side_effect = FileNotFoundError  # noqa: F841
#         result = read_csv(path_file)
#         assert result == "Файл не найден"


# def test_file_not_found(path_file=DATA_PATH_CSV):
#     with patch("builtins.open", side_effect=FileNotFoundError):
#         result = read_csv(path_file)
#         assert result == "Файл не найден"


# def test_read_csv_decode_error(path_file=DATA_PATH_CSV):
#     with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
#         mocked_file.side_effect = csv.Error("Ошибка чтения")
#         # side_effect = csv.Error  # noqa: F841
#         result = read_csv(path_file)
#         assert result == f"Произошла ошибка Ошибка чтения"


# def test_read_csv_if_parsed_is_none(path_file=DATA_PATH_CSV):
#     with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
#         mock_open(read_data=None)
#         result = read_csv(path_file)
#         assert result == "Пустой файл"

#
# def test_read_csv_if_delimiter(path_file=DATA_PATH_CSV):
#     with patch("builtins.open", mock_open(read_data=",")) as mocked_file:
#         result = read_csv(path_file)
#         assert result == "Неверный делимитер в файле. Ожидался: ';'"
    # with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
    #     mock_open(read_data=',')
    #     result = read_csv(path_file)
    #     # raise ValueError(f"Неверный делимитер в файле. Ожидался: '{delimiter}'")
    #     assert result == "Неверный делимитер в файле. Ожидался: ';'"


# def test_read_csv_if_column(path_file=DATA_PATH_CSV):
#     with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
#         mocked_file.side_effect = "'1';2;3.0"
#         # mock_open(read_data='"1";"2";"3"')
#         result = read_csv(path_file)
#         # ValueError("должно быть 9 столбцов")
#         assert result == "должно быть 9 столбцов"

# @patch("module_name.mock_get")
# def test_invalid_number_of_columns(mock_get, path_file=DATA_PATH_CSV):
#     mock_data = "col1;col2;col3;col4;col5;col6;col7;col8\n" \
#                 "val1;val2;val3;val4;val5;val6;val7;val8\n"
#     with patch("builtins.open", mock_open(read_data=mock_data)):
#         result = read_csv(path_file)
#         mock_get.assertEqual(result, "должно быть 9 столбцов")


# def test_read_csv_if_newline(path_file=DATA_PATH_CSV):
#     with patch(
#         "builtins.open",
#         mock_open(read_data="id,state,date,amount\n1,EXECUTED,2023-09-05T11:30:32Z"),
#     ) as mocked_file:  # noqa: F841
#         result = read_csv(path_file)
#         assert result == "должно быть 9 столбцов"
#     mock_open(read_data_newline=".")
#     result = read_csv(path_file)
#     # ValueError("должно быть 9 столбцов")
#     assert result == "должно быть 9 столбцов"

#
# def test_read_csv_pd(path_file=DATA_PATH_CSV):
#     with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
#         result = read_csv(
#             [
#         {
#             "id": 650703.0,
#             "state": "EXECUTED",
#             "date": "2023-09-05T11:30:32Z",
#             "amount": 16210.0,
#             "currency_name": "Sol",
#             "currency_code": "PEN",
#             "from": "Счет 58803664561298323391",
#             "to": "Счет 39745660563456619397",
#             "description": "Перевод организации",
#         },
#         {
#             "id": 3598919.0,
#             "state": "EXECUTED",
#             "date": "2020-12-06T23:00:58Z",
#             "amount": 29740.0,
#             "currency_name": "Peso",
#             "currency_code": "COP",
#             "from": "Discover 3172601889670065",
#             "to": "Discover 0720428384694643",
#             "description": "Перевод с карты на карту",
#         },
#     ]
#         )
#     expected = [
#         {
#             "id": 650703.0,
#             "state": "EXECUTED",
#             "date": "2023-09-05T11:30:32Z",
#             "amount": 16210.0,
#             "currency_name": "Sol",
#             "currency_code": "PEN",
#             "from": "Счет 58803664561298323391",
#             "to": "Счет 39745660563456619397",
#             "description": "Перевод организации",
#         },
#         {
#             "id": 3598919.0,
#             "state": "EXECUTED",
#             "date": "2020-12-06T23:00:58Z",
#             "amount": 29740.0,
#             "currency_name": "Peso",
#             "currency_code": "COP",
#             "from": "Discover 3172601889670065",
#             "to": "Discover 0720428384694643",
#             "description": "Перевод с карты на карту",
#         },
#     ]
#     assert result == expected
