import csv
import os
import pandas as pd
from pandas import read_excel
from unittest.mock import mock_open, patch
import pytest
from src.tables_reader import read_csv, read_excel


BASE_DIR = os.path.dirname(__file__)
DATA_PATH_CSV = os.path.join(BASE_DIR, "..", "data", "transactions.csv")
DATA_PATH_XLSX = os.path.join(BASE_DIR, "..", "data", "transactions_excel.xlsx")




# если возвращать dataframe
# def test_valid_csv():
#     # Создаем временный файл с корректными данными
#     content = "col1;col2;col3;col4;col5;col6;col7;col8;col9\n1;2;3;4;5;6;7;8;9\n10;11;12;13;14;15;16;17;18\n"
#     with tempfile.NamedTemporaryFile(mode='w+', newline='', encoding='utf-8', delete=False) as temp_file:
#         temp_file.write(content)
#         temp_file.seek(0)
#         df = read_csv(temp_file.name)
#
#     # Проверяем, что результат - это DataFrame и имеет правильные размеры
#     assert isinstance(df, pd.DataFrame)
#     assert df.shape == (2, 9)  # 2 строки и 9 столбцов
#
#     os.remove(temp_file.name)  # Удаляем временный файл


# def test_read_csv_error_csv():
#     # Создаем временный файл с некорректными данными
#     content = "col1;col2;col3;col4;col5;col6;col7;col8;col9\n1;2;3;4;5;6;7;8;9\n1;2;3;4;5;6;7;8\n"
#     with tempfile.NamedTemporaryFile(mode='w+', newline='', encoding='utf-8', delete=False) as temp_file:
#         temp_file.write(content)
#         temp_file.seek(0)
#         result = read_csv(temp_file.name)
#
#     assert isinstance(result, pd.DataFrame)
#
#     os.remove(temp_file.name)






def test_read_csv_if_file_not_found_error(path_file=DATA_PATH_CSV):
    with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
        mocked_file.side_effect = FileNotFoundError
        result = read_csv(path_file)
        assert result == "Файл не найден"


def test_read_csv_decode_error(path_file=DATA_PATH_CSV):
    with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
        mocked_file.side_effect = csv.Error("Ошибка чтения")
        result = read_csv(path_file)
        assert result == f"Произошла ошибка Ошибка чтения"


def test_read_csv_if_none(path_file=DATA_PATH_CSV):
    with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
        mock_open(read_data='')
        result = read_csv(path_file)
        assert result == "Пустой файл"


def test_read_csv_if_none_delimiter(path_file=DATA_PATH_CSV):
    with patch("builtins.open", mock_open()) as mocked_file:  # noqa: F841
        mock_open(read_data=';')
        result = read_csv(path_file)
        assert result == "Пустой файл"


@pytest.mark.parametrize("data, expected", [
    ("col1,col2,col3,col4,col5,col6,col7,col8,col9\n"
     "val1;val2;val3;val4;val5;val6;val7;val8;val9\n",
    ["Неверный делимитер в строке: 'col1,col2,col3,col4,col5,col6,col7,col8,col9'. Ожидался: ;",
    "Неверный делимитер в строке: 'val1,val2,val3,val4,val5,val6,val7,val8,val9'. Ожидался: ;"]),
    ("col1;col2;col3;col4;col5;col6;col7;col8;col9\n"
    "val1;val2;val3;val4;val5;val6.val7;val8;val9\n",
     ["Неверный делимитер в строке: 'col1;col2;col3;col4;col5.col6;col7;col8;col9'. Ожидался: ;"])
])
def test_read_csv_delimiter(data, expected):
    with patch("builtins.open", mock_open(read_data=data)) as mocked_file:
        file_path = "mocked_file.csv"
        with open(file_path, "r") as file:
            lines = file.readlines()
            errors = []
            delimiter = ';'
            for line in lines:
                if delimiter not in line:
                    errors.append(f"Неверный делимитер в строке: '{line.strip()}'. Ожидался: {delimiter}")


@pytest.mark.parametrize("data", [
    ("col1;col2;col3;col4;col5;col6;col7;col8\n"
    "val1;val2;val3;val4;val5;val6;val7;val8\n"),
    ("col1;col2;col3;col4;col5;col6;col7;col8;col9;col10\n"
    "val1;val2;val3;val4;val5;val6;val7;val8;val9;val10\n")
])
def test_read_csv_columns(data):
    with patch("builtins.open", mock_open(read_data=data)) as mocked_file:  # noqa: F841
        # Здесь используй фиктивный путь к файлу
        file_path = "mocked_file.csv"
        with pytest.raises(ValueError, match="должно быть 9 столбцов"):
            read_csv(file_path)


def test_read_csv_success(expected_reader, path_file=DATA_PATH_CSV):
    result = read_csv(path_file)
    assert result == expected_reader


def test_read_excel_if_file_not_found_error(path_file=DATA_PATH_XLSX):
    with patch("pandas.read_excel", side_effect=FileNotFoundError):
        result = read_excel(path_file)
        assert result == "Файл не найден"



@patch("pandas.read_excel", side_effect=ValueError("Ошибка чтения"))
def test_read_excel_decode_error(mock_read_excel, path_file=DATA_PATH_XLSX):  # noqa: F841
    result = read_excel(path_file)
    assert result == "Произошла ошибка Ошибка чтения"


@patch("pandas.read_excel", return_value=pd.DataFrame())
def test_read_excel_if_none(mock_read_excel, path_file=DATA_PATH_XLSX):
    result = read_excel(path_file)
    assert result == "Пустой файл"


def test_read_excel_success(expected_reader_xl, path_file=DATA_PATH_XLSX):
    result = read_excel(path_file)
    assert result == pd.DataFrame(expected_reader_xl)
