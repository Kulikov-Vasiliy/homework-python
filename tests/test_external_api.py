import json
import os
from unittest.mock import Mock, mock_open, patch

import requests

from src.external_api import currency_to_rubs

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "operations.json")

@patch('requests.get')
def test_currency_to_rubs_api_success(mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 1000}
    mock_get.return_value = mock_response

    assert result == [{
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {
            "amount": 1000,
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560"
    }]
    result = currency_to_rubs("operations.json")
    assert isinstance(result, list)


def test_currency_to_rubs_if_file_not_found_error():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = currency_to_rubs("operations.json")
        assert result is None


def test_currency_to_rubs_if_json_decode_error():
    with patch("builtins.open", mock_open()) as mocked_file:
        side_effect = json.JSONDecodeError
        result = currency_to_rubs("operations.json")
        assert result == "некорректный формат"


def test_currency_to_rubs_if_json_incorrect():
    with patch("builtins.open", mock_open(read_data="not a json")) as mocked_file:
        side_effect = json.JSONDecodeError
        result = currency_to_rubs("operations.json")
        assert result == "некорректный формат"


def test_currency_to_rubs_if_json_none():
    with patch("builtins.open", mock_open(read_data=None)) as mocked_file:
        result = currency_to_rubs("operations.json")
        assert result == "некорректный формат"


@patch("requests.get")
def test_currency_to_rubs_if_4xx(mock_get, ignore='result in "converted.json"'):
    # Настраиваем mock на возврат ошибки HTTP 429
    mock_response = Mock()
    mock_response.status_code = 450
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "450 Client Error"
    )
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    result = currency_to_rubs("operations.json")
    assert result == "Client Error: 450"


@patch("requests.get")
def test_currency_to_rubs_if_5xx(mock_get):
    mock_response = Mock()
    mock_response.status_code = 504
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "504 Server Error"
    )
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    result = currency_to_rubs("operations.json")
    assert result == "Server Error"
