import os
from unittest.mock import mock_open, patch
import csv
from src.tables_reader import *

BASE_DIR = os.path.dirname(__file__)
DATA_PATH_CSV = os.path.join(BASE_DIR, "..", "data", "transactions.csv")
DATA_PATH_XLSX = os.path.join(BASE_DIR, "..", "data", "transactions_excel.xlsx")


def test_read_csv_if_file_not_found_error(path_file=DATA_PATH_CSV):
    with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
        side_effect = FileNotFoundError  # noqa: F841
        result = read_csv(path_file)
        assert result == "Файл не найден"


def test_read_csv_decode_error(path_file=DATA_PATH_CSV):
    with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
        side_effect = csv.Error  # noqa: F841
        result = read_csv(path_file)
        assert result == f"Произошла ошибка {csv.Error}"


def test_read_csv_if_parsed_operations_is_none(path_file=DATA_PATH_CSV):
    with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
        mock_open(read_data=None)
        result = read_csv(path_file)
        assert result == "Пустой файл"

#
# def test_json_to_list_if_parsed_operations_is_not_list(path_file=DATA_PATH):
#     with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
#         mock_open(read_data='{"key": "value"}')
#         result = json_to_list(path_file)
#         assert result == []

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