import os
import time

import requests
from dotenv import load_dotenv

from src.utils import DATA_PATH, json_to_list, operations_filled

load_dotenv()
DATA_PATH_API = os.getenv("API_KEY")


def currency_to_rubs(operations: list[dict]) -> float | str:  # type: ignore[return]
    """Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях.
    * Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения
    текущего курса валют и конвертации суммы операции в рубли."""
    try:
        for operation in operations_filled:
            amount = operation["operationAmount"]["amount"]
            currency_code = operation["operationAmount"]["currency"]["code"]

            if currency_code != "RUB":

                payload = {"amount": float(amount), "from": currency_code, "to": "RUB"}
                url = "https://api.apilayer.com/exchangerates_data/convert"
                headers = {"apikey": DATA_PATH_API}
                response = requests.get(url, headers=headers, params=payload)

                response.raise_for_status()
                result = response.json()
                converted_amount = round(result.get("result", 0), 2)  # noqa: F841
                time.sleep(3)

                return converted_amount

    except requests.exceptions.HTTPError:
        if 500 <= response.status_code < 600:
            return "Server Error"
        elif 400 <= response.status_code < 500:
            return f"Client Error: {response.status_code}"


for operation in json_to_list(DATA_PATH):
    print(currency_to_rubs(operation))  # type:ignore


operations = json_to_list(path_file=DATA_PATH)
converted_operations = currency_to_rubs(operations)
