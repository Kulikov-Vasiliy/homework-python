from unittest.mock import Mock, patch

import requests

from src.external_api import currency_to_rubs


@patch("requests.get")
def test_currency_to_rubs_if_4xx(mock_get, operations_filled):
    # Настраиваем mock на возврат ошибки HTTP 429
    mock_response = Mock()
    mock_response.status_code = 450
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "450 Client Error"
    )
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    for operation in operations_filled:
        currency_code = operation["operationAmount"]["currency"]["code"]
        if currency_code != "RUB":
            result = currency_to_rubs(operation)
            assert result == "Client Error: 450"


@patch("requests.get")
def test_currency_to_rubs_if_5xx(mock_get, operations_filled):
    mock_response = Mock()
    mock_response.status_code = 504
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "504 Server Error"
    )
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    for operation in operations_filled:
        currency_code = operation["operationAmount"]["currency"]["code"]
        if currency_code != "RUB":
            result = currency_to_rubs(operation)
            assert result == "Server Error"


@patch("requests.get")
def test_currency_to_rubs_api_success(mock_get, operations_filled):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"success": True, "result": 1000.00}
    mock_get.return_value = mock_response

    for operation in operations_filled:
        currency_code = operation["operationAmount"]["currency"]["code"]
        if currency_code != "RUB":
            result = currency_to_rubs(operation)
            assert result == 1000.00


def test_currency_to_rubs_api_if_rub(operations_filled):
    for operation in operations_filled:
        currency_code = operation["operationAmount"]["currency"]["code"]
        amount = float(operation["operationAmount"]["amount"])
        if currency_code == "RUB":
            result = currency_to_rubs(operation)
            assert result == amount
