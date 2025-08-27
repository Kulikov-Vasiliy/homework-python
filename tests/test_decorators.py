import os
from unittest.mock import mock_open, patch

import pytest

from src.decorators import log, my_function

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "test_log.txt")


@log(filename=None)
def my_function_sum_args(x, y):
    return x + y


def test_my_function_file_output_a():
    with patch("builtins.open", mock_open()) as mocked_file:
        result = my_function_sum_args(2, 3)
        assert result == 5
        mocked_file.assert_not_called()
        # Проверка, что запись не произошла без filename


@log(filename=None)
def my_function_sum_kwargs(x, y):
    return x + y


def test_my_function_file_output_k():
    with patch("builtins.open", mock_open()) as mocked_file:
        result = my_function_sum_args(x=2, y=3)
        assert result == 5
        mocked_file.assert_not_called()


def test_my_function_args_err(capsys):
    with patch("builtins.open", mock_open()) as mocked_file:
        with pytest.raises(TypeError):
            my_function("1", 2)
            captured = capsys.readouterr()
            assert captured.out == (
                "my_function error: can only concatenate"
                " str (not 'int') to str. Inputs: ('1', 2), {}"
            )
            mocked_file.assert_not_called()


def test_my_function_kwargs_err(capsys):
    with patch("builtins.open", mock_open()) as mocked_file:
        with pytest.raises(TypeError):
            my_function(3, y="5")
            captured = capsys.readouterr()
            assert captured.out == (
                "my_function error: unsupported operand"
                " type(s) for +: 'int' and 'str'. Inputs: (3,), {'y': '5'}"
            )
            mocked_file.assert_not_called()


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (1, 4, 5),
        ("1", "4", "14"),
        (1.0, 4.1, 5.1),
        ("x=1", "y=4", "x=1y=4"),
        ("1", "y=2", "1y=2"),
        ({"x": 1, "y": 4}, None, 5),
        (1, {"y": 4}, 5),
    ],
)
def test_my_function(tmp_path, x, y, expected):
    log_file = tmp_path / "test_log.txt"
    with patch("src.decorators.DATA_PATH", str(log_file)):
        if isinstance(x, dict):
            assert my_function(**x) == expected
        elif isinstance(y, dict):
            y = y.get("y", 0)
        elif isinstance(x, dict) and isinstance(y, dict):
            merged = {**x, **y}
            assert my_function(**merged) == expected
        else:
            assert my_function(x, y) == expected
