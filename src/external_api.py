import json
import os
import time

import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "operations.json")
load_dotenv()
DATA_PATH_API = os.getenv("API_KEY")

DATA_PATH_CONVERTED = os.path.join(BASE_DIR, "..", "data", "converted.json")


def currency_to_rubs(operations: list[dict]) -> list[dict] | str | None:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях.
    * Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения
    текущего курса валют и конвертации суммы операции в рубли."""
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            operations = json.load(f)

            for operation in operations:
                if operation == {}:
                    continue
                amount = operation.get("operationAmount", {}).get("amount")
                currency_code = (
                    operation.get("operationAmount", {}).get("currency", {}).get("code")
                )
                # currency_name = (
                #     operation.get("operationAmount", {}).get("currency", {}).get("name")
                # )

                if currency_code != "RUB":
                    payload = {"amount": amount, "from": currency_code, "to": "RUB"}
                    url = "https://api.apilayer.com/exchangerates_data/convert"
                    headers = {"apikey": DATA_PATH_API}
                    response = requests.get(url, headers=headers, params=payload)
                    print(response)

                    response.raise_for_status()
                    result = response.json()
                    converted_amount = result.get("result", 0)

                    operation["operationAmount"]["amount"] = converted_amount
                    operation["operationAmount"]["currency"]["code"] = "RUB"
                    operation["operationAmount"]["currency"]["name"] = "руб."
                    time.sleep(1)

        # with open(DATA_PATH_CONVERTED, "w", encoding="UTF-8") as f:
        #     json.dump(operations, f, ensure_ascii=False, indent=2)
        #     print('result in "converted.json"')

    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return "некорректный формат"
    except requests.exceptions.HTTPError:
        if 500 <= response.status_code < 600:
            return "Server Error"
        elif 400 <= response.status_code < 500:
            return f"Client Error: {response.status_code}"

    # except FileNotFoundError:
    #     return None
    # except json.JSONDecodeError:
    #     return "некорректный формат"
    # except requests.exceptions.HTTPError as e:
    #     status_code = e.response.status_code if hasattr(e, 'response') else None
    #     if status_code:
    #         if 500 <= status_code < 600:
    #             return "Server Error"
    #         elif 400 <= status_code < 500:
    #             return f"Client Error: {status_code}"
    #         return f"HTTP Error: {str(e)}"
    # except Exception as e:
    #     return f"Unexpected error: {str(e)}"


def write_to_file(operations: list[dict], file_path: str):
    with open(file_path, "w", encoding="UTF-8") as f:
        json.dump(operations, f, ensure_ascii=False, indent=2)
        print('result in "converted.json"')

converted_operations = currency_to_rubs("operations.json")
write_to_file(converted_operations, DATA_PATH_CONVERTED)
