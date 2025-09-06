import os
import time

import requests

# noinspection PyUnresolvedReferences
from dotenv import load_dotenv


load_dotenv()
DATA_PATH_API = os.getenv("API_KEY")


def currency_to_rubs(operation: dict) -> float | str:  # type: ignore[return]
    """Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях.
    * Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения
    текущего курса валют и конвертации суммы операции в рубли."""
    response = None
    try:

        amount = operation["operationAmount"]["amount"]
        currency_code = operation["operationAmount"]["currency"]["code"]
        if currency_code != "RUB":

            payload = {"amount": float(amount), "from": currency_code, "to": "RUB"}
            url = "https://api.apilayer.com/exchangerates_data/convert"
            headers = {"apikey": DATA_PATH_API}
            response = requests.get(url, headers=headers, params=payload)

            response.raise_for_status()
            result = response.json()
            converted_amount = result.get("result", 0)
            time.sleep(3)

            return converted_amount
        return amount

    except requests.exceptions.HTTPError:
        if 500 <= response.status_code < 600:
            return "Server Error"
        elif 400 <= response.status_code < 500:
            return f"Client Error: {response.status_code}"
