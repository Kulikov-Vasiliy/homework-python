import json
import os
import time

import requests
from dotenv import load_dotenv

from src import utils

BASE_DIR = os.path.dirname(__file__)

load_dotenv()
DATA_PATH_API = os.getenv("API_KEY")

DATA_PATH_CONVERTED = os.path.join(BASE_DIR, "..", "data", "converted.json")


def currency_to_rubs(operations: list[dict]) -> float | str:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях.
    * Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения
    текущего курса валют и конвертации суммы операции в рубли."""
    try:
        operations = utils.json_to_list("operations.json")  # type: ignore

        for operation in operations:
            amount = operation.get("operationAmount", {}).get("amount")
            currency_code = operation.get("operationAmount", {}).get("currency", {}).get("code")

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

    except requests.exceptions.HTTPError:
        if 500 <= response.status_code < 600:
            return "Server Error"
        elif 400 <= response.status_code < 500:
            return f"Client Error: {response.status_code}"


def write_to_file(converted_amount: float, file_path: str):
    operations = utils.json_to_list("operations.json")  # type: ignore
    for operation in operations:
        if isinstance(operation, dict) and "operationAmount" in operation:
            if operation.get("operationAmount", {}).get("currency", {}).get("code") != "RUB":
                operation["operationAmount"]["amount"] = converted_amount
                operation["operationAmount"]["currency"]["code"] = "RUB"
                operation["operationAmount"]["currency"]["name"] = "руб."

    with open(file_path, "w", encoding="UTF-8") as f:
        json.dump(operations, f, ensure_ascii=False, indent=2)
    print('result in "converted.json"')


converted_operations = currency_to_rubs("operations.json")  # type: ignore
write_to_file(converted_operations, DATA_PATH_CONVERTED)
